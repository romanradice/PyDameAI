import json
import os.path
from definition import DATA_DIR

def set_data_path_json(path: str, data: dict):
    with open(path, 'w') as outfile:
        json.dump(data, outfile)

def set_data_json(file_name: str, data: dict):
    path = os.path.join(DATA_DIR, file_name)
    with open(path, 'w') as outfile:
        json.dump(data, outfile)

def get_data_json(file_name: str) -> dict:
    path = os.path.join(DATA_DIR, file_name)
    data = {}
    try:
        with open(path) as json_file:
            data = json.load(json_file)
    except json.JSONDecodeError:
        pass
    return data

def add_data_json(file_name: str, data: dict):
    data_file = get_data_json(file_name)
    data_file.update(data)
    set_data_json(file_name, data_file)