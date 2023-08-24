import pandas as pd
import matplotlib.pyplot as plt

def count_deaths_by_faction(death_file, player_file, start_time, end_time):
    # Lire les données depuis les fichiers CSV
    deaths_df = pd.read_csv(death_file, delimiter=';')
    players_df = pd.read_csv(player_file, delimiter=';')

    # Convertir la colonne 'Time' en objet datetime avec le format correct
    deaths_df['Time'] = pd.to_datetime(deaths_df['Time'], format="%Y.%m.%d %H:%M:%S")

    # Filtrer les morts entre start_time et end_time
    deaths_between_dates = deaths_df[(deaths_df['Time'] >= start_time) & (deaths_df['Time'] <= end_time)]

    # Fusionner les données de morts et de joueurs en fonction du 'Name'
    merged_df = deaths_between_dates.merge(players_df, on='Name', how='left')

    # Regrouper par 'Faction' et compter le nombre de morts pour chaque faction
    faction_deaths_count = merged_df.groupby('Faction').size().reset_index(name='Deaths')

    return faction_deaths_count

def plot_faction_deaths(faction_deaths_count, start_time, end_time):
    # Créer un diagramme à barres empilées pour les deux factions
    fig, ax = plt.subplots(figsize=(8, 2))
    bar_height = 0.2

    print(faction_deaths_count)

    elyos_deaths = faction_deaths_count[faction_deaths_count['Faction'] == 'Elyos']['Deaths'].iloc[0]
    asmo_deaths = faction_deaths_count[faction_deaths_count['Faction'] == 'Asmo']['Deaths'].iloc[0]

    # Position des barres manuellement ajustée pour les mettre en face l'une de l'autre
    ax.barh('0', elyos_deaths, height=bar_height, color='green', label='Elyos', left=0)
    ax.barh('0', asmo_deaths, height=bar_height, color='blue', label='Asmo', left=-asmo_deaths)

    total_deaths = elyos_deaths + asmo_deaths

    # Afficher le nombre de morts à l'intérieur de chaque partie de la barre
    ax.text(elyos_deaths-10, '0', str(elyos_deaths), ha='right', va='center', fontweight='bold', fontsize=20, color='black')
    ax.text(10, '0', "Elyos", ha='left', va='center', fontweight='bold', fontsize=20, color='black')
    ax.text(-asmo_deaths+10, '0', str(asmo_deaths), ha='left', va='center', fontweight='bold', fontsize=20, color='black')
    ax.text(-10, '0', "Asmos", ha='right', va='center', fontweight='bold', fontsize=20, color='black')

    ax.set_xlim(-asmo_deaths-5, elyos_deaths + 5) # Ajuster la limite de l'axe x pour que les barres soient centrées
    ax.set_xlabel('Number of Deaths')
    ax.set_title('Players deaths by faction between ' + str(start_time) + " and " + str(end_time))

    # Masquer les graduations de l'axe y pour avoir un affichage plus propre
    ax.get_yaxis().set_visible(False)
    
    plt.show()


if __name__ == "__main__":
    death_file = "08-09-U/Logs/fichiers_fusionnes_sans_doublons.csv"
    player_file = "Players.csv"
    start_time = pd.to_datetime("2023-08-09 21:00:00", format="%Y.%m.%d %H:%M:%S")
    end_time = pd.to_datetime("2023-08-09 22:25:00", format="%Y.%m.%d %H:%M:%S")

    faction_deaths_count = count_deaths_by_faction(death_file, player_file, start_time, end_time)
    print(faction_deaths_count)

    plot_faction_deaths(faction_deaths_count, start_time, end_time)
