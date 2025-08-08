import json, os
from .paths import base_path

SETTINGS_FILE = base_path("settings.json")

def load():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    return {}

def save(data):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(data, f, indent=2)
