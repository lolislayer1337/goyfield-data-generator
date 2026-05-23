from pathlib import Path

import paths
from utils import get_json


def check_images():
    items: dict = get_json(paths.ITEMS_PATH)
    buildings: dict = get_json(paths.BUILDINGS_PATH)

    item_icons = [item["iconId"] for item in items.values()]
    building_icons = [building["iconId"] for building in buildings.values()]

    print("Checking item icons...")

    item_icon_counter = 0
    for icon_id in item_icons:
        if not check_image_exists(paths.ITEM_ICONS_FOLDER_PATH, icon_id):
            print(f"Image not found: {icon_id}")
            continue

        item_icon_counter += 1
    
    print(f"Item icons found: {item_icon_counter}/{len(item_icons)}")

    print("Checking building icons...")

    building_icon_counter = 0
    for icon_id in building_icons:
        if not check_image_exists(paths.BUILDING_ICONS_FOLDER_PATH, icon_id):
            print(f"Image not found: {icon_id}")
            continue

        building_icon_counter += 1
    
    print(f"Building icons found: {building_icon_counter}/{len(building_icons)}")

    print("\nChecking complete:\n" +
    f"    Item icons: {item_icon_counter}/{len(item_icons)}\n" +
    f"    Building icons: {building_icon_counter}/{len(building_icons)}\n")


def check_image_exists(folder_path: Path, icon_id: str):
    path = folder_path / f"{icon_id}.png"

    return path.exists()
