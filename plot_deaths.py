import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def plot_faction_deaths(player_file, death_file, start_time=None, end_time=None):
    # Lire les données des joueurs et des morts depuis les fichiers CSV
    players_df = pd.read_csv(player_file, delimiter=';')
    deaths_df = pd.read_csv(death_file, delimiter=';')

    # Convertir la colonne 'Time' en objet datetime avec le format correct
    deaths_df['Time'] = pd.to_datetime(deaths_df['Time'], format="%Y.%m.%d %H:%M:%S")

    # Fusionner les DataFrames pour avoir les informations de mort pour chaque joueur
    merged_df = players_df.merge(deaths_df, on='Name', how='left')

    # Filtrer les morts par faction
    elyos_deaths = merged_df[merged_df['Faction'] == 'Elyos']
    asmo_deaths = merged_df[merged_df['Faction'] == 'Asmo']

    # Filter deaths within the specified time range (if provided)
    if start_time and end_time:
        elyos_deaths = elyos_deaths[(elyos_deaths['Time'] >= start_time) & (elyos_deaths['Time'] <= end_time)]
        asmo_deaths = asmo_deaths[(asmo_deaths['Time'] >= start_time) & (asmo_deaths['Time'] <= end_time)]

    # Compter les morts par tranche de 5 secondes
    elyos_deaths_count = elyos_deaths.resample('5S', on='Time').size()
    asmo_deaths_count = asmo_deaths.resample('5S', on='Time').size()

    # Tracer le diagramme de barres
    fig, ax = plt.subplots(figsize=(12, 6))

    # Définir la largeur des barres en millisecondes (1 seconde = 1000 millisecondes)
    bar_width = 0.0001

    ax.bar(elyos_deaths_count.index, elyos_deaths_count, width=bar_width, color='green', label='Elyos')
    ax.bar(asmo_deaths_count.index, -asmo_deaths_count, width=bar_width, color='blue', label='Asmo')

    ax.set_xlabel('Time (HH:MM:SS)')
    ax.set_ylabel('Number of deaths')
    ax.set_title('Players deaths by faction (slices of 5 seconds)')
    ax.legend()

    # Ajouter les axes
    ax.axhline(y=0, color='black', linewidth=0.5)  # Axe horizontal à y=0

    # Formater l'axe des abscisses pour afficher l'heure, les minutes et les secondes seulement
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))

    plt.xticks(rotation=45)
    plt.show()

if __name__ == "__main__":
    player_file = "Players.csv"
    death_file = "08-09-U/Logs/fichiers_fusionnes_sans_doublons.csv"
    start_time = pd.to_datetime("2023-08-09 21:30:00", format="%Y-%m-%d %H:%M:%S")
    end_time = pd.to_datetime("2023-08-09 22:30:00", format="%Y-%m-%d %H:%M:%S")
    plot_faction_deaths(player_file, death_file, start_time, end_time)
