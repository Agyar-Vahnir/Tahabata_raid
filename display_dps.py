import numpy as np
import matplotlib.pyplot as plt
import check_people
import csv

def average_of_lists(list_of_lists):
    total_sum = 0
    total_count = 0

    for sublist in list_of_lists:
        total_sum += sum(sublist)
        total_count += len(sublist)

    if total_count == 0:
        return 0

    return total_sum / total_count

def plot_dps(playerlist, logfile, show_asmos = True, show_elyos = True, display_mean = True, Data = "Damage"):
    if check_people.check_new_people(playerlist,logfile):
        with open(playerlist) as playerdatabase:
            playersdb = csv.DictReader(playerdatabase, delimiter=";",skipinitialspace=True)
            playersdic = list(playersdb)
            playerslist = []
            for p in playersdic:
                playerslist.append(p.values())
        with open(logfile) as newlog: 
            it_players = csv.reader(newlog,delimiter=" ",skipinitialspace=False)
            loadedlog = []
            for p_log in it_players:
                for p_db in playersdic:
                    if p_log[0] == p_db["Name"]:
                        loadedlog.append({"Name":p_log[0],"Class":p_db["Class"],"Faction":p_db["Faction"],"Damage":int(p_log[1]),"DPS":int(p_log[2])})
                        break
        print(loadedlog)

        # plt.figure()
        # plt.bar(range(len(bar_damage)),bar_damage)
        # plt.show()

        # Préparation des données pour le diagramme en barres
        factions = list(set(entry["Faction"] for entry in loadedlog))
        num_factions = len(factions)
        print("FACTIONS:" + str(num_factions))
        classes = list(set(entry["Class"] for entry in loadedlog))
        num_classes = len(classes)

        # Initialiser un dictionnaire pour stocker les valeurs de "Damage" par "Faction" et "Class"
        damage_data = {faction: {player_class: [] for player_class in classes} for faction in factions}

        for entry in loadedlog:
            damage = entry[Data]
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
            ax.set_ylabel(Data, FontSize=18)
            ax.set_title(Data + " by Class for "+ faction, FontSize = 25)
            ticks = [(indices[i][j]+indices[i][j+1])/2 for j in range(len(sorted_classes))]
            ax.set_xticks(ticks)
            ax.set_xticklabels(xlabels,fontsize = 12)
            ax.set_xlim([-1,max(indices[:][-1])+1])
        
        plt.tight_layout()
        plt.show()


    else:
        print("PEOPLE MISSING")

plot_dps("Players.csv","07-30-U/07-30-U-Stallari.txt", Data = "Damage")
plot_dps("Players.csv","07-30-U/07-30-U-Stallari.txt", Data = "DPS")
