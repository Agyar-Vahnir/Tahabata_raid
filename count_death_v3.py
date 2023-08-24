import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def count_deaths_by_player(death_file, player_file, start_time, end_time, player_names=None):
    deaths_df = pd.read_csv(death_file, delimiter=';')
    players_df = pd.read_csv(player_file, delimiter=';')

    deaths_df['Time'] = pd.to_datetime(deaths_df['Time'], format="%Y.%m.%d %H:%M:%S")

    deaths_between_dates = deaths_df[(deaths_df['Time'] >= start_time) & (deaths_df['Time'] <= end_time)]
    
    if player_names is not None:
        deaths_between_dates = deaths_between_dates[deaths_between_dates['Name'].isin(player_names)]

    merged_df = deaths_between_dates.merge(players_df, on='Name', how='left')

    player_deaths_count = merged_df.groupby(['Faction', 'Name']).size().reset_index(name='Deaths')

    return player_deaths_count

def plot_player_deaths(player_deaths_count, max_display=None, leaders=[]):
    fig, ax = plt.subplots(figsize=(8, 6))
    bar_height = 0.2
    space_ratio = 1.2

    elyos_players = player_deaths_count[player_deaths_count['Faction'] == 'Elyos'].sort_values(by='Deaths', ascending=False)
    asmo_players = player_deaths_count[player_deaths_count['Faction'] == 'Asmo'].sort_values(by='Deaths', ascending=False)

    if max_display is not None:
        elyos_players = elyos_players.head(max_display)
        asmo_players = asmo_players.head(max_display)

    if not elyos_players.empty:
        ax.barh(-np.multiply(range(len(elyos_players)), bar_height*space_ratio), elyos_players['Deaths'], height=bar_height, color='green', label='Elyos')
        elyos = elyos_players.to_dict(orient='records')
        for indice in range(len(elyos)):
            player = elyos[indice]
            name = player['Name']
            deaths = player['Deaths']
            ax.text(deaths-0.2, -indice*bar_height*space_ratio, str(deaths), ha='right', va='center', fontweight='bold', fontsize=15, color='black')
            ax.text(0.2, -indice*bar_height*space_ratio, name, ha='left', va='center', fontweight='bold', fontsize=15, color='black')
    
    if not asmo_players.empty:
        ax.barh(-np.multiply(range(len(asmo_players)), bar_height*space_ratio), -asmo_players['Deaths'], height=bar_height, color='blue', label='Asmo')
        asmos = asmo_players.to_dict(orient='records')
        for indice in range(len(asmos)):
            player = asmos[indice]
            name = player['Name']
            deaths = player['Deaths']
            ax.text(-deaths+0.2, -indice*bar_height*space_ratio, str(deaths), ha='right', va='center', fontweight='bold', fontsize=15, color='black')
            ax.text(-0.2, -indice*bar_height*space_ratio, name, ha='right', va='center', fontweight='bold', fontsize=15, color='black')
    
    ax.set_xlabel('Number of Deaths')
    ax.set_yticks([])
    ax.set_title('Player deaths by faction between ' + str(start_time) + ' and ' + str(end_time))

    ax.legend()
    
    plt.show()

if __name__ == "__main__":
    death_file = "08-09-U/Logs/fichiers_fusionnes_sans_doublons.csv"
    player_file = "Players.csv"
    start_time = pd.to_datetime("2023-08-09 21:00:00", format="%Y-%m-%d %H:%M:%S")
    end_time = pd.to_datetime("2023-08-09 22:25:00", format="%Y-%m-%d %H:%M:%S")

    players_to_count = ['Citria', 'Paaprika', 'Divin', 'Lavandain']  # Replace with the player names you want to count deaths for
    players_to_count = []  # Replace with the player names you want to count deaths for
    leaders = ["Paaprika","Citria"]
    players_to_display = 20  # Replace with the maximum number of players you want to display
    if not players_to_count or players_to_count == []:
        players_to_count = None  # Set to None to count all players

    player_deaths_count = count_deaths_by_player(death_file, player_file, start_time, end_time, player_names=players_to_count)
    print(player_deaths_count)

    plot_player_deaths(player_deaths_count, max_display=players_to_display, leaders=leaders)
