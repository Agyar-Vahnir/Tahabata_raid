import numpy as np
import matplotlib.pyplot as plt
import csv
import check_people
import os
import clear_text

def people_attending(playerlist, logs, output_file, write=True):
    check = True
    for logfile in logs:
        print("Loading: " + logfile)
        if not check_people.check_new_people(playerlist,logfile):
            check = False
    if check:
        with open(playerlist) as playerdatabase:
            playersdb = csv.DictReader(playerdatabase, delimiter=";",skipinitialspace=True)
            playersdic = list(playersdb)
            # print(playersdic)
        logplayers = []
        for logfile in logs:
            with open(logfile) as newlog: 
                it_players = csv.reader(newlog,delimiter=" ",skipinitialspace=False)
                for p in it_players:
                    logplayers.append(p[0])
        logplayers = list(dict.fromkeys(logplayers))
        elyos = np.zeros(8)
        asmos = np.zeros(8)
        for player in playersdic:
            if player["Name"] in logplayers:
                if player["Faction"] == "Elyos":
                    if player["Class"] == "Assassin": elyos[0] += 1
                    elif  player["Class"] == "Ranger": elyos[1] += 1
                    elif  player["Class"] == "Gladiator": elyos[2] += 1
                    elif  player["Class"] == "Templar": elyos[3] += 1
                    elif  player["Class"] == "Spiritmaster": elyos[4] += 1
                    elif  player["Class"] == "Sorcerer": elyos[5] += 1
                    elif  player["Class"] == "Cleric": elyos[6] += 1
                    elif  player["Class"] == "Chanter": elyos[7] += 1
                elif player["Faction"] == "Asmo":
                    if player["Class"] == "Assassin": asmos[0] += 1
                    elif  player["Class"] == "Ranger": asmos[1] += 1
                    elif  player["Class"] == "Gladiator": asmos[2] += 1
                    elif  player["Class"] == "Templar": asmos[3] += 1
                    elif  player["Class"] == "Spiritmaster": asmos[4] += 1
                    elif  player["Class"] == "Sorcerer": asmos[5] += 1
                    elif  player["Class"] == "Cleric": asmos[6] += 1
                    elif  player["Class"] == "Chanter": asmos[7] += 1
        print("\n ATTENDING")
        attending =[elyos,asmos]
        faction = ["Elyos","Asmos"]
        classes = ["Assassin", "Ranger", "Gladiator", "Templar", "Spiritmaster", "Sorcerer", "Cleric", "Chanter"]
        if write :
            with open(output_file, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=';')
                for fac in range(2):
                    for clas in range(8):
                        writer.writerow([faction[fac], classes[clas], str(attending[fac][clas])[:-2]])
        n_elyos = sum(elyos)
        n_asmos = sum(asmos)
        return [n_elyos, n_asmos]
    else:
        print("PEOPLE MISSING")

RAID_ID = "08-06-U"
clear_text.process_files_in_folder(RAID_ID)

logs = []

for filename in os.listdir(RAID_ID):
    if filename.endswith('.txt'):
        print(RAID_ID + "/" + filename)
        logs.append(RAID_ID + "/" + filename)

people_attending("Players.csv",logs,RAID_ID + "/" + RAID_ID +"_players.csv")