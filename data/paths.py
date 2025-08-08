import os, sys

def base_path(*parts):
    try:
        root = sys._MEIPASS  # PyInstaller temp dir
    except AttributeError:
        # package root (this file: .../moddock/data/paths.py)
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(root, *parts)

def ensure_structure():
    for folder in ["media", "mods", "profiles"]:
        os.makedirs(base_path(folder), exist_ok=True)
