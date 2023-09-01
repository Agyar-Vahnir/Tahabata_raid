import numpy as np
import matplotlib.pyplot as plt
import csv
import clear_text
import pandas as pd

def check_new_people(playerlist, logfile):
    """Function to check if all players recorded are already in the database"""

    ## Load the player database
    player_df = pd.read_csv(playerlist,delimiter=";",skipinitialspace=True)
    player_df = player_df["Name"]
    print(player_df)
    
    ## Load the players from the log file
    log_df = pd.read_csv(logfile,delimiter=" ",skipinitialspace=True, header=None)
    print(log_df)
    log_df = log_df.iloc(axis=1)[0]
    print(log_df)


    ## Make the list of the players in the log file but not in the database
    newplayer = log_df[~log_df.isin(player_df)]
    print(newplayer)
    return (newplayer.empty)


def add_new_players(playerlist):
    """A function to add new players to the database from the dedicated files"""
    clear_text.process_files_in_folder("C:/Users/Salto/Desktop/RAID ASMO GIT/CLASSFACTION")
    classe = ["Assassin","Ranger","Sorcerer","Spiritmaster","Gladiator","Templar","Cleric","Chanter"]
    faction = ["Elyos","Asmo"]
    files = ["ELYOSASSA","ASMOSASSA","ELYOSRANG","ASMOSRANG","ELYOSSORC","ASMOSSORC","ELYOSSPIR","ASMOSSPIR","ELYOSGLAD","ASMOSGLAD","ELYOSTEMP","ASMOSTEMP","ELYOSCLER","ASMOSCLER","ELYOSCHAN","ASMOSCHAN"]
    with open(playerlist) as playerdatabase:
        it_players = csv.reader(playerdatabase,delimiter=";",skipinitialspace=True)
        formerplayers = []
        playerslist = []
        next(it_players)
        for p in it_players:
            playerslist.append(p)
            formerplayers.append(p[0])
    for i in range(16):
        with open("C:/Users/Salto/Desktop/RAID ASMO GIT/CLASSFACTION/" + files[i] +".txt") as newplayers:
            newplayer = csv.reader(newplayers, delimiter=" ", lineterminator=",")
            for p in newplayer:
                if p[0] not in(formerplayers):
                    playerslist.append([p[0],faction[i%2],classe[int(i/2)]])
    with open(playerlist, 'w', newline='') as newlist:
        writer = csv.writer(newlist, delimiter=';')
        writer.writerow(["Name","Faction","Class"])
        writer.writerows(playerslist)
