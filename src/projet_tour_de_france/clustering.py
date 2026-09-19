import pandas as pd

from sklearn.cluster import AgglomerativeClustering, KMeans
from sklearn.metrics import silhouette_score


def _cluster_KMeans(villages, N_STAGES):
    """
    Cluster les villages en N_STAGES étapes avec algo KMeans.
    Arguments:
    villages -- DataFrame contenant les  villages avec les colonnes en km : 'x_km' and 'y_km' 
    Returns:
    labels_kmeans -- tableau liste des étapes rattachées à chaque village pour l'algo de clustering'
    """
    X = villages[['x_km', 'y_km']]
    kmeans = KMeans(n_clusters=N_STAGES, n_init=10, random_state=42)  # définition du modèle et de ses paramètres
    labels_kmeans = kmeans.fit_predict(X)   #calcule les centroïdes et prédit les clusters, retourne l'index des clusters associé à chaque village
    return labels_kmeans


def _cluster_Agglomerative(villages, N_STAGES):
    """
    Cluster les villages en N_STAGES étapes avec Agglomerative Clustering.
    Arguments:
    villages -- DataFrame contenant les  villages avec les colonnes en km : 'x_km' and 'y_km' 
    Returns:
    labels_agglo -- tableau liste des étapes rattachées à chaque village pour l'algo de clustering'
    """
    X = villages[['x_km', 'y_km']]
    cah = AgglomerativeClustering(n_clusters=N_STAGES, linkage="ward")
    labels_cah = cah.fit_predict(X)  # définition du modèle et de ses paramètres
    return labels_cah


def _silhouette_score_kmeans(villages, labels_kmeans):   
    """
    Calcule le silhouette score pour  KMeans clustering.
    Arguments:
    villages -- DataFrame contenant les  villages avec les colonnes en km : 'x_km' and 'y_km' 
    labels_kmeans -- array of cluster labels for each village
    Returns:
    score_kmeans -- silhouette score for KMeans clustering
    """
    X = villages[['x_km', 'y_km']]
    sil_kmeans = silhouette_score(X, labels_kmeans)
    return sil_kmeans


def _silhouette_score_cah(villages, labels_cah):
    """
    Calcule le silhouette score pour Agglomerative Clustering.
    Arguments:
    villages -- DataFrame contenant les  villages avec les colonnes en km : 'x_km' and 'y_km' 
    labels_cah -- array of cluster labels for each village
    Returns:
    score_cah -- silhouette score for Agglomerative Clustering
    """
    X = villages[['x_km', 'y_km']]
    sil_cah = silhouette_score(X, labels_cah)
    return sil_cah


def _comparison_KMeans_Cah(sil_kmeans, sil_cah, labels_kmeans, labels_cah, N_STAGES):
    """
    Compare les scores de silhouette des algos KMeans and Agglomerative Clustering, et l'étendue des labels.
    Arguments:
    sil_kmeans -- silhouette score pour KMeans clustering
    sil_cah -- silhouette score pour Agglomerative Clustering
    labels_kmeans -- tableau liste des étapes rattachées à chaque village pour le KMeans
    labels_cah -- tableau liste des étapes rattachées à chaque village pour le  Agglomerative Clustering
    Returns:
    best_method -- retourne les labels de la méthode ayant le meilleur score de silhouette et des clusters valides (au moins 2 villages par cluster)
    """
    sizes_kmeans= pd.Series(labels_kmeans).value_counts()    #on transforme le numpy à une dimension en serie pandas pour pouvoir calculer min et max
    sizes_cah = pd.Series(labels_cah).value_counts()
    # cas posant problème : si les deux méthodes ne donnent pas exactement N_STAGES clusters, ou si un cluster a moins de 2 villages, on ne peut pas faire un tour de France en 21 étapes
    if len(set(labels_kmeans)) != N_STAGES and len(set(labels_cah)) != N_STAGES:
        raise ValueError(f"Aucune des méthodes de clustering n'a produit exactement {N_STAGES} clusters. Impossible de faire un tour de France en 21 étapes")
    if len(set(labels_kmeans)) != N_STAGES and sizes_kmeans.min() < 2:
        raise ValueError(f"La méthode KMeans n'a pas produit exactement {N_STAGES} clusters ou un cluster a moins de 2 villages. Impossible de faire un tour de France en 21 vraies étapes")
    if len(set(labels_cah)) != N_STAGES and sizes_cah.min() < 2:
        raise ValueError(f"La méthode Agglomerative Clustering n'a pas produit exactement {N_STAGES} clusters ou un cluster a moins de 2 villages. Impossible de faire un tour de France en 21 vraies étapes")
    if sizes_kmeans.min() < 2 and sizes_cah.min() < 2:
        raise ValueError(f"Les 2 méthodes de clustering ont produit des clusters avec moins de 2 villages. Impossible de faire un tour de France en 21 vraies étapes")
    # cas où pas de choix possible : si une étape n'a qu'un seul village, on ne peut pas faire un tour de France en 21 vraies étapes
    if sizes_kmeans.min() < 2:
        return labels_cah
    if sizes_cah.min() < 2:
        return labels_kmeans
    # on a bien 21 étapes de plus de 2 villages pour les 2 méthodes, on peut comparer les scores de silhouette
    if sil_kmeans > sil_cah:
        return labels_kmeans
    else:
        return labels_cah


def get_best_clustering(villages, N_STAGES):
    """
    Determine la meilleure méthode de clustering (KMeans or Agglomerative Clustering) basée sur le score de silhouette et/ou la taille des étapes.
    Arguments:
    villages -- DataFrame contenant les  villages avec les colonnes en km : 'x_km' and 'y_km' 
    Returns:
    best_clustering  -- tableau de labels (numéro des étapes) pour chaque village, tableau obtenu grâce à la meilleure méthode de clustering  
    """
    labels_kmeans = _cluster_KMeans(villages, N_STAGES)
    labels_cah = _cluster_Agglomerative(villages, N_STAGES)
    sil_kmeans = _silhouette_score_kmeans(villages, labels_kmeans)
    sil_cah = _silhouette_score_cah(villages, labels_cah)
    best_clustering = _comparison_KMeans_Cah(sil_kmeans, sil_cah, labels_kmeans, labels_cah, N_STAGES)
    return best_clustering