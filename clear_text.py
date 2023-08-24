import os

def process_files_in_folder(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(folder_path, filename)
            process_file_in_place(file_path)

def process_file_in_place(file_path):
    with open(file_path, 'r') as f:
        text = f.read()

    # Retirer toutes les parenthèses
    text = remove_parentheses(text)

    # Retirer tout le texte jusqu'à arriver au caractère ":"
    text = remove_text_until_colon(text)

    # Transformer toutes les "," en "\n"
    text = replace_commas_with_newlines(text)

    with open(file_path, 'w') as f:
        f.write(text)

def remove_parentheses(text):
    return ''.join(char for char in text if char not in '().')

def remove_text_until_colon(text):
    index = text.find(': ')
    if index != -1:
        return text[index + 2:]
    return text

def replace_commas_with_newlines(text):
    return text.replace(', ', '\n')

# Appel de la fonction pour un dossier donné
folder_path = '07-30-U'
process_files_in_folder(folder_path)
