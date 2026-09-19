import math
from pathlib import Path
import sys

import pandas as pd


def _resource_path(relative_path: str) -> Path:
    """
    Retourne le chemin absolu vers une ressource de l'application.

    Fonctionne :
    - en développement avec Python ;
    - avec un exécutable créé par PyInstaller.
    """

    if getattr(sys, "frozen", False):
        # Exécution depuis l'EXE PyInstaller
        base_path = Path(sys._MEIPASS)
    else:
        # Exécution depuis le projet Python
        base_path = Path(__file__).resolve().parent.parent.parent

    return base_path / relative_path


def load_villages():
    """A partir d'un fichier .csv, charge dans un dataFrame les 120 villages du Tour 

    Arguments:
    path -- localisation du fichier .csv
    Returns:
    villages -- DataFrame avec les colonnes village, departement, latitude, longitude
    """
    try:
        path_data = _resource_path("data/villages_2027.csv")
        villages = pd.read_csv(path_data, dtype={"departement": str})   #le département est présent sous la forme 45, 33, ... dans le fichier .csv.
                                    # On utilise le dtype pour forcer à l'interpréter comme un string, ainsi les dép. 01, 02 seront mis sur 2 caractères
                                    # et pas interprétés comme des numériques 1, 2, ...
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Le fichier '{path_data}' est introuvable. Il est fourni avec le projet : "
            "vérifie que tu exécutes bien le notebook depuis le dossier Projet_03."
        ) from None
    # si le fichier n'est pas trouvé pendant le read, l'exception est levée. le except l'intercepte et le raise léve une nouvelle exception.
    # si rien au-dessus pour la capturer, le message s'affiche et le programme s'arrête. from None sert à masquer le message généré par le except.
    return villages


def add_villages_latlon_km(villages):
    """Transforme latitude et longitude de degrés en kilometres.

    Arguments:
    villages -- DataFrame avec colonnes lat et lon en degrés
    Returns:
    villages -- DataFrame avec 2 nouvelles colonnes lat et lon en km (x_km, y_km)
    """
    # On va créer 2 nouvelles colonnes dans le dataframe villages, x_km et y_km, qui contiennent les coordonnées en km des villages, 
    # par rapport à un point de référence (latitude : latitude moyenne de tous les villages, longitude : 0).    
    villages = villages.copy()
    lat_mean = villages["latitude"].mean()
    #print(f"Latitude moyenne de nos villages : {lat_mean:.2f}° (1 degré de longitude y vaut {111 * math.cos(math.radians(lat_mean)):.0f} km)")
    villages["y_km"] = villages["latitude"] * 111
    villages["x_km"] = villages["longitude"] * 111 * math.cos(math.radians(lat_mean))
    return villages


def add_villages_stage(labels, villages):
    """
    Pour chacun des villages, ajout de l'étape à laquelle il est associé, et pn ordonne les étapes par ordre croissant 
    en partant du nord vers le sud, et on commence la numérotation à partir de 1 (à 21)
    Argument:
    labels -- DataFrame contenant les étapes de rattachement de chacun des villages
    villages -- DataFrame 
    """
    villages = villages.copy()
    villages["stage"] = labels
    villages = villages.copy()
    # on renumérote les étapes du nord au sud : plus lisible qu'une numérotation arbitraire
    # villages.groupby("stage")["latitude"].mean().sort_values(ascending=False) => dataframe avec stage en index et moyenne des latitudes par stage décroissante (du nord au sud)
    stage_order = villages.groupby("stage")["latitude"].mean().sort_values(ascending=False).index

    # dans stage_order on va avoir un index 0, le stage correspondant à l'étape le plus au nord (exemple : 3), 
    # on va renuméroter le 3 en 1 (0+1, étape 0 ne voulant rien dire)
    villages["stage"] = villages["stage"].map({old: new + 1 for new, old in enumerate(stage_order)})
    return villages


