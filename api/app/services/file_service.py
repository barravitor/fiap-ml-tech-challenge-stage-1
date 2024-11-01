import os

def check_if_file_exists(file_path) -> bool:
    return os.path.exists(file_path)

def create_folder_does_not_exist(directory_path):
    os.makedirs(directory_path, exist_ok=True)

def remove_file_by_path(csv_file_path: str):
    try:
        os.remove(csv_file_path)
        print(f"The file {csv_file_path} has been deleted.")
    except FileNotFoundError:
        print(f"The file {csv_file_path} not found.")
    except Exception as e:
        print(f"Error to delete file: {e}")