import os

def check_if_file_exists(file_path) -> bool:
    return os.path.exists(file_path)