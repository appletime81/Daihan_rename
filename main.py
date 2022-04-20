import os
from pathlib import Path
from pprint import pprint
from datetime import datetime
from xml.dom import minidom
import xml.etree.ElementTree as ET
import re


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
    count = 0
    tmp_list = list()
    for i, item in enumerate(all_item_created_time_list):
        if item[0][-3:] != "txt":
            if i > 0 or i == len(all_item_created_time_list) - 1:
                tmp_list.append([item[0], item[1]])
        if (
            item[0][-3:] == "txt"
            and all_item_created_time_list[i + 1][0][-3:] == "jpg"
        ) or i == len(all_item_created_time_list) - 1:
            if i != 0:
                root = minidom.Document()
                xml = root.createElement("Transaction")
                xml.setAttribute("Name", "AIImageInfo")
                root.appendChild(xml)

                for tag_ in [
                    [log_point, "LogPint"],
                    [machine_name, "MachineName"],
                    [lot_number, "LotNumber"],
                    [pin_package, "PinPackage"],
                ]:
                    tag = root.createElement(tag_[1])
                    text = root.createTextNode(str(tag_[0]))
                    tag.appendChild(text)
                    xml.appendChild(tag)

                image_tag = root.createElement("IMAGE")
                image_tag.setAttribute("Count", f"{len(tmp_list)}")

                if len(tmp_list) >= 10:
                    tmp_list = tmp_list[-10:]

                for item in tmp_list[-10:]:
                    tag = root.createElement("Item")
                    tmp_index_name = item[0].split("/")[-1]
                    tmp_index_name = tmp_index_name[
                        re.search("_Index\d+_\d+", tmp_index_name).start() :
                    ]
                    text = root.createTextNode(
                        f'{log_point}_{machine_name}_{lot_number}_{tmp_list.index(item) + 1}_{item[1].replace("-", "").replace(":", "")}{tmp_index_name}'
                    )
                    tag.appendChild(text)
                    image_tag.appendChild(tag)

                xml.appendChild(image_tag)

                xml_str = root.toprettyxml(indent="\t")
                save_path_file = f"{count + 1}.xml"
                count += 1
                with open(save_path_file, "w") as f:
                    f.write(xml_str)

            tmp_list = list()
            if item[0][-3:] == "txt":
                (
                    log_point,
                    machine_name,
                    lot_number,
                    pin_package,
                ) = get_machine_info_by_tet_file_name(
                    all_item_created_time_list[i][0]
                )



def rename(all_item_created_time_list):
    count = 0
    for i, item in enumerate(all_item_created_time_list):
        print(i, item)
        if item[0][-3:] == "txt":
            (
                log_point,
                machine_name,
                lot_number,
                pin_package,
            ) = get_machine_info_by_tet_file_name(all_item_created_time_list[i][0])
            count = 0
        else:
            count += 1
            tmp_index_name = item[0].split("/")[-1]
            tmp_index_name = tmp_index_name[
                re.search("_Index\d+_\d+", tmp_index_name).start() :
            ]
            os.rename(
                item[0],
                f'{os.getcwd()}/After_Convert/{log_point}_{machine_name}_{lot_number}_{count}_{item[1].replace("-", "").replace(":", "")}{tmp_index_name}',
            )


def get_machine_info_by_tet_file_name(txt_file_path: str):
    txt_file_name = txt_file_path.split("/")[-1]
    if txt_file_name[-3:] == "txt":
        txt_file_name_str_list = txt_file_name.split("_")
        log_point = txt_file_name_str_list[0]
        machine_name = txt_file_name_str_list[1]
        lot_number = txt_file_name_str_list[2]
        pin_package = txt_file_name_str_list[3].replace(".txt", "")
        return log_point, machine_name, lot_number, pin_package


def check_item_list(item_list):
    new_item_list = list()
    for i, item in enumerate(item_list):
        if (
            item[0][-3:] == "txt"
            and i < len(item_list) - 1
            and item_list[i + 1][0][-3:] == "txt"
        ):
            pass
        elif item[0][-3:] == "txt" and i == len(item_list) - 1:
            pass
        else:
            new_item_list.append(item)
    return new_item_list


def main():
    all_txt_file_created_time_list = get_create_time(get_all_txt_file_path())
    all_image_file_created_time_list = get_create_time(get_all_image_file_path())
    all_item_created_time_list = (
        all_txt_file_created_time_list + all_image_file_created_time_list
    )
    all_item_created_time_list = sorted(all_item_created_time_list, key=sort_func)
    all_item_created_time_list = check_item_list(all_item_created_time_list)
    # pprint(all_item_created_time_list)
    gen_xml_file(all_item_created_time_list)

    if not os.path.isdir("After_Convert"):
        os.mkdir("After_Convert")
    rename(all_item_created_time_list)


main()
