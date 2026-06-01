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