import pandas as pd
from datetime import timedelta

RAID_ID = "08-09-U"
files = ["Logs_PAAP_logdeath.csv","Logs_BARTO_logdeath.csv","Logs_REKI_logdeath.csv"]
for i in range(len(files)):
    files[i] = RAID_ID + "/Logs/" + files[i]

# Liste des noms de fichiers CSV à fusionner avec leur décalage respectif en secondes
file_offsets = [(files[0], 0), (files[1], 9), (files[2], 6)]

# Initialisation du DataFrame avec le premier fichier
first_file_name, first_offset = file_offsets[0]
merged_df = pd.read_csv(first_file_name, sep=';')  # Spécifier le délimiteur point virgule
merged_df['Time'] = pd.to_datetime(merged_df['Time'], format='%Y.%m.%d %H:%M:%S') - timedelta(seconds=first_offset)

# Boucle pour fusionner les fichiers restants avec décalage
for file_name, offset in file_offsets[1:]:
    df = pd.read_csv(file_name, sep=';')  # Spécifier le délimiteur point virgule
    df['Time'] = pd.to_datetime(df['Time'], format='%Y.%m.%d %H:%M:%S') - timedelta(seconds=offset)
    merged_df = pd.concat([merged_df, df])

# Tri par date/heure
merged_df.sort_values(by=['Name', 'Time'], inplace=True)

# Supprimer les doublons selon le critère spécifié
cleaned_rows = []
previous_row = None

for index, row in merged_df.iterrows():
    if previous_row is None or (row['Name'] != previous_row['Name'] or (row['Time'] - previous_row['Time']) > timedelta(seconds=3)):
        cleaned_rows.append(row)
    if index % 20 == 0:
        print(index)
    previous_row = row

# Créer un DataFrame propre avec les lignes non dupliquées
filtered_df = pd.DataFrame(cleaned_rows)

# Sauvegarde du résultat dans un nouveau fichier CSV avec le délimiteur point virgule et le format de date d'entrée
filtered_df['Time'] = filtered_df['Time'].dt.strftime('%Y.%m.%d %H:%M:%S')  # Reconvertir le format de date
filtered_df.to_csv(RAID_ID + "/Logs/" + "fichiers_fusionnes_sans_doublons.csv", index=False, sep=';', date_format='%Y.%m.%d %H:%M:%S')

print("Fusion, synchronisation et suppression des doublons terminées. Résultats sauvegardés dans 'fichiers_fusionnes_sans_doublons.csv'.")
