import pandas as pd
from datetime import datetime, timedelta

def convert_to_timestamp(time_value):
    # Vérifier si la valeur est déjà un horodatage numérique
    if pd.isna(time_value):
        return float('nan')

    try:
        # Convertir la valeur de temps en timestamp UNIX si c'est une chaîne de caractères
        return pd.to_datetime(time_value, format='%Y.%m.%d %H:%M:%S')
    except ValueError:
        # Gérer les cas où la valeur ne peut pas être convertie en horodatage
        return float('nan')

def synchronize_time(file_paths, output_file, output_death, time_shifts):
    n_files = len(file_paths)
    time_shift = []
    for shift in time_shifts:
        # Ajouter " seconds" au format timeshift pour le rendre compatible avec pd.to_timedelta
        time_shift.append(pd.to_timedelta(shift + " seconds"))
    print(time_shift)
    # Lire le premier fichier et convertir les horodatages en format datetime
    df = pd.read_csv(file_paths[0], sep=';', index_col=False)
    df["Time"] = df["Time"].apply(convert_to_timestamp)
    death_df = pd.read_csv(death_paths[0], sep=';', index_col=False)
    death_df["Time"] = death_df["Time"].apply(convert_to_timestamp)

    # Parcourir les autres fichiers pour synchroniser les temps
    for i in range(1,n_files):
        file_path = file_paths[i]
        death_path = death_paths[i]
        # Lire le fichier et convertir les horodatages en format datetime
        df_next = pd.read_csv(file_path, sep=';', index_col=False)
        df_next["Time"] = df_next["Time"].apply(convert_to_timestamp)
        death_df_next = pd.read_csv(death_path, sep=';', index_col=False)
        death_df_next["Time"] = death_df_next["Time"].apply(convert_to_timestamp)

        # Trouver le dernier coup porté à "Veteran Stallari" dans le fichier actuel
        last_stallari_time_next = df_next[df_next["Target"] == 'Veteran Stallari']["Time"].max()
        last_stallari_time = df[df["Target"] == 'Veteran Stallari']["Time"].max()

        # Calculer le décalage entre les derniers coups portés à "Veteran Stallari" des deux fichiers
        time_offset = last_stallari_time - last_stallari_time_next
        time_offset = time_shift[i]
        print(time_offset)

        # Appliquer le décalage à tous les horodatages du fichier actuel
        df_next["Time"] = df_next["Time"] - time_offset
        death_df_next["Time"] = death_df_next["Time"] - time_offset

        # Mettre à jour le DataFrame global avec les données du fichier actuel
        df = pd.concat([df, df_next], ignore_index=True)
        death_df = pd.concat([death_df, death_df_next], ignore_index=True)

    # Trouver le temps de référence pour synchroniser le premier coup porté sur "Veteran Dux" à l'heure souhaitée
    first_dux_time = df[df["Target"] == 'Veteran Dux']["Time"].min()
    reference_time = pd.to_datetime("2023.07.30 22:05:00", format='%Y.%m.%d %H:%M:%S')
    time_offset_last = reference_time - first_dux_time
    print(time_offset_last)

    # Appliquer le dernier décalage à tous les horodatages du DataFrame global
    df["Time"] = df["Time"] + time_offset_last
    death_df["Time"] = death_df["Time"] + time_offset_last

    # Trier par ordre chronologique en utilisant le fichier avec le log le plus ancien comme référence
    df.sort_values(by=['Time'], ignore_index=True, inplace=True)
    death_df.sort_values(by=['Time'], ignore_index=True, inplace=True)

    # Convertir les horodatages de nouveau en format datetime
    df["Time"] = df["Time"].dt.strftime('%Y.%m.%d %H:%M:%S')
    death_df["Time"] = death_df["Time"].dt.strftime('%Y.%m.%d %H:%M:%S')

    # Sauvegarder le résultat dans un fichier CSV avec le header approprié
    df.to_csv(output_file, sep=';', index=False)
    death_df.to_csv(output_death, sep=';', index=False)

if __name__ == "__main__":
    # Liste des chemins de fichiers CSV que vous souhaitez fusionner
    file_paths = ["07-30-U/Logs/0730UPAAP_logext.csv", "07-30-U/Logs/0730UVERDA_logext.csv", "07-30-U/Logs/0730UBARTO_logext.csv"]
    death_paths = ["07-30-U/Logs/0730UPAAP_logdeath.csv", "07-30-U/Logs/0730UVERDA_logdeath.csv", "07-30-U/Logs/0730UBARTO_logdeath.csv"]
    time_shift = ["0","64","65"]
    
    # Chemin vers le fichier de sortie
    output_file = "07-30-U/Logs/total.csv"
    output_death = "07-30-U/Logs/deaths.csv"
    
    # Appeler la fonction pour synchroniser les temps et fusionner les fichiers
    synchronize_time(file_paths, output_file, output_death, time_shift)
