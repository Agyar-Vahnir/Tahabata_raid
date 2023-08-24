import csv

def find_duplicate_names(csv_file):
    name_counts = {}
    duplicate_names = []

    with open(csv_file, 'r', newline='') as file:
        reader = csv.DictReader(file, delimiter=';')
        for row in reader:
            name = row['Name']
            if name in name_counts:
                name_counts[name] += 1
            else:
                name_counts[name] = 1

            if name_counts[name] == 2:
                duplicate_names.append(name)

    return duplicate_names

def remove_duplicates_from_csv(csv_file, duplicate_names):
    rows_to_keep = []
    with open(csv_file, 'r', newline='') as file:
        reader = csv.DictReader(file, delimiter=';')
        for row in reader:
            name = row['Name']
            if name not in duplicate_names:
                rows_to_keep.append(row)

    with open(csv_file, 'w', newline='') as file:
        fieldnames = ['Name', 'Faction', 'Class']  # Replace with the actual column names
        writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()
        for row in rows_to_keep:
            writer.writerow(row)

def write_to_file(file_name, data):
    with open(file_name, 'w') as file:
        for item in data:
            file.write(f"{item}\n")

if __name__ == "__main__":
    input_file = "Players.csv"
    output_file = "duplicate_names.txt"

    duplicate_names_list = find_duplicate_names(input_file)

    if duplicate_names_list:
        remove_duplicates_from_csv(input_file, duplicate_names_list)
        write_to_file(output_file, duplicate_names_list)
        print("Duplicate names have been removed from the CSV file.")
        print("Duplicate names have been written to 'duplicate_names.txt'")
    else:
        print("No duplicate names found in the CSV file.")
