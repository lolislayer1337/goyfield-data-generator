import json


def get_json(path):
    with open(path, encoding="utf-8") as file:
        return json.load(file)


def save_json(obj, path):
    with open(path, "w", encoding="utf-8") as file:
        json.dump(obj, file, ensure_ascii=False, indent=4)