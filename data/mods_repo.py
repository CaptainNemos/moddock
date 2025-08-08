import json, os
from .paths import base_path

MODS_JSON = base_path("installed_mods.json")

def load():
    if os.path.exists(MODS_JSON):
        with open(MODS_JSON, "r") as f:
            return json.load(f)
    return []

def save(mods):
    with open(MODS_JSON, "w") as f:
        json.dump(mods, f, indent=2)
