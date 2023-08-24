import pandas as pd
from datetime import datetime

RAID_ID = "08-09-U"
files = ["Logs_PAAP_logext.csv", "Logs_BARTO_logext.csv", "Logs_REKI_logext.csv"]
for i in range(len(files)):
    files[i] = RAID_ID + "/Logs/" + files[i]

# Chemins vers vos fichiers CSV
file_paths = files.copy()  # Remplacez par les chemins de vos fichiers

# Dates de début et de fin pour la période que vous souhaitez analyser
start_date = "2023-08-09 21:30:00"  # Remplacez par votre date de début
end_date = "2023-08-09 22:35:00"    # Remplacez par votre date de fin

# Liste pour stocker les noms de sources de dégâts
sources = []

# Boucle à travers chaque fichier
for file_path in file_paths:
    df = pd.read_csv(file_path, sep=';')  # Assurez-vous que le séparateur est correct
    df['Time'] = pd.to_datetime(df['Time'], format='%Y.%m.%d %H:%M:%S')

    # Filtrer les lignes entre les dates spécifiées
    filtered_df = df[(df['Time'] >= start_date) & (df['Time'] <= end_date)]

    # Ajouter les noms de sources de dégâts à la liste
    sources.extend(filtered_df['Source'].unique())

# Convertir la liste en un DataFrame
sources_df = pd.DataFrame({'Source': sources})

# Retirer les doublons
sources_df.drop_duplicates(subset='Source', keep='first', inplace=True)

# Exclure la source "UNASSIGNED"
sources_df = sources_df[sources_df['Source'] != 'UNASSIGNED']

# Enregistrer le DataFrame dans un fichier CSV
sources_df.to_csv(RAID_ID + "/Logs/sources_de_degats.csv", index=False, sep=';')

print("Noms de sources de dégâts enregistrés dans 'sources_de_degats.csv'.")
