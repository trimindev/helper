import os


def count_files_in_folder(folder_path):
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"The folder path '{folder_path}' does not exist.")

    file_count = 0

    for _, _, files in os.walk(folder_path):
        file_count += len(files)

    return file_count
