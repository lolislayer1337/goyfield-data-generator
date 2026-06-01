from pathlib import Path

import paths
from utils import get_json, save_json


def merge_data():
    print("Merging data...")

    data_files_list: list[str] = [
        paths.ITEMS,
        paths.FULL_BOTTLES,
        paths.FUEL,
        paths.CRAFTABLE_ITEMS,
        paths.RESOURCE_POINTS,
        paths.BUILDINGS,
        paths.CRAFTERS,
        paths.MINERS,
        paths.PUMPS,
        paths.POWER_STATIONS,
        paths.MACHINE_CRAFTS,
        paths.MACHINE_CRAFT_GROUPS,
        paths.MANUAL_CRAFTS,
        paths.HUB_CRAFTS
    ]

    merged_prev = [get_json(paths.MERGED_DATA_FOLDER_PATH / file_name) for file_name in data_files_list]

    new_data = [get_json(paths.OUT_DATA_FOLDER_PATH / file_name) for file_name in data_files_list]

    merged_new = [merge(new_data[i], merged_prev[i]) for i in range(len(data_files_list))]

    for i in range(len(data_files_list)):
        table = merged_new[i]
        file_name = data_files_list[i]

        save_json(table, paths.MERGED_DATA_FOLDER_PATH / file_name)
    
    print("Data merging completed")


def merge_locales():
    print("Merging locales...")

    merged_locales_folders_list: list[Path] = [
        paths.MERGED_DE_PATH,
        paths.MERGED_EN_PATH,
        paths.MERGED_ES_PATH,
        paths.MERGED_FR_PATH,
        paths.MERGED_ID_PATH,
        paths.MERGED_IT_PATH,
        paths.MERGED_JA_PATH,
        paths.MERGED_KO_PATH,
        paths.MERGED_PT_PATH,
        paths.MERGED_RU_PATH,
        paths.MERGED_TH_PATH,
        paths.MERGED_VI_PATH,
        paths.MERGED_ZHCN_PATH,
        paths.MERGED_ZHTW_PATH
    ]

    out_locales_folders_list: list[Path] = [
        paths.DE_OUT_PATH,
        paths.EN_OUT_PATH,
        paths.ES_OUT_PATH,
        paths.FR_OUT_PATH,
        paths.ID_OUT_PATH,
        paths.IT_OUT_PATH,
        paths.JA_OUT_PATH,
        paths.KO_OUT_PATH,
        paths.PT_OUT_PATH,
        paths.RU_OUT_PATH,
        paths.TH_OUT_PATH,
        paths.VI_OUT_PATH,
        paths.ZHCN_OUT_PATH,
        paths.ZHTW_OUT_PATH
    ]

    locales_files_list: list[str] = [
        paths.ITEMS,
        paths.BUILDINGS,
        paths.ITEM_NAMES,
        paths.BUILDING_NAMES,
        paths.RESOURCE_POINTS,
        paths.RESOURCE_POINT_NAMES
    ]

    for i in range(len(merged_locales_folders_list)):
        merge_folder = merged_locales_folders_list[i]
        out_folder = out_locales_folders_list[i]

        for file_name in locales_files_list:
            table_1 = get_json(out_folder / file_name)
            table_2 = get_json(merge_folder / file_name)

            new_table = merge(table_1, table_2)

            save_json(new_table, merge_folder / file_name)

    print("Locales merging completed")


# if there is a conflict, table_1 takes precedence
def merge(table_1: dict | list, table_2: dict | list):
    if isinstance(table_1, dict) and isinstance(table_2, dict):
        return merge_table(table_1, table_2)
    
    if isinstance(table_1, list) and isinstance(table_2, list):
        return merge_list(table_1, table_2)

def merge_list(list_1: list, list_2: list):
    result = set()

    for i in list_1:
        result.add(i)
    
    for i in list_2:
        result.add(i)
    
    return list(result)

# if there is a conflict, table_1 takes precedence
def merge_table(table_1: dict, table_2: dict):
    result_table = {k: v for k, v in table_2.items()}

    for k, v in table_1.items():
        result_table[k] = v
    
    return result_table
