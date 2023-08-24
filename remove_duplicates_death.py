import pandas as pd

def remove_duplicate_deaths(input_file, output_file, time_threshold_seconds=5):
    # Charger le fichier CSV dans un DataFrame pandas avec le point-virgule comme délimiteur
    df = pd.read_csv(input_file, sep=';', parse_dates=["Time"], infer_datetime_format=True)

    # Trier le DataFrame par le nom du joueur et la colonne de temps
    df.sort_values(by=["Name", "Time"], inplace=True)

    # Calculer la différence entre chaque horodatage et le suivant pour chaque joueur
    df["TimeDiff"] = df.groupby("Name")["Time"].diff()

    # Identifier les doublons basés sur le temps de mort et le nom du joueur en tenant compte du time_threshold_seconds
    duplicates = df["TimeDiff"] <= pd.to_timedelta(time_threshold_seconds, unit='s')

    # Garder uniquement la première occurrence des doublons pour chaque joueur
    df = df[~duplicates]

    # Supprimer la colonne temporaire utilisée pour le calcul des différences de temps
    df.drop(columns=["TimeDiff"], inplace=True)

    # Sauvegarder le DataFrame résultant dans un nouveau fichier CSV avec le point-virgule comme délimiteur
    # et en conservant le format d'entrée pour la colonne de temps
    df.to_csv(output_file, index=False, sep=';', date_format='%Y.%m.%d %H:%M:%S')




if __name__ == "__main__":
    # Chemin vers le fichier d'entrée contenant les morts des joueurs
    input_file = "07-30-U/Logs/deaths.csv"

    # Chemin vers le fichier de sortie sans les doublons de morts
    output_file = "07-30-U/Logs/death_no_dupe.csv"

    # Intervalle de temps en secondes pour considérer les morts comme des doublons
    time_threshold_seconds = 3

    # Appeler la fonction pour retirer les doublons de morts
    remove_duplicate_deaths(input_file, output_file, time_threshold_seconds)
