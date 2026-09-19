Projet_foot_2026 est réalisé à partir des mini-projets Data / IA proposés par le site ** Machine Learnia Ltd ** durant l'été 2026.

Guillaume Saint-Cirgue, Fondateur du site et Senior Data Scientist avec plus de 10 ans d’expérience dans les secteurs de la tech, l’aviation, la robotique, l’énergie, et les usines connectées nous fait partager ses connaissances dans le domaine de l’intelligence artificielle.

Au travers de projets partagés, guidés étape par étape, avec des explications claires, il aborde des sujets relatifs :
  * au clustering et algorithmes - Projet Tour de France
  * 
J'ai réalisé ce projet et ai décidé de le modifier librement en ajoutant mes propres commentaires et codes.

Environnement : 
1 . Utilisation de uv comme outil de gestion de l'environnement de Python : pour créer facilement un environnement virtuel,
décrire le projet et gérer mes dépendances via le fichier pyproject.toml 
2 . Présence d'un folder scripts permettant de générer une version exécutable .exe du projet dans le repertoire dist (simple .exe ou possibilité d'avoir un setup)

********************************************




On souhaite réaliser un tour de France à vélo (Corse inclue).
On a 120 villes à visiter, à séparer en 21 étapes.

Grace à un algorithme de clustering (ML non supervisé), on va déterminer quelles vont être nos étapes.
Dans les faits on va tester 2 algorithmes, les comparer et retenir le meilleur.

Les différentes villes sont contenues dans un fichier .csv, qu'on va charger dans un DataFrame.
On dispose pour chacune de leur coordonnées géographiques.

Pour déterminer nos 21 clusters / étapes, on va utilise successivement :
K-means : Méthode basées sur les centroïdes, Divise les données en k groupes autour de centres. Chaque point est rattaché au centre le plus proche.
CAH (AgglomerativeClustering) : Méthode de clustering hiérarchique (ie : on fusionne progressivement des groupes). Au départ, chaque observation est un cluster. l'algo cherche les deux clusters les plus proches, Il les fusionne. Puis il recommence jusqu'à obtenir le nombre de clusters demandé.

Les algorithmes de clustering utilise une distance entre observations (par défaut la distance euclidienne).
On va donc devoir convertir les latitudes/longitudes exprimés en degrés en km.

Une fois le choix de l'algorithme fait et les 21 étapes fixées, on va chercher à calculer les distances parcourues pendant chacune des étapes, et la distance totale. L'objectif est d'obtenir le chemin le plus court.
Là encore 2 algorithmes :
* Stratégie la plus intuitive - l'algorithme glouton : on va au village le plus proche non encore visité
* l'algorithme 2-opt. Son objectif est raccourcir un trajet en supprimant les croisements inutiles. Le 2-opt parcourt un trajet, choisit deux segments à la fois, vérifie si les remplacer par deux autres raccourcit la distance, et si c'est le cas, il inverse la portion intermédiaire du chemin. Il répète cette opération jusqu'à ce qu'aucun échange ne permette plus d'améliorer le trajet.


Pour aller plus loin, quelques idées à explorer :

- télécharger une liste d'autres villes de France (y compris Paris pour l'étape finale) et reprendre l'exercice de 0
- remplacer le vol d'oiseau par de vrais temps de trajet routiers, ou découvrir les solveurs professionnels comme OR-Tools de Google.
- Ajouter une regle dans l'algorithme de clustering, rejetant les étapes dont le chemin le plus court est > 200 km