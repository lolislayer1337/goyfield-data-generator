from pathlib import Path

import paths
from utils import get_json, save_json


def fetch_locales():
    item_table = get_json(paths.ITEM_TABLE_PATH)
    building_table = get_json(paths.FACTORY_BUILDING_TABLE_PATH)
    items = get_json(paths.ITEMS_PATH)
    full_bottles = get_json(paths.FULL_BOTTLES_PATH)
    buildings = get_json(paths.BUILDINGS_PATH)

    items_i18n_id = {}
    for i in items.keys():
        id = i
        name_id = str(item_table[id]["name"]["id"])

        items_i18n_id[id] = {
            "nameId": name_id
        }

    buildings_i18n_id = {}
    for i in buildings.keys():
        id = i
        name_id = str(building_table[id]["name"]["id"])

        buildings_i18n_id[id] = {
            "nameId": name_id
        }

    item_groups_i18n_id = {
        "nature": {"nameId": 4705594465915771189},
        "gatherable": {"nameId": -9150267921727244148},
        "product": {"nameId": 597830712374115114},
        "usable": {"nameId": -4607626685843896299},
        "facility": {"nameId": -6016389103269425768}
    }



    def save_locales(input_path: Path, output_folder_path: Path):
        locales = get_json(input_path)

        items_i18n = {}
        for item_id, obj in items_i18n_id.items():
            name_id = str(obj["nameId"])

            name = locales[name_id]

            items_i18n[item_id] = {
                "name": name
            }
        
        for item_id, obj in full_bottles.items():
            liquid_id = obj["liquidId"]
            empty_bottle_id = obj["emptyBottleId"]

            liquid_name = items_i18n[liquid_id]["name"]
            empty_bottle_name = items_i18n[empty_bottle_id]["name"]

            items_i18n[item_id]["name"] = f"{empty_bottle_name} ({liquid_name})"
        
        buildings_i18n = {}
        for building_id, obj in buildings_i18n_id.items():
            name_id = str(obj["nameId"])

            name = locales[name_id]

            buildings_i18n[building_id] = {
                "name": name
            }
        
        item_groups_i18n = {}
        for item_group_id, obj in item_groups_i18n_id.items():
            name_id = str(obj["nameId"])

            name = locales[name_id]

            item_groups_i18n[item_group_id] = {
                "name": name
            }
        
        save_json(items_i18n, output_folder_path / "items.json")
        save_json(buildings_i18n, output_folder_path / "buildings.json")
        save_json(item_groups_i18n, output_folder_path / "itemGroups.json")


    save_locales(paths.DE_PATH, paths.DE_OUT_PATH)
    save_locales(paths.EN_PATH, paths.EN_OUT_PATH)
    save_locales(paths.MX_PATH, paths.ES_OUT_PATH)
    save_locales(paths.FR_PATH, paths.FR_OUT_PATH)
    save_locales(paths.ID_PATH, paths.ID_OUT_PATH)
    save_locales(paths.IT_PATH, paths.IT_OUT_PATH)
    save_locales(paths.JP_PATH, paths.JA_OUT_PATH)
    save_locales(paths.KR_PATH, paths.KO_OUT_PATH)
    save_locales(paths.BR_PATH, paths.PT_OUT_PATH)
    save_locales(paths.RU_PATH, paths.RU_OUT_PATH)
    save_locales(paths.TH_PATH, paths.TH_OUT_PATH)
    save_locales(paths.VN_PATH, paths.VI_OUT_PATH)
    save_locales(paths.CN_PATH, paths.ZHCN_OUT_PATH)
    save_locales(paths.TC_PATH, paths.ZHTW_OUT_PATH)
