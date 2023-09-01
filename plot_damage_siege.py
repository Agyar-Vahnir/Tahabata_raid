import pandas as pd
import numpy as np
import manage_siege_weapons
import check_people
import matplotlib.pyplot as plt
from datetime import datetime
def average_of_lists(list_of_lists):
    total_sum = 0
    total_count = 0

    for sublist in list_of_lists:
        total_sum += sum(sublist)
        total_count += len(sublist)

    if total_count == 0:
        return 0

    return total_sum / total_count

def plot_damage(playerlist, log, targets, start, end, display_mean = True):
    log_df = pd.read_csv(log, sep=",")
    player_df = pd.read_csv(playerlist, sep=';')
    target_df = pd.DataFrame(targets, columns=["Target"])

    log_df["DateTime"] = pd.to_datetime(log_df["DateTime"])
    log_df = log_df[(log_df["DateTime"] > start) & (log_df["DateTime"] < end)]
    log_df = log_df.rename(columns={"Source":"Name"})
    log_df = log_df.merge(target_df,how='inner',on="Target")
    log_df = log_df.merge(player_df, on="Name", how="inner")
    log_df = manage_siege_weapons.filter_siege_weapons(log_df)
    log_df = log_df.drop(columns=["DateTime","Skill","Heal","Target"])
    
    log_df = log_df.groupby(by=['Name','Faction','Class'])['Damage'].sum().reset_index()

    log_df = log_df.drop(index=log_df[(log_df["Class"] == "Siege") & (log_df["Damage"] < 1000)].index)

    factions = list(dict.fromkeys(log_df["Faction"].tolist())) 
    num_factions = len(factions)
    classes = list(dict.fromkeys(log_df["Class"].tolist())) 
    num_classes = len(classes)


    # Initialiser un dictionnaire pour stocker les valeurs de "Damage" par "Faction" et "Class"
    damage_data = {faction: {player_class: [] for player_class in classes} for faction in factions}
    log_dict = log_df.to_dict("records")

    for entry in log_dict:
        damage = entry["Damage"]
        player_class = entry["Class"]
        faction = entry["Faction"]
        damage_data[faction][player_class].append(damage)
    for faction in factions:
        for classe in classes:
            damage_data[faction][classe].sort(reverse = True)
    # Calculer les moyennes pour chaque tableau de valeurs (Class)
    average_damage_by_class = {
        player_class: np.mean([damage for faction_data in damage_data.values() for damage in faction_data[player_class]])
        for player_class in classes
    }

    # Trier le dictionnaire damage_data en utilisant les moyennes de Damage par Class
    sorted_classes = sorted(average_damage_by_class, key=average_damage_by_class.get, reverse=True)
    damage_data_sorted = {faction: {player_class: damage_data[faction][player_class] for player_class in sorted_classes} for faction in factions}

    # Création du diagramme en barres avec sous-diagrammes pour chaque "Faction"
    class_colors = {
        "Siege": "#888888",
        "Assassin": "#006400",      # Vert foncé
        "Ranger": "#008000",        # Vert clair
        "Cleric": "#FFD700",        # Jaune doré
        "Chanter": "#FFA500",       # Jaune orangé
        "Gladiator": "#4169E1",     # Bleu royal
        "Templar": "#00008B",       # Bleu dragon
        "Spiritmaster": "#8B008B",  # Violet tirant sur le magenta
        "Sorcerer": "#8A2BE2"       # Violet tirant sur le bleu
    }
    class_colors_mean = {
        "Siege": "#AAAAAA",
        "Assassin": "#004000",      # Vert foncé (légèrement plus sombre)
        "Ranger": "#006400",        # Vert clair (légèrement plus sombre)
        "Cleric": "#DAA520",        # Jaune doré (légèrement plus sombre)
        "Chanter": "#FF8C00",       # Jaune orangé (légèrement plus sombre)
        "Gladiator": "#2E4B8F",     # Bleu royal (légèrement plus sombre)
        "Templar": "#00004B",       # Bleu dragon (légèrement plus sombre)
        "Spiritmaster": "#6A006A",  # Violet tirant sur le magenta (légèrement plus sombre)
        "Sorcerer": "#641E9E"       # Violet tirant sur le bleu (légèrement plus sombre)
}

    x = np.arange(num_classes)
    bar_width = 0.2
    indices = []
    for faction in damage_data_sorted.values():
        ind = [0]
        for classe in faction.values():
            ind.append(ind[-1]+len(classe))
        indices.append(ind)
    if num_factions == 1:
        fig, ax = plt.subplots(figsize=(8, 5), sharex=True)
        axs = [ax]  # Convertir l'axe unique en une liste pour faciliter l'itération
    else:
        fig, axs = plt.subplots(nrows=num_factions, ncols=1, figsize=(8, 5*num_factions), sharex=True)

    x = np.arange(num_classes)
    bar_width = 0.2

    for i, (faction, faction_data) in enumerate(damage_data_sorted.items()):
        ax = axs[i]
        index_values = indices[i]  # Récupérer les indices spécifiques pour cette faction
        xlabels = []
        plots = []
        legends = []
        all_dmg =[]
        for j, player_class in enumerate(sorted_classes):
            class_data = faction_data[player_class]
            all_dmg.append(class_data)
            xlabels.append(player_class + "s: " + str(len(class_data)))

            ax.bar(range(indices[i][j],indices[i][j+1]), class_data, label=player_class, width = 1, color=class_colors[player_class])
            if display_mean:
                plot = ax.plot([indices[i][j],indices[i][j+1]-0.5], [average_damage_by_class[player_class],average_damage_by_class[player_class]],'--', color=class_colors_mean[player_class], LineWidth=1.75)
                plots.append(plot)
                legends.append(player_class + " avg: " + str(int(average_damage_by_class[player_class]*100)/100))
        total_avg = average_of_lists(all_dmg)
        if display_mean:
            ax.plot([indices[i][0],indices[i][-1]],[total_avg,total_avg],'--', color="red", LineWidth=2.5)
            legends.append("Total avg: " + str(int(total_avg*100)/100))
            ax.legend(legends)
        ax.set_ylabel("Damage", FontSize=18)
        ax.set_title("Damage by Class for "+ faction, FontSize = 25)
        ticks = [(indices[i][j]+indices[i][j+1])/2 for j in range(len(sorted_classes))]
        ax.set_xticks(ticks)
        ax.set_xticklabels(xlabels,fontsize = 12)
        ax.set_xlim([-1,max(indices[:][-1])+1])
    
    plt.tight_layout()
    plt.show()





playerlist = "C:/Users/Salto/Desktop/RAID ASMO/Players.csv"
log = "C:/Users/Salto/Documents/RAIDS/08-30-GI/log_unfiltered.csv"
targets = ["Balaur Castle Gate"]

start = "2023-08-30 22:08:00"
end = "2023-08-30 22:30:00"

start = datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
end = datetime.strptime(end, "%Y-%m-%d %H:%M:%S")


plot_damage(playerlist,log,targets, start, end)




