import json
import os
from typing import Dict, Any
from data.paths import base_path

CONFIG_FILE = base_path("moddock_config.json")

_default_config: Dict[str, Any] = {
    "settings": {
        "last_view": "simple",
        "steam_user": "",
        "steam_password_saved": False,
    },
    # store mods as dict keyed by string id
    "mods": {}
}

def _read_file(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def _write_file(path: str, data: Any) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def _ensure_defaults(cfg: Dict[str, Any]) -> Dict[str, Any]:
    merged = {
        "settings": {**_default_config["settings"], **cfg.get("settings", {})},
        "mods": cfg.get("mods", {})
    }
    # normalize mods to dict if it came in as a list
    if isinstance(merged["mods"], list):
        merged["mods"] = {str(m.get("id")): m for m in merged["mods"] if isinstance(m, dict) and "id" in m}
    # ensure string keys
    if isinstance(merged["mods"], dict):
        merged["mods"] = {str(k): v for k, v in merged["mods"].items()}
    return merged

def _load_cfg() -> Dict[str, Any]:
    # First-run migration from old files if present
    old_mods = base_path("installed_mods.json")
    old_settings = base_path("settings.json")
    if not os.path.exists(CONFIG_FILE) and (os.path.exists(old_mods) or os.path.exists(old_settings)):
        cfg = _default_config.copy()
        # migrate settings
        if os.path.exists(old_settings):
            try:
                s = _read_file(old_settings)
                if isinstance(s, dict):
                    cfg["settings"].update(s)
            except Exception:
                pass
        # migrate mods (list or dict)
        if os.path.exists(old_mods):
            try:
                m = _read_file(old_mods)
                if isinstance(m, list):
                    cfg["mods"] = {str(it.get("id")): it for it in m if isinstance(it, dict) and "id" in it}
                elif isinstance(m, dict):
                    cfg["mods"] = {str(k): v for k, v in m.items()}
            except Exception:
                pass
        _write_file(CONFIG_FILE, cfg)
        # don't delete old files automatically—user can keep as backup
        return cfg

    if os.path.exists(CONFIG_FILE):
        try:
            cfg = _read_file(CONFIG_FILE)
            return _ensure_defaults(cfg)
        except Exception:
            # fallback to defaults on read error
            return _default_config.copy()
    else:
        return _default_config.copy()

def _save_cfg(cfg: Dict[str, Any]) -> None:
    # ensure directory exists (usually root, but just in case)
    os.makedirs(os.path.dirname(CONFIG_FILE) or ".", exist_ok=True)
    _write_file(CONFIG_FILE, cfg)

# ------------- Settings API -------------

def get_setting(key: str, default=None):
    cfg = _load_cfg()
    return cfg["settings"].get(key, default)

def set_setting(key: str, value) -> None:
    cfg = _load_cfg()
    cfg["settings"][key] = value
    _save_cfg(cfg)

# ------------- Mods API -------------

def get_mods() -> Dict[str, Dict[str, Any]]:
    """
    Return mods as a dict keyed by string mod_id.
    Also performs a light filesystem sync with ./mods/@<id> directories:
      - mark existing folders as 'downloaded'
      - mark previously 'downloaded' but missing folders as 'missing'
    """
    cfg = _load_cfg()
    mods: Dict[str, Dict[str, Any]] = cfg.get("mods", {})
    if not isinstance(mods, dict):
        # normalize if file was edited manually
        if isinstance(mods, list):
            mods = {str(m.get("id")): m for m in mods if isinstance(m, dict) and "id" in m}
        else:
            mods = {}

    # filesystem sync
    mods_dir = base_path("mods")
    os.makedirs(mods_dir, exist_ok=True)
    fs_mods = set()
    try:
        for entry in os.listdir(mods_dir):
            full = os.path.join(mods_dir, entry)
            if os.path.isdir(full) and entry.startswith("@"):
                fs_mods.add(entry[1:])  # strip '@'
    except Exception:
        pass

    # mark downloaded
    for mid in fs_mods:
        mid = str(mid)
        if mid not in mods:
            mods[mid] = {"id": mid, "name": f"Mod {mid}", "enabled": True, "status": "downloaded", "source": "steam"}
        else:
            if mods[mid].get("status") != "downloaded":
                mods[mid]["status"] = "downloaded"

    # mark missing if previously downloaded but folder gone
    for mid, m in list(mods.items()):
        if m.get("status") == "downloaded" and str(mid) not in fs_mods:
            m["status"] = "missing"

    cfg["mods"] = mods
    _save_cfg(cfg)
    return mods

def set_mods(mods: Dict[str, Dict[str, Any]]) -> None:
    # normalize keys to strings
    if isinstance(mods, dict):
        mods = {str(k): v for k, v in mods.items()}
    elif isinstance(mods, list):
        mods = {str(m.get("id")): m for m in mods if isinstance(m, dict) and "id" in m}
    else:
        mods = {}
    cfg = _load_cfg()
    cfg["mods"] = mods
    _save_cfg(cfg)
