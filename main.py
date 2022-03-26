import os
from pathlib import Path
from pprint import pprint
from datetime import datetime


def get_all_txt_file_path():
    txt_files_paths = list()
    for root, dirs, files in os.walk(os.getcwd()):
        for file in files:
            if file[-3:] == "txt":
                txt_files_paths.append(os.path.join(root, file))
    return txt_files_paths


def get_all_image_file_path():
    image_files_paths = list()
    for root, _, files in os.walk(os.getcwd()):
        for file in files:
            if file[-3:] == "jpg":
                image_files_paths.append(os.path.join(root, file))
    return image_files_paths


def get_create_time(files_paths: list):
    files_created_time_list = list()
    for files_path in files_paths:
        files_created_time_list.append(
            [
                files_path,
                datetime.fromtimestamp(Path(files_path).stat().st_mtime).strftime(
                    "%Y-%m-%d-%H:%M:%S"
                ),
            ]
        )


def main():
    get_create_time(get_all_txt_file_path())
    get_create_time(get_all_image_file_path())


main()
