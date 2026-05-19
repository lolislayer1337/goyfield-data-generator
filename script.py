from pathlib import Path

import paths
from utils import get_json, save_json


craft_table = get_json(paths.FACTORY_MACHINE_CRAFT_TABLE_PATH)
craft_group_table = get_json(paths.FACTORY_MACHINE_CRAFT_GROUP_TABLE_PATH)
crafters_table = get_json(paths.FACTORY_MACHINE_CRAFTER_TABLE_PATH)
fuel_item_table = get_json(paths.FACTORY_FUEL_ITEM_TABLE_PATH)
power_station_table = get_json(paths.FACTORY_POWER_STATION_TABLE_PATH)
miner_table = get_json(paths.FACTORY_MINER_TABLE_PATH)
building_item_reverse_table = get_json(paths.FACTORY_BUILDING_ITEM_REVERSE_TABLE_PATH)
fluid_pump_in_table = get_json(paths.FACTORY_FLUID_PUMP_IN_TABLE_PATH)
full_bottle_table = get_json(paths.FULL_BOTTLE_TABLE_PATH)
manual_craft_table = get_json(paths.FACTORY_MANUAL_CRAFT_TABLE_PATH)
hub_craft_table = get_json(paths.FACTORY_HUB_CRAFT_TABLE_PATH)
item_table = get_json(paths.ITEM_TABLE_PATH)
item_type_table = get_json(paths.ITEM_TYPE_TABLE_PATH)
wiki_group_table = get_json(paths.WIKI_GROUP_TABLE_PATH)
wiki_entry_data_table = get_json(paths.WIKI_ENTRY_DATA_TABLE_PATH)
building_table = get_json(paths.FACTORY_BUILDING_TABLE_PATH)

en = get_json(paths.EN_PATH)
ru = get_json(paths.RU_PATH)


buildings = {}

machine_craft_groups = {}
msPerRound_groups = {}
for formula_group_id, obj in craft_group_table.items():
    id = obj["formulaGroupIdGroup"]
    craft_list = obj["craftList"]
    ms_per_round = obj["msPerRound"]

    machine_craft_groups[id] = {
        "id": id,
        "craftList": craft_list,
    }
    msPerRound_groups[formula_group_id] = ms_per_round


all_items = set()
machine_crafts = {}
for formula_id, craft in craft_table.items():
    id = craft["id"]
    formula_group_id = craft["formulaGroupId"]
    building_id = craft["machineId"]
    ingredients = []
    outcomes = []
    progress_round = craft["progressRound"]
    craft_time_ms = progress_round * msPerRound_groups[formula_group_id]
    for i in craft["ingredients"]:
        for item in i["group"]:
            ingredients.append({
                "count": item["count"],
                "itemId": item["id"]
            })
            all_items.add(item["id"])
    
    for i in craft["outcomes"]:
        for item in i["group"]:
            outcomes.append({
                "count": item["count"],
                "itemId": item["id"]
            })
            all_items.add(item["id"])

    obj = {
        "id": id,
        "formulaGroupId": formula_group_id,
        "buildingId": building_id,
        "ingredients": ingredients,
        "outcomes": outcomes,
        "craftTimeMs": craft_time_ms
    }

    machine_crafts[id] = obj

manual_crafts = {}
for formula_id, obj in manual_craft_table.items():
    id = obj["id"]
    ingredients = []
    outcomes = []

    for item in obj["ingredients"]:
        ingredients.append({
            "count": item["count"],
            "itemId": item["id"]
        })
        all_items.add(item["id"])
    
    for item in obj["outcomes"]:
        outcomes.append({
            "count": item["count"],
            "itemId": item["id"]
        })
        all_items.add(item["id"])
    
    manual_crafts[id] = {
        "id": id,
        "ingredients": ingredients,
        "outcomes": outcomes
    }

building_crafts = {}
for building_id, obj in hub_craft_table.items():
    id = obj["id"]
    ingredients = []
    outcomes = []

    for item in obj["ingredients"]:
        ingredients.append({
            "count": item["count"],
            "itemId": item["id"]
        })
        all_items.add(item["id"])
    
    for item in obj["outcomes"]:
        outcomes.append({
            "count": item["count"],
            "itemId": item["id"]
        })
        all_items.add(item["id"])
    
    building_crafts[id] = {
        "id": id,
        "ingredients": ingredients,
        "outcomes": outcomes
    }

full_bottles = {}
for item_id, obj in full_bottle_table.items():
    id = obj["id"]
    empty_bottle_id = obj["emptyBottleId"]
    liquid_id = obj["liquidId"]

    full_bottles[id] = {
        "id": id,
        "emptyBottleId": empty_bottle_id,
        "liquidId": liquid_id
    }


machine_crafters = {}
for building_id, obj in crafters_table.items():
    id = building_id
    mode_map = []
    for mode in obj["modeMap"]:
        formula_group_id = mode["groupName"]
        mode_name = mode["modeName"]
        if formula_group_id == "":
            continue
        mode_map.append({
            "formulaGroupId": formula_group_id,
            "modeName": mode_name
        })
    
    if len(mode_map) == 0:
        continue

    machine_crafters[id] = {
        "id": building_id,
        "modeMap": mode_map
    }

    buildings[id] = {
        "id": id,
        "type": "crafter"
    }


fuel = {}
for item_id, obj in fuel_item_table.items():
    power_provide = obj["powerProvide"]
    progress_round = obj["progressRound"]

    fuel[item_id] = {
        "id": item_id,
        "powerProvide": power_provide,
        "progressRound": progress_round
    }


power_stations = {}
for building_id, obj in power_station_table.items():
    id = obj["id"]
    ms_per_round = obj["msPerRound"]

    power_stations[id] = {
        "id": id,
        "msPerRound": ms_per_round
    }

    buildings[id] = {
        "id": id,
        "type": "powerStation"
    }

miners = {}
for building_id, obj in miner_table.items():
    id = obj["id"]
    mining_time_ms = obj["msPerRound"]
    mineable = []
    
    for i in obj["mineable"]:
        temp = {
            "miningItemId": i["miningItemId"],
            "miningTimeMs": mining_time_ms
        }
        if i["consumeItem"]["id"] != "":
            temp["consumeItem"] = {
                "itemId": i["consumeItem"]["id"],
                "count": i["consumeItem"]["count"]
            }
        mineable.append(temp)

    miners[id] = {
        "id": id,
        "mineable": mineable
    }

    buildings[id] = {
        "id": id,
        "type": "miner"
    }

fluid_pumps = {}
for building_id, obj in fluid_pump_in_table.items():
    id = obj["id"]
    pump_time_ms = obj["msPerRound"]
    enable_liquid_ids = obj["enableLiquidIds"]

    fluid_pumps[id] = {
        "id": id,
        "pumpTimeMs": pump_time_ms,
        "enableLiquidIds": enable_liquid_ids
    }

    buildings[id] = {
        "id": id,
        "type": "pump"
    }

item_id_to_building_id = {}
for building_id, obj in buildings.items():
    item_id = building_item_reverse_table[building_id]["itemId"]

    obj["itemId"] = item_id
    item_id_to_building_id[item_id] = building_id


item_categories = {
    "wiki_group_item_nature": "nature",
    "wiki_group_item_material": "gatherable",
    "wiki_group_item_product": "product",
    "wiki_group_item_usable": "usable",

}
for obj in wiki_group_table["wiki_type_building"]["list"]:
    item_categories[obj["groupId"]] = "facility"

item_id_to_group_id = {}
for obj in wiki_entry_data_table.values():
    item_id = obj["refItemId"]
    group_id = obj["groupId"]

    if item_id == "": continue
    if group_id not in item_categories: continue

    item_id_to_group_id[item_id] = item_categories[group_id]


items = {}
for item_id in all_items:
    obj = item_table[item_id]

    id = obj["id"]
    icon_id = obj["iconId"]
    rarity = obj["rarity"]
    group_id = item_id_to_group_id[item_id]

    items[id] = {
        "id": id,
        "iconId": icon_id,
        "rarity": rarity,
        "groupId": group_id
    }


save_json(machine_crafts, paths.MACHINE_CRAFT_TABLE_PATH)
save_json(machine_craft_groups, paths.MACHINE_CRAFT_GROUP_PATH)
save_json(machine_crafters, paths.MACHINE_CRAFTERS_PATH)
save_json(fuel, paths.FUEL_PATH)
save_json(power_stations, paths.POWER_STATIONS_PATH)
save_json(miners, paths.MINERS_PATH)
save_json(buildings, paths.BUILDINGS_PATH)
save_json(item_id_to_building_id, paths.ITEM_ID_TO_BUILDING_ID_PATH)
save_json(fluid_pumps, paths.FLUID_PUMPS_PATH)
save_json(full_bottles, paths.FULL_BOTTLES_PATH)
save_json(manual_crafts, paths.MANUAL_CRAFTS_PATH)
save_json(building_crafts, paths.BUILDING_CRAFTS_PATH)
save_json(items, paths.ITEMS_PATH)

# locales

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
