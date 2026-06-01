from pathlib import Path

import paths
from utils import get_json, save_json


def create_empty_merged_files_if_not_exists():
    print("Creating empty files...")

    data_list: list[Path] = [
        paths.MERGED_ITEMS_PATH,
        paths.MERGED_FULL_BOTTLES_PATH,
        paths.MERGED_FUEL_PATH,
        paths.MERGED_CRAFTABLE_ITEMS_PATH,
        paths.MERGED_RESOURCE_POINTS_PATH,
        paths.MERGED_ITEM_ID_TO_BUILDING_ID_PATH,
        paths.MERGED_BUILDINGS_PATH,
        paths.MERGED_CRAFTERS_PATH,
        paths.MERGED_MINERS_PATH,
        paths.MERGED_PUMPS_PATH,
        paths.MERGED_POWER_STATIONS_PATH,
        paths.MERGED_MACHINE_CRAFTS_PATH,
        paths.MERGED_MACHINE_CRAFT_GROUPS_PATH,
        paths.MERGED_MANUAL_CRAFTS_PATH,
        paths.MERGED_HUB_CRAFTS_PATH
    ]

    locales_folders_list: list[Path] = [
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

    locales_files_list: list[str] = [
        paths.ITEMS,
        paths.BUILDINGS,
        paths.ITEM_NAMES,
        paths.BUILDING_NAMES,
        paths.RESOURCE_POINTS,
        paths.RESOURCE_POINT_NAMES
    ]

    for path in data_list:
        if not path.exists():
            save_json({}, path)
    
    for folder in locales_folders_list:
        for file_name in locales_files_list:
            path = folder / file_name

            if not path.exists():
                save_json({}, path)

    print("Files created")
