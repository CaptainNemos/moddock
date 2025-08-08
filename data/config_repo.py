import json
import os
from data.paths import base_path

CONFIG_FILE = base_path("moddock_config.json")

_default_config = {
    "settings": {
        "last_view": "simple",
        "steam_user": "",
        "steam_password_enc": ""
    },
    "mods": []
}

def _load():
    
    # Migration
    old_mods_file = base_path("installed_mods.json")
    old_settings_file = base_path("settings.json")
    migrated = False
    if os.path.exists(old_mods_file) or os.path.exists(old_settings_file):
        data = _default_config.copy()
        if os.path.exists(old_settings_file):
            try:
                with open(old_settings_file, "r", encoding="utf-8") as f:
                    data["settings"].update(json.load(f))
            except:
                pass
        if os.path.exists(old_mods_file):
            try:
                with open(old_mods_file, "r", encoding="utf-8") as f:
                    data["mods"] = json.load(f)
            except:
                pass
        _save(data)
        for p in [old_mods_file, old_settings_file]:
            try: os.remove(p)
            except: pass
        return data
    
    if not os.path.exists(CONFIG_FILE):
        return _default_config.copy()
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        # merge defaults in case new keys were added
        merged = _default_config.copy()
        merged["settings"] = {**_default_config["settings"], **data.get("settings", {})}
        merged["mods"] = data.get("mods", [])
        return merged
    except Exception as e:
        print(f"[config_repo] Failed to load config: {e}")
        return _default_config.copy()

def _save(data):
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"[config_repo] Failed to save config: {e}")

# Settings
def get_setting(key, default=None):
    cfg = _load()
        # Sync with filesystem
    mods_dir = base_path("mods")
    os.makedirs(mods_dir, exist_ok=True)
    fs_mods = [d for d in os.listdir(mods_dir) if os.path.isdir(os.path.join(mods_dir, d)) and d.startswith("@")]

    # Map by id
    mods_by_id = {m["id"]: m for m in cfg["mods"]}
    for folder in fs_mods:
        mod_id = folder.lstrip("@")
        if mod_id in mods_by_id:
            if mods_by_id[mod_id].get("status") != "downloaded":
                mods_by_id[mod_id]["status"] = "downloaded"
        else:
            mods_by_id[mod_id] = {
                "id": mod_id,
                "name": f"Mod {mod_id}",
                "status": "downloaded",
                "enabled": True
            }
    # Mark missing
    for mod_id in list(mods_by_id.keys()):
        if f"@{mod_id}" not in fs_mods and mods_by_id[mod_id]["status"] == "downloaded":
            mods_by_id[mod_id]["status"] = "missing"

    cfg["mods"] = list(mods_by_id.values())
    _save(cfg)

    return cfg["settings"].get(key, default)

def set_setting(key, value):
    cfg = _load()
    cfg["settings"][key] = value
    _save(cfg)

# Mods
def get_mods():
    cfg = _load()
    return cfg["mods"]

def set_mods(mods):
    cfg = _load()
    cfg["mods"] = mods
    _save(cfg)
