from pathlib import Path

import paths
from utils import get_json, save_json


def fetch_data():
    craft_table =                 get_json(paths.FACTORY_MACHINE_CRAFT_TABLE_PATH)
    craft_group_table =           get_json(paths.FACTORY_MACHINE_CRAFT_GROUP_TABLE_PATH)
    crafters_table =              get_json(paths.FACTORY_MACHINE_CRAFTER_TABLE_PATH)
    fuel_item_table =             get_json(paths.FACTORY_FUEL_ITEM_TABLE_PATH)
    power_station_table =         get_json(paths.FACTORY_POWER_STATION_TABLE_PATH)
    miner_table =                 get_json(paths.FACTORY_MINER_TABLE_PATH)
    building_item_reverse_table = get_json(paths.FACTORY_BUILDING_ITEM_REVERSE_TABLE_PATH)
    fluid_pump_in_table =         get_json(paths.FACTORY_FLUID_PUMP_IN_TABLE_PATH)
    full_bottle_table =           get_json(paths.FULL_BOTTLE_TABLE_PATH)
    manual_craft_table =          get_json(paths.FACTORY_MANUAL_CRAFT_TABLE_PATH)
    hub_craft_table =             get_json(paths.FACTORY_HUB_CRAFT_TABLE_PATH)
    item_table =                  get_json(paths.ITEM_TABLE_PATH)
    wiki_group_table =            get_json(paths.WIKI_GROUP_TABLE_PATH)
    wiki_entry_data_table =       get_json(paths.WIKI_ENTRY_DATA_TABLE_PATH)
    building_table =              get_json(paths.FACTORY_BUILDING_TABLE_PATH)


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
        mineable = {}
        
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
            mineable[temp["miningItemId"]] = temp

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


    craftable_items = sorted(list(all_items.copy()))


    for building_id, obj in buildings.items():
        icon_id = building_table[building_id]["iconOnPanel"]
        obj["iconId"] = icon_id


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


    for item in [v for v in items.values() if v["groupId"] == "gatherable"]:
        item_id: str = item["id"]

        if item_id.startswith("item_drop_"):
            items[item_id]["subGroupId"] = "drop"
        
        if item_id.startswith("item_muck_"):
            items[item_id]["subGroupId"] = "muck"

        if item_id.startswith("item_plant_"):
            items[item_id]["subGroupId"] = "plant"
    
    for item in [v for v in items.values() if v["groupId"] == "product"]:
        item_id: str = item["id"]

        if "_powder" in item_id:
            items[item_id]["subGroupId"] = "powder"

        if item_id.startswith("item_xiranite"):
            items[item_id]["subGroupId"] = "xiranite"
        
        if item_id.startswith("item_activity_xiranite"):
            items[item_id]["subGroupId"] = "activityXiranite"
        
        if item_id.startswith("item_carbon"):
            items[item_id]["subGroupId"] = "carbon"

        if item_id.startswith("item_copper"):
            items[item_id]["subGroupId"] = "copper"

        if item_id.startswith("item_crystal") or item_id.startswith("item_originium"):
            items[item_id]["subGroupId"] = "originium"
        
        if item_id.startswith("item_glass") or item_id.startswith("item_quartz"):
            items[item_id]["subGroupId"] = "amethyst"
        
        if item_id.startswith("item_iron"):
            items[item_id]["subGroupId"] = "iron"
        
        if item_id.startswith("item_proc_battery"):
            items[item_id]["subGroupId"] = "battery"
        
        if item_id.startswith("item_equip_script"):
            items[item_id]["subGroupId"] = "component"
        
        if item_id.startswith("item_muck"):
            items[item_id]["subGroupId"] = "muck"
    
    for item in [v for v in items.values() if v["groupId"] == "usable"]:
        item_id: str = item["id"]

        items[item_id]["subGroupId"] = "other"

        if item_id.startswith("item_proc_bomb"):
            items[item_id]["subGroupId"] = "bomb"
        
        if (item_id.startswith("item_bottled_flower") 
            or item_id.startswith("item_bottled_food") 
            or item_id.startswith("item_bottled_grass")
            or item_id.startswith("item_bottled_rec_hp")):
            items[item_id]["subGroupId"] = "bottledProdFood"
        
        if "_powder" in item_id:
            items[item_id]["subGroupId"] = "powder"
        
    for item in [v for v in items.values() if v["groupId"] == "facility"]:
        item_id: str = item["id"]

        items[item_id]["subGroupId"] = "other"

        if item_id.startswith("item_port_battle"):
            items[item_id]["subGroupId"] = "battle"
        
        if item_id.startswith("item_port_soil"):
            items[item_id]["subGroupId"] = "soil"

    for item in [v for v in items.values() if v["groupId"] == "nature"]:
        item_id: str = item["id"]

        if "_ore" in item_id or "item_quartz_sand" in item_id:
            items[item_id]["subGroupId"] = "ore"
        
        if item_id.startswith("item_plant_moss") or item_id.startswith("item_plant_bbflower"):
            items[item_id]["subGroupId"] = "flowerPlant"
        
        if item_id.startswith("item_plant_grass"):
            items[item_id]["subGroupId"] = "grassPlant"
        
        if item_id.startswith("item_plant_sp"):
            items[item_id]["subGroupId"] = "soilPlant"
        
        if "_wood" in item_id:
            items[item_id]["subGroupId"] = "wood"

    for building in buildings.values():
        building_type = building["type"]
        item_id = building["itemId"]

        if item_id == "item_port_furnance_nop_1": continue

        items[item_id]["subGroupId"] = building_type
    
    for item in full_bottles.values():
        fbottle_id = item["id"]
        liquid_id = item["liquidId"]

        items[fbottle_id]["subGroupId"] = "fullBottle"
        items[liquid_id]["subGroupId"] = "liquid"


    sub_groups = set()
    for item in items.values():
        if "subGroupId" not in item: continue

        group_id = item["groupId"]
        sub_group_id = item["subGroupId"]

        item["subGroupId"] = f"{group_id}_{sub_group_id}"
        sub_groups.add(f"{group_id}_{sub_group_id}")

    item_groups = {}
    for item in items.values():
        item_id = item["id"]
        group_id = item["groupId"]

        if group_id not in item_groups:
            item_groups[group_id] = { "withoutSubGroup": [] }
        
        if "subGroupId" in item:
            sub_group_id = item["subGroupId"]

            if sub_group_id not in item_groups[group_id]:
                item_groups[group_id][sub_group_id] = []

            item_groups[group_id][sub_group_id].append(item_id)
        
        else:
            item_groups[group_id]["withoutSubGroup"].append(item_id)
            item_groups[group_id]["withoutSubGroup"] = sorted(item_groups[group_id]["withoutSubGroup"])
    

    item_sub_group_list = sorted(list(sub_groups))

    
    items = dict(sorted(items.items(), key=lambda item: item[0]))
    items = dict(sorted(items.items(), key=lambda item: item[1]["subGroupId"]))
    items = dict(sorted(items.items(), key=lambda item: item[1]["groupId"]))


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
    save_json(item_groups, paths.ITEM_GROUPS_PATH)
    save_json(craftable_items, paths.CRAFTABLE_ITEMS_PATH)
    save_json(item_sub_group_list, paths.ITEM_SUB_GROUP_LIST_PATH)
