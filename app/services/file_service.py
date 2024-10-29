import os
import csv

def check_if_file_exists(file_path) -> bool:
    return os.path.exists(file_path)

def get_file_path(file_name):
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    tmp_dir = os.path.join(project_root, 'tmp')

    os.makedirs(tmp_dir, exist_ok=True)

    return os.path.join(tmp_dir, file_name)


def write_to_csv(data, file_name):
    """
    Escreve uma lista de dicionários em um arquivo CSV.

    :param data: Lista de dicionários com os dados a serem escritos
    :param file_name: Nome do arquivo CSV a ser criado
    """
    if not data:
        print("Nenhum dado para escrever.")
        return

    headers = data[0].keys()

    file_path = get_file_path(file_name)

    with open(file_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()

        for entry in data:
            writer.writerow(entry)

    return file_path
