import math

def _haversine(lat1, lon1, lat2, lon2):
    """Calcule la distance entre 2 points GPS en km (ou calcul à vol d'oiseau).
    Arguments:
    lat1, lon1 -- latitude et longitude du 1er point, en degrés
    lat2, lon2 -- latitude et longitude du 2nd point, en degrés
    Returns:
    distance -- distance entre 2 points, en km
    """
    earth_radius = 6371
    lat1_rad, lon1_rad = math.radians(lat1), math.radians(lon1)
    lat2_rad, lon2_rad = math.radians(lat2), math.radians(lon2)
    delta_lat = lat2_rad - lat1_rad
    delta_lon = lon2_rad - lon1_rad
    a = math.sin(delta_lat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2
    distance = 2 * earth_radius * math.asin(math.sqrt(a))
    return distance


def _matrix_km(villages):
    """Calcule la distance entre 2 villages en kilometers. et le stocke dans une matrice carrée.
    Arguments:
    villages -- DataFrame des 120 villages avec coordonnées GPS
    Returns:
    distances  -- matrice carrée avec les distances entre 2 villages en km, La matrice est symétrique et de dimension 
    (n_villages, n_villages) et sa diagonale est nulle (distance d'un village à lui-même = 0)
    """
    coords = list(zip(villages["latitude"], villages["longitude"]))
    n_villages = len(coords)
    distances = [[0] * n_villages for _ in range(n_villages)]

    for i in range(n_villages):
        for j in range(i+1,n_villages):
            lat1, lon1 = coords[i]
            lat2, lon2 = coords[j]
            distances[i][j] = distances[j][i]= _haversine(lat1, lon1, lat2, lon2)
    return distances


def _path_distance(path, matrix_distances):
    """Calcule la distance totale entre les villages successifs du path (en km)
    Arguments:
    path -- liste des indices des villages dans l'ordre de calcul de distance à effectuer
    matrix_distances -- matrice des distances entre les villages
    Returns:
    total -- total de la distance entre les différents villages parcourus du 1er élément du path jsuqu'au dernier 
    """
    total = 0
    for i in range(len(path) - 1):
        total += matrix_distances[path[i]][path[i + 1]]    # récupère la distance entre 2 villages successifs dans path 
    return total


def _greedy_path(indices, start, matrix_distances):    # ou algorithme glouton
    """construit un chemin ouvert (village de début différent d'arrivée) en choisissant toujours la meilleure option locale à chaque étape.
    L'idée est : À chaque village, aller vers le village non visité le plus proche.
    Build an open path through the given villages with the nearest-neighbor heuristic.
    Arguments:
    indices -- liste des indices des villages appartenant à la même étape
    start -- indice du village de départ (appartenant à la liste indices)
    matrix_distances -- matrice des distances entre 2 villages (repérés par leur indice)
    Returns:
    path -- liste des indices des villages, classés par ordre de visite selon greedy path, en commençant par l'indice start
    """
    path = [start]      # path contient les différents villages visités dans l'ordre, avec parcours de proche en proche
                        # on commence par le village de départ : start 
                        # on va reconstituer ainsi la liste des villages visités dans l'ordre, 
                        # en partant du village de départ et en allant vers le village le plus proche à chaque étape
                        # on pourra ensuite calculer la distance totale du parcours avec la fonction path_distance(path)  
    
    unvisited = indices.copy()     
    unvisited.remove(start)     # unvisited = liste des villages restant à visiter, le village start ayant déjà été visité, on le retire
    while unvisited:            # tant qu'il reste des villages à visiter
        last = path[-1]         # on prend le dernier village visité
        next_village = min(unvisited, key=lambda x: matrix_distances[last][x])  #on cherche le village le plus proche du dernier visité
        path.append(next_village)       # on ajoute ce village au chemin
        unvisited.remove(next_village)  # on retire ce village de la liste des villages restant à visiter
    return path


def _two_opt(path, matrix_distances):
    """ Algo qui optimise un chemin ouvert, basé sur un théorème de géométrie dit que "si deux segments d'un parcours se croisent, 
    alors les décroiser raccourcit TOUJOURS le parcours (algo 2-opt).
    Pour chaque paire de positions `(i, j)` du parcours, on se demande "est-ce que retourner le segment entre `i` et `j` raccourcit 
    le tout ?". Si oui, on retourne. Et on recommence tant qu'on trouve des améliorations.
    Arguments:
    path -- liste des indices de villages, dans l'ordre de leur visite
    matrix_distances -- matrice des distances entre 2 villages (repérés par leur indice)

    Returns:
    path -- liste des indices ordonnés (mêmes villages, meilleur ordre - chemin le plus court)
    """
    path = path.copy()    # path contient les différents villages visités dans l'ordre
                    # on fait une copie de la liste path pour ne pas modifier l'originale passée comme argument
    
    improved = True    # on peut encore améliorer le parcours (on va chercher à réduire la distance totale du parcours en inversant des segments de villages)
    while improved:
        improved = False
        for i in range(1, len(path) - 2):
            for j in range(i + 1, len(path) - 1):
                # On calcule la distance actuelle des segments (i-1, i) et (j, j+1)
                current_distance = matrix_distances[path[i - 1]][path[i]] + matrix_distances[path[j]][path[j + 1]]
                # On calcule la distance si on inverse les segments (i, j)
                new_distance = matrix_distances[path[i - 1]][path[j]] + matrix_distances[path[i]][path[j + 1]]
                # Si la nouvelle distance est plus courte, on effectue l'inversion des segments, ie on réorganise l'ordre des villages dans le parcours
                if new_distance < current_distance:
                    path[i:j + 1] = reversed(path[i:j + 1])
                    improved = True     # on a trouvé une amélioration, on a donc inversé le sens du segment.
        # Une fois toutes les paires (i, j) parcourues, si on a effectué au moins une amélioration, on recommence depuis le début, sinon  on sort
    return path


def best_paths(villages, N_STAGES):
    """
    Pour chaque stage/étape, on va calculer le meilleur parcours et sa distance totale
    Arguments:
        villages -- DataFrame des 120 villages avec coordonnées GPS
    Returns:
        stage_paths -- liste des chemins les plus courts pour chacune des N_STAGES étapes (chemin = liste des indices des villes formant une étape)
        stage_distances -- liste des distances pour chacune des N_STAGES étape
    """
    villages = villages.copy()
    distances = _matrix_km(villages)
    stage_paths = {}
    stage_distances = {}

    for stage in range(1, N_STAGES + 1):            #pour chaque étape du Tour 2027, on va calculer le meilleur parcours et sa distance
        stage_indices = list(villages.index[villages["stage"] == stage])   #on filtre les villages appartenant à l'étape courante
        # On calcule le parcours initial avec l'algorithme glouton, on va tester tous les villages de l'étape comme point de départ pour trouver le meilleur parcours
        best_path = None            # meilleur chemin trouvé jusqu'à présent pour l'étape courante
        best_distance = float("inf")    # on initialise la meilleure distance à + inf
        for start_village in stage_indices:                             #on va tester tous les villages de l'étape comme point de départ pour trouver le meilleur parcours
            current_path = _greedy_path(stage_indices, start_village, distances)    # on calcule le parcours avec l'alogorithme glouton
            current_path = _two_opt(current_path, distances)           # on essaie d'améliorer le parcours avec l'algorithme 2-opt
            current_distance = _path_distance(current_path, distances)              # on calcule la distance totale de ce parcours
            if best_path is None or current_distance < best_distance:   # si le chemin est meilleur que le meilleur chemin trouvé jusqu'à présent, on le remplace
                best_path = current_path
                best_distance = current_distance

        # on a maintenant le meilleur parcours pour l'étape courante, le plus court en distance totale, 
        # on  stocke dans le dictionnaire stage_paths avec comme clé le numéro de l'étape et les villes dans l'ordre , et dans stage_distances la distance totale de ce parcours
        stage_paths[stage] = best_path
        stage_distances[stage] = best_distance
    return stage_paths, stage_distances

