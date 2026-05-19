import json
from pathlib import Path


def get_json(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, encoding="utf-8") as file:
        return json.load(file)


def save_json(obj, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as file:
        json.dump(obj, file, ensure_ascii=False, indent=4)