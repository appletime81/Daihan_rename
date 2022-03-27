import os
from pathlib import Path
from pprint import pprint
from datetime import datetime
from xml.dom import minidom
import xml.etree.ElementTree as ET


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
    return files_created_time_list


def sort_func(item: list):
    return item[1]


def gen_xml_file(all_item_created_time_list: list):
    # item[0] = item's path, item[1] = item's created time
    for item in all_item_created_time_list:
        get_machine_info_by_tet_file_name(item[0])

    root = minidom.Document()

    xml = root.createElement("Transaction")
    xml.setAttribute("Name", "AIImageInfo")
    root.appendChild(xml)

    productChild = root.createElement("product")
    productChild.setAttribute("name", "Geeks for Geeks")
    xml.appendChild(productChild)

    www = root.createElement("www")
    www.setAttribute("name", "www for Geeks")
    productChild.appendChild(www)

    # 儲存檔案
    xml_str = root.toprettyxml(indent="\t")
    save_path_file = "gfg.xml"

    with open(save_path_file, "w") as f:
        f.write(xml_str)


def rename():
    pass


def get_machine_info_by_tet_file_name(txt_file_path: str):
    txt_file_name = txt_file_path.split("/")[-1]
    if txt_file_name[-3:] == "txt":
        txt_file_name_str_list = txt_file_name.split("_")
        log_point = txt_file_name_str_list[0]
        machine_name = txt_file_name_str_list[1]
        lot_number = txt_file_name_str_list[2]
        pin_package = txt_file_name_str_list[3]
        return log_point, machine_name, lot_number, pin_package


def main():
    all_txt_file_created_time_list = get_create_time(get_all_txt_file_path())
    all_image_file_created_time_list = get_create_time(get_all_image_file_path())
    all_item_created_time_list = (
        all_txt_file_created_time_list + all_image_file_created_time_list
    )
    # pprint(all_item_created_time_list)
    all_item_created_time_list = sorted(all_item_created_time_list, key=sort_func)
    pprint(all_item_created_time_list)
    gen_xml_file(all_item_created_time_list)


main()
