import csv
from datetime import datetime
import os

def transform_to_datetime(instant_str):
    try:
        # Parse the input string to a datetime object
        dt_object = datetime.strptime(instant_str, "%d.%m.%Y %H:%M:%S")

        # Convert the datetime object to the desired format
        formatted_dt_str = dt_object.strftime("%Y.%m.%d %H:%M:%S")

        return formatted_dt_str

    except ValueError:
        # If the input string is not in the correct format, handle the error
        raise ValueError("Invalid input format. Please provide the date in 'dd.mm.yyyy hh:mm:ss' format.")


def compile_logs(log_list,output_file,death_file):
    csvfile = open(output_file, 'w', newline='')
    writer_output = csv.writer(csvfile, delimiter=';')
    writer_output.writerow(["Source","Time","Skill","Damage","Heal","Target"])
    csvfile = open(death_file, 'w', newline='')
    writer_death = csv.writer(csvfile, delimiter=';')
    writer_death.writerow(["Name","Time"])
    for log_file in log_list:
        log = open(log_file)
        reader = csv.reader(log, delimiter = "\t")
        count = 0
        for line in reader:
            if line != []:
                if line[0] != '':
                    current_char = line[0].split(' ',1)[0]
                else:
                    log_line = line.copy()
                    log_line[0] = current_char
                    if current_char == "UNASSIGNED":
                        source = log_line[0]
                        time = transform_to_datetime(log_line[1])
                        skill = log_line[2]
                        if log_line[4] != "":
                            damage = int(log_line[4].replace(".",""))
                        else:
                            damage = 0
                        if log_line[5] != "":
                            heal = int(log_line[5].replace(".",""))
                        else:
                            heal = 0
                        target = log_line[6]
                        writer_output.writerow([source,time,skill,damage,heal,target])
                    elif log_line[2][0] != "[":
                        source = log_line[0]
                        time = transform_to_datetime(log_line[1])
                        skill = log_line[2]
                        if log_line[7] != "":
                            damage = int(log_line[7].replace(".",""))
                        else:
                            damage = 0
                        if log_line[8] != "":
                            heal = int(log_line[8].replace(".",""))
                        else:
                            heal = 0
                        target = log_line[9]
                        writer_output.writerow([source,time,skill,damage,heal,target])
                    elif log_line[2]=="[Player has died]":
                        deadplayer = log_line[0]
                        time = transform_to_datetime(log_line[1])
                        writer_death.writerow([deadplayer,time])
RAID_ID = "08-09-U"
folder_path = RAID_ID + "/Logs"
for filename in os.listdir(folder_path):
    if filename.endswith('.txt'):
        file_path = os.path.join(folder_path, filename)
        compile_logs([file_path], file_path[:-4] + "_logext.csv", file_path[:-4] + "_logdeath.csv")