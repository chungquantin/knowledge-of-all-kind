import json


def save_json_file(path, data):
    with open(path, "w+") as f:
        json.dump(data, f, indent=4, sort_keys=True)