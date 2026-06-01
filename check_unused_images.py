from pathlib import Path

import paths
from utils import get_json


def check_unused_images():
    items: dict = get_json(paths.MERGED_ITEMS_PATH)
    buildings: dict = get_json(paths.MERGED_BUILDINGS_PATH)

    item_icons = set([item["iconId"] for item in items.values()])
    building_icons = set([building["iconId"] for building in buildings.values()])

    print("Checking item icons...")

    unused_item_icons = get_unused_images(paths.ITEM_ICONS_FOLDER_PATH, item_icons)
    
    if (len(unused_item_icons) == 0): print("Unused item icons not found")
    else: print(f"Unused item icons found: {len(unused_item_icons)}")

    unused_building_icons = get_unused_images(paths.BUILDING_ICONS_FOLDER_PATH, building_icons)

    if (len(unused_building_icons) == 0): print("Unused building icons not found")
    else: print(f"Unused building icons found: {len(unused_building_icons)}")

    print("\nUnused icons found:\n" +
          f"    Item icons: {len(unused_item_icons)}\n" +
          f"    Building icons: {len(unused_building_icons)}\n")
    
    ans = input("Delete unused files? Y/N\n").lower()

    if ans == "y" or ans == "yes":
        print("Deleting files...")
        err_item_icons = delete_files(unused_item_icons)
        err_building_icons = delete_files(unused_building_icons)

        file_count = len(unused_item_icons) + len(unused_building_icons)
        err_count = len(err_item_icons) + len(err_building_icons)
        print("\nDeletion results:\n" + 
              f"    Successful deleted: {file_count - err_count}/{file_count}")
        if err_count != 0:
            print(f"    Error when deleting: {err_count}")
        print("")

        


def get_unused_images(folder_path: Path, icons: set) -> set[Path]:
    unused_icons = set()
    files = [f for f in folder_path.iterdir() if f.is_file()]

    for file in files:
        if file.stem not in icons:
            unused_icons.add(file)
    
    return unused_icons


def delete_files(files: set[Path]) -> list[Path]:
    delete_err = []
    for file in files:
        successful = delete_file(file)

        if not successful:
            delete_err.append(file)
    
    return delete_err
    


def delete_file(file: Path) -> bool:
    if not file.is_file():
        print(f"{file.name} is not a file")
        return False
    
    try:
        file.unlink()
    except OSError as e:
        print(f"Error when deleting {file.name}: {e}")
        return False
    
    return True