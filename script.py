import json

from utils import get_json, save_json


# input locales
BR_PATH = "./data/I18nTextTable_BR.json"
CN_PATH = "./data/I18nTextTable_CN.json"
DE_PATH = "./data/I18nTextTable_DE.json"
EN_PATH = "./data/I18nTextTable_EN.json"
FR_PATH = "./data/I18nTextTable_FR.json"
ID_PATH = "./data/I18nTextTable_ID.json"
IT_PATH = "./data/I18nTextTable_IT.json"
JP_PATH = "./data/I18nTextTable_JP.json"
KR_PATH = "./data/I18nTextTable_KR.json"
MX_PATH = "./data/I18nTextTable_MX.json"
RU_PATH = "./data/I18nTextTable_RU.json"
TC_PATH = "./data/I18nTextTable_TC.json"
TH_PATH = "./data/I18nTextTable_TH.json"
VN_PATH = "./data/I18nTextTable_VN.json"

# input files
ITEM_TABLE_PATH = "./data/ItemTable.json"
FULL_BOTTLE_TABLE_PATH = "./data/FullBottleTable.json"
FACTORY_MACHINE_CRAFT_TABLE_PATH = "./data/FactoryMachineCraftTable.json"
FACTORY_MACHINE_CRAFT_GROUP_TABLE_PATH = "./data/FactoryMachineCraftGroupTable.json"
FACTORY_MANUAL_CRAFT_TABLE_PATH = "./data/FactoryManualCraftTable.json"
FACTORY_HUB_CRAFT_TABLE_PATH = "./data/FactoryHubCraftTable.json"
FACTORY_MACHINE_CRAFTER_TABLE_PATH = "./data/FactoryMachineCrafterTable.json"
FACTORY_FUEL_ITEM_TABLE_PATH = "./data/FactoryFuelItemTable.json"
FACTORY_POWER_STATION_TABLE_PATH = "./data/FactoryPowerStationTable.json"
FACTORY_MINER_TABLE_PATH = "./data/FactoryMinerTable.json"
FACTORY_BUILDING_ITEM_REVERSE_TABLE_PATH = "./data/FactoryBuildingItemReverseTable.json"
FACTORY_FLUID_PUMP_IN_TABLE = "./data/FactoryFluidPumpInTable.json"

# output files
MACHINE_CRAFT_TABLE_PATH = "./out/machineCrafts.json"
MACHINE_CRAFT_GROUP_PATH = "./out/machineCraftGroups.json"
MACHINE_CRAFTERS_PATH = "./out/crafters.json"
FUEL_PATH = "./out/fuel.json"
POWER_STATIONS_PATH = "./out/powerStations.json"
MINERS_PATH = "./out/miners.json"
FLUID_PUMPS_PATH = "./out/fluidPumps.json"
BUILDINGS_PATH = "./out/buildings.json"
ITEM_ID_TO_BUILDING_ID_PATH = "./out/itemId2BuildingId.json"
FULL_BOTTLES_PATH = "./out/fullBottles.json"
MANUAL_CRAFTS_PATH = "./out/manualCrafts.json"
BUILDING_CRAFTS_PATH = "./out/hubCrafts.json"

craft_table = get_json(FACTORY_MACHINE_CRAFT_TABLE_PATH)
craft_group_table = get_json(FACTORY_MACHINE_CRAFT_GROUP_TABLE_PATH)
crafters_table = get_json(FACTORY_MACHINE_CRAFTER_TABLE_PATH)
fuel_item_table = get_json(FACTORY_FUEL_ITEM_TABLE_PATH)
power_station_table = get_json(FACTORY_POWER_STATION_TABLE_PATH)
miner_table = get_json(FACTORY_MINER_TABLE_PATH)
building_item_reverse_table = get_json(FACTORY_BUILDING_ITEM_REVERSE_TABLE_PATH)
fluid_pump_in_table = get_json(FACTORY_FLUID_PUMP_IN_TABLE)
full_bottle_table = get_json(FULL_BOTTLE_TABLE_PATH)
manual_craft_table = get_json(FACTORY_MANUAL_CRAFT_TABLE_PATH)
hub_craft_table = get_json(FACTORY_HUB_CRAFT_TABLE_PATH)


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


save_json(machine_crafts, MACHINE_CRAFT_TABLE_PATH)
save_json(machine_craft_groups, MACHINE_CRAFT_GROUP_PATH)
save_json(machine_crafters, MACHINE_CRAFTERS_PATH)
save_json(fuel, FUEL_PATH)
save_json(power_stations, POWER_STATIONS_PATH)
save_json(miners, MINERS_PATH)
save_json(buildings, BUILDINGS_PATH)
save_json(item_id_to_building_id, ITEM_ID_TO_BUILDING_ID_PATH)
save_json(fluid_pumps, FLUID_PUMPS_PATH)
save_json(full_bottles, FULL_BOTTLES_PATH)
save_json(manual_crafts, MANUAL_CRAFTS_PATH)
save_json(building_crafts, BUILDING_CRAFTS_PATH)
