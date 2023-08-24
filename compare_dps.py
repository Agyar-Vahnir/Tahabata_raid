import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def plot_damage_per_second(log_file, targets, gaps_start, gaps_end, xlim_start, xlim_end):
    # Lire les données depuis le fichier de logs CSV
    logs_df = pd.read_csv(log_file, delimiter=';')

    # Convertir la colonne 'Time' en objet datetime avec le format correct
    logs_df['Time'] = pd.to_datetime(logs_df['Time'], format="%Y.%m.%d %H:%M:%S")

    # Ajouter un décalage de temps de 17 secondes
    logs_df['Time'] = logs_df['Time'] + pd.Timedelta(seconds=-10)

    # Filtrer les dégâts pour les cibles spécifiées
    filtered_logs = logs_df[logs_df['Target'].str.strip().isin(targets)]

    # Regroupement croisé (pivot) pour obtenir la table des dégâts par seconde pour chaque Target et chaque Source
    damage_by_second = filtered_logs.pivot_table(index='Time', columns='Target', values='Damage', aggfunc='sum')

    # Remplir les valeurs manquantes avec zéro
    damage_by_second = damage_by_second.fillna(0)

    # Créer un graphique de barres séparé pour chaque cible en subplot
    fig, axs = plt.subplots(len(targets), 1, figsize=(12, 6 * len(targets)), sharex=True)
    if len(targets) == 1:
        axs = [axs]
    plt.xlabel('Time')
    plt.ylabel('DPS')

    for i, target in enumerate(targets):
        axs[i].bar(damage_by_second.index, damage_by_second[target], width=0.00001)
        axs[i].set_title(f'DPS on {target}')
        axs[i].grid(True)
        axs[i].xaxis.set_major_locator(mdates.MinuteLocator(interval=1))
        axs[i].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

        for gap_start, gap_end in zip(gaps_start, gaps_end):
            axs[i].axvspan(gap_start, gap_end, facecolor='red', alpha=0.2)

        # Ajouter la gestion des limites d'axe x (xlim)
        if xlim_start and xlim_end:
            axs[i].set_xlim(xlim_start, xlim_end)

    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    log_file = "08-09-U/Logs/Logs_REKI_logext.csv"
    targets = ['Veteran Dux']
    gaps_start = []
    gaps_end = []
    xlim_start = pd.to_datetime("2023-08-09 22:04:00")  # Remplacez par votre date de début pour xlim
    xlim_end = pd.to_datetime("2023-08-09 22:15:00")    # Remplacez par votre date de fin pour xlim

    gaps_start = pd.to_datetime(gaps_start, format="%Y-%m-%d %H:%M:%S")
    gaps_end = pd.to_datetime(gaps_end, format="%Y-%m-%d %H:%M:%S")

    plot_damage_per_second(log_file, targets, gaps_start, gaps_end, xlim_start, xlim_end)