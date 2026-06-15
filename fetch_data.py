from pathlib import Path

import paths
from utils import get_json, save_json


def fetch_data():
    craft_table: dict =                 get_json(paths.FACTORY_MACHINE_CRAFT_TABLE_PATH)
    craft_group_table: dict =           get_json(paths.FACTORY_MACHINE_CRAFT_GROUP_TABLE_PATH)
    crafters_table: dict =              get_json(paths.FACTORY_MACHINE_CRAFTER_TABLE_PATH)
    fuel_item_table: dict =             get_json(paths.FACTORY_FUEL_ITEM_TABLE_PATH)
    power_station_table: dict =         get_json(paths.FACTORY_POWER_STATION_TABLE_PATH)
    miner_table: dict =                 get_json(paths.FACTORY_MINER_TABLE_PATH)
    building_item_reverse_table: dict = get_json(paths.FACTORY_BUILDING_ITEM_REVERSE_TABLE_PATH)
    fluid_pump_in_table: dict =         get_json(paths.FACTORY_FLUID_PUMP_IN_TABLE_PATH)
    full_bottle_table: dict =           get_json(paths.FULL_BOTTLE_TABLE_PATH)
    manual_craft_table: dict =          get_json(paths.FACTORY_MANUAL_CRAFT_TABLE_PATH)
    hub_craft_table: dict =             get_json(paths.FACTORY_HUB_CRAFT_TABLE_PATH)
    item_table: dict =                  get_json(paths.ITEM_TABLE_PATH)
    wiki_group_table: dict =            get_json(paths.WIKI_GROUP_TABLE_PATH)
    wiki_entry_data_table: dict =       get_json(paths.WIKI_ENTRY_DATA_TABLE_PATH)
    building_table: dict =              get_json(paths.FACTORY_BUILDING_TABLE_PATH)
    enemy_drop_table: dict =            get_json(paths.WIKI_ENEMY_DROP_TABLE_PATH)


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

    for key, value in enemy_drop_table.items():
        item_ids = value["dropItemIds"]
        for item_id in item_ids:
            all_items.add(item_id)


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

        
    item_filters = {
        "rarity": [],
        "type": [],
        "groupId": [],
        "material": []
    }


    
    for item in [v for v in items.values() if v["groupId"] == "nature"]:
        item_id: str = item["id"]
        item_type = get_item_type_nature(item_id)
        item["type"] = item_type
        item["material"] = get_item_material_nature(item_id, item_type)

    for item in [v for v in items.values() if v["groupId"] == "product"]:
        item_id: str = item["id"]
        item_type = get_item_type_product(item_id)
        item["type"] = item_type
        item["material"] = get_item_material_product(item_id, item_type)

    for item in [v for v in items.values() if v["groupId"] == "usable"]:
        item_id: str = item["id"]
        item_type = get_item_type_usable(item_id)
        item["type"] = item_type
        item["material"] = get_item_material_usable(item_id, item_type)

    for item in [v for v in items.values() if v["groupId"] == "gatherable"]:
        item_id: str = item["id"]
        item_type = get_item_type_gatherable(item_id)
        item["type"] = item_type
        item["material"] = None

    crafter_id_list = [buildings[v]["itemId"] for v in machine_crafters.keys()]

    for item in [v for v in items.values() if v["groupId"] == "facility"]:
        item_id: str = item["id"]
        item_type = get_item_type_facility(item_id, crafter_id_list)
        item["type"] = item_type
        item["material"] = None

    
    item_group_set = set()
    item_rarity_set = set()
    item_type_set = set()

    for item in items.values():
        rarity = item["rarity"]
        group = item["groupId"]
        item_type = item["type"]

        item_rarity_set.add(rarity)
        item_group_set.add(group)
        item_type_set.add(item_type)

    item_filters["rarity"] = list(item_rarity_set)
    item_filters["groupId"] = list(item_group_set)
    item_filters["type"] = list(item_type_set)

    item_types = get_key_lists_by_field(items, "type")
    item_groups = get_key_lists_by_field(items, "groupId")
    item_materials = get_key_lists_by_field(items, "material")

    
    items = dict(sorted(items.items(), key=lambda item: item[0]))
    items = dict(sorted(items.items(), key=lambda item: item[1]["groupId"]))

    resource_points = {}
    for obj in [item for item in item_table.values() if item["type"] == 41 or item["type"] == 28]:
        point_id = obj["id"]
        item_id = obj["iconId"]
        point_type = ""

        if obj["type"] == 41:
            point_type = "liquid"

        if obj["type"] == 28:
            point_type = "mine"

        resource_points[point_id] = {
            "id": point_id,
            "itemId": item_id,
            "type": point_type
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
    save_json(craftable_items, paths.CRAFTABLE_ITEMS_PATH)
    save_json(resource_points, paths.RESOURCE_POINTS_PATH)
    save_json(item_filters, paths.ITEM_FILTERS_PATH)
    save_json(item_types, paths.ITEM_TYPES_PATH)
    save_json(item_groups, paths.ITEM_GROUPS_PATH)
    save_json(item_materials, paths.ITEM_MATERIALS_PATH)


def get_item_type_nature(item_id: str) -> str:

    if item_id.startswith("item_liquid"):
        return "liquid"
    
    if "_ore" in item_id or "item_quartz_sand" in item_id:
        return "ore"
    
    if "_wood" in item_id:
        return "wood"
    
    if "_seed_" in item_id:
        return "plant_seed"
    
    if "_spc_" in item_id:
        return "plant_special"
    
    if "_plant_" in item_id:
        return "plant"
    
    return "other"


def get_item_type_product(item_id: str) -> str:

    if item_id.startswith("item_proc_battery_"):
        return "battery"
    
    if item_id.startswith("item_fbottle_"):
        return "full_bottle"
    
    if item_id.startswith("item_liquid_"):
        return "liquid"
    
    if item_id.startswith("item_equip_script_"):
        return "component"
    
    if item_id.startswith("item_muck_"):
        return "muck"
    
    if "enr_powder" in item_id and "xiranite_enr" not in item_id:
        return "compressed_powder"
    
    if "_powder" in item_id:
        return "powder"
    
    if "_cmpt" in item_id:
        return "part"
    
    if "_bottle" in item_id:
        return "bottle"
    
    if (item_id.endswith("_enr") 
        or item_id.endswith("_mtl")
        or item_id.endswith("_glass")
        or item_id.endswith("_shell")
        or item_id.endswith("_nugget")
        or item_id.endswith("_poly")):
        return "ingot"
    
    # if item_id.endswith("_poly"):
    #     return "poly"
    
    if item_id.endswith("_tool"):
        return "tool"
    
    if item_id.endswith("hulu"):
        return "hulu"

    return "other"


def get_item_type_usable(item_id: str) -> str:

    if item_id.startswith("item_proc_bomb"):
        return "bomb"
    
    if "_powder_" in item_id:
        return "powder"
    
    if item_id.startswith("item_bottled_rec_hp"):
        return "hp_recovery"
    
    if item_id.startswith("item_bottled_food"):
        return "food"
    
    if item_id.startswith("item_bottled_flower") or item_id.startswith("item_bottled_grass"):
        return "special_food"

    return "other"


def get_item_type_gatherable(item_id: str) -> str:

    if item_id.startswith("item_muck_"):
        return "muck"
    
    if "_insect_" in item_id:
        return "insect"
    
    if item_id.startswith("item_drop_"):
        return "drop"

    return "other"


def get_item_type_facility(item_id: str, crafter_ids: list[str]) -> str:

    if item_id in crafter_ids:
        return "crafter"

    if item_id.startswith("item_port_battle_"):
        return "battle"
    
    if item_id.startswith("item_port_soil_"):
        return "soil"
    
    if item_id.startswith("item_port_power_"):
        return "power"
    
    if item_id.startswith("item_port_miner_"):
        return "miner"
    
    if item_id.startswith("item_port_pump_"):
        return "pump"

    return "other"


def get_item_material_nature(item_id: str, type_id: str) -> str | None:

    if type_id == "ore":
        if item_id.startswith("item_originium"):
            return "originium"
        
        if item_id.startswith("item_quartz"):
            return "amethyst"
        
        if item_id.startswith("item_iron_"):
            return "iron"
        
        if item_id.startswith("item_copper"):
            return "copper"
    
    if type_id == "liquid":
        if "water" in item_id:
            return "water"
        
        if "acid" in item_id:
            return "acid"
        
    i = item_id.split("_")[-1]

    if item_id.startswith("item_plant_grass_spc"):
        return f"plant_grass_spc_{i}"

    if item_id.startswith("item_plant_moss_spc"):
        return f"plant_flower_spc_{i}"
    
    if item_id.startswith("item_plant_sp"):
        return f"plant_sp_{i}"
    
    if item_id.startswith("item_plant_grass"):
        return f"plant_grass_{i}"
    
    if item_id.startswith("item_plant_moss"):
        return f"plant_flower_{i}"
    
    if item_id.startswith("item_plant_bbflower"):
        return f"plant_bbflower_{i}"

    return None


def get_item_material_product(item_id: str, type_id: str) -> str | None:

    if type_id == "full_bottle":
        return None
    
    if "crystal_enr" in item_id or "originium_enr" in item_id:
        return "originium_enr"
    
    if "crystal" in item_id or "originium" in item_id:
        return "originium"
    
    if "quartz_enr" in item_id or "glass_enr" in item_id:
        return "amethyst_enr"
    
    if "quartz" in item_id or "glass" in item_id:
        return "amethyst"
    
    if "iron_enr" in item_id:
        return "iron_enr"
    
    if "iron" in item_id:
        return "iron"
    
    if "copper_enr" in item_id:
        return "copper_enr"
    
    if "copper" in item_id:
        return "copper"
    
    if "carbon_enr" in item_id:
        return "carbon_enr"
    
    if "carbon" in item_id:
        return "carbon"
    
    i = item_id.split("_")[-1]

    if "plant_moss_spc" in item_id:
        return f"plant_flower_spc_{i}"
    
    if "plant_grass_spc" in item_id:
        return f"plant_grass_spc_{i}"
    
    if "plant_moss" in item_id:
        return f"plant_flower_{i}"
    
    if "plant_grass" in item_id:
        return f"plant_grass_{i}"
    
    if "plant_bbflower" in item_id:
        return f"plant_bbflower_{i}"
    
    if "xiranite_enr" in item_id:
        return "xiranite_enr"
    
    if "xiranite" in item_id:
        return "xiranite"
    
    if "sewage" in item_id:
        return "sewage"
    
    if item_id.startswith("item_equip_script"):
        if item_id.endswith("_4_1"):
            return "copper"
        
        if item_id.endswith("_4_2"):
            return "copper_enr"
        
        if item_id.endswith("_1"):
            return "amethyst"
        
        if item_id.endswith("_2"):
            return "iron"
        
        if item_id.endswith("_3"):
            return "amethyst_enr"
        
        if item_id.endswith("_4"):
            return "xiranite"
        
    return None


def get_item_material_usable(item_id: str, type_id: str) -> str | None:

    if "item_bottled_food_" in item_id:
        if item_id.endswith("_1") or item_id.endswith("_2") or item_id.endswith("_3"):
            return "plant_flower_2"
        
        if item_id.endswith("_4") or item_id.endswith("_5"):
            return "plant_grass_1"
        
    if "item_bottled_rec_hp_" in item_id:
        if item_id.endswith("_1") or item_id.endswith("_2") or item_id.endswith("_3"):
            return "plant_flower_1"
        
        if item_id.endswith("_4") or item_id.endswith("_5"):
            return "plant_grass_2"
        
    if item_id.startswith("item_bottled_flower") and "spc" in item_id:
        i = item_id[19:-5]
        
        return f"plant_flower_spc_{i}"
    
    if item_id.startswith("item_bottled_grass") and "spc" in item_id:
        i = item_id[18:-5]

        return f"plant_grass_spc_{i}"
    
    i = item_id.split("_")[-1]
    
    if item_id.startswith("item_plant_grass_powder"):
        return f"plant_grass_{i}"
    
    if item_id.startswith("item_plant_grass_spc_powder"):
        return f"plant_grass_spc_{i}"
    
    if item_id.startswith("item_plant_moss_powder"):
        return f"plant_flower_{i}"
    
    if item_id.startswith("item_plant_moss_spc_powder"):
        return f"plant_flower_spc_{i}"

    return None


def get_key_lists_by_field(d: dict, field_name: str) -> dict[str, list]:
    result: dict[str, list] = {
        "None": []
    }

    for k, v in d.items():
        if field_name not in v:
            result["None"].append(k)
            continue

        field_value = v[field_name]

        if field_value is None:
            result["None"].append(k)
            continue

        if field_value not in result:
            result[field_value] = []
        
        result[field_value].append(k)

    for k, v in result.items():
        result[k] = sorted(v)
    
    return result
