import numpy as np
import matplotlib.pyplot as plt
import csv
import clear_text

def check_new_people(playerlist, logfile):
    """Function to check if all players recorded are already in the database"""

    ## Load the player database
    with open(playerlist) as playerdatabase:
        it_players = csv.reader(playerdatabase,delimiter=";",skipinitialspace=True)
        formerplayers = []
        for p in it_players:
            formerplayers.append(p[0])
    
    ## Load the players from the log file
    with open(logfile) as newlog:
        log = csv.reader(newlog, delimiter=" ", skipinitialspace=True)
        next(log)
        logplayers =  []
        for p in log:
            logplayers.append(p[0])

    ## Make the list of the players in the log file but not in the database
    newplayer = []
    for player in logplayers:
        if player not in formerplayers:
            newplayer.append(player)
    print(newplayer)
    return (newplayer==[])


def add_new_players(playerlist):
    """A function to add new players to the database from the dedicated files"""
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
        with open("CLASSFACTION/" + files[i] +".txt") as newplayers:
            newplayer = csv.reader(newplayers, delimiter=" ", lineterminator=",")
            for p in newplayer:
                if p[0] not in(formerplayers):
                    playerslist.append([p[0],faction[i%2],classe[int(i/2)]])
    with open(playerlist, 'w', newline='') as newlist:
        writer = csv.writer(newlist, delimiter=';')
        writer.writerow(["Name","Faction","Class"])
        writer.writerows(playerslist)

clear_text.process_files_in_folder("CLASSFACTION")

add_new_players("Players.csv")


