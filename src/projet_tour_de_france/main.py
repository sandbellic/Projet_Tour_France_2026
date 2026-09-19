
from projet_tour_de_france.clustering import get_best_clustering
from projet_tour_de_france.utils import load_villages, add_villages_latlon_km, add_villages_stage
from projet_tour_de_france.distances import best_paths
from projet_tour_de_france.vizualisation import print_roadbook, plot_final_tour, plot_stages

N_STAGES = 21

def main():

 
    villages = load_villages()      #charge les 120 villages sélectionnés pour le Tour de France dans un DataFrame
    villages = add_villages_latlon_km(villages)                         # ajoute 2 colonnes au DataFrame : les coordonnées transformées en km

    # Utilisation du ML pour calcul des clusters de villages (étapes) : 
    # Comparaison modèles KMeans et AgglomerativeClustering pour trouver le meilleur clustering 
    villages_labels = get_best_clustering(villages, N_STAGES)    # get_best_clustering() retourne pour chaque village les labels/étapes obtenus via la méthode ayant le meilleur score de silhouette et des clusters valides (au moins 2 villages par cluster)

    # Ajoute les labels/étapes au DataFrame villages et les re numérote de façon à avoir les étapes classées de façon croissante du Nord vers le Sud
    villages = add_villages_stage(villages_labels, villages)
    #plot_stages(villages, villages["stage"], "les différentes étapes")

    # mesure des parcours d'étapes : on cherche à optimiser le parcours et avoir le plus court
    stage_paths, stage_distances = best_paths(villages, N_STAGES)

    # Représentation de la carte de France (continent + Corse) avec les parcours numérotés et les distances et ordres des villes pour chaque étape
    print_roadbook(villages, stage_paths, stage_distances)
    plot_final_tour(villages, stage_paths, stage_distances)     


if __name__ == "__main__":
    main()