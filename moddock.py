import os
import json
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
from PIL import Image, ImageTk

import sys

def base_path(*relative_path):
    """Always resolves path relative to executable or script location"""
    try:
        root = sys._MEIPASS  # PyInstaller temp folder
    except AttributeError:
        root = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(root, *relative_path)

# Ensure required folders and files exist even before UI loads
for folder in ["media", "mods", "profiles"]:
    os.makedirs(base_path(folder), exist_ok=True)

installed_mods_path = base_path("installed_mods.json")
if not os.path.exists(installed_mods_path):
    with open(installed_mods_path, "w") as f:
        f.write("{}")

# Create a default profile if none exists
profile_dir = base_path("profiles")
if not any(f.endswith(".json") for f in os.listdir(profile_dir)):
    with open(os.path.join(profile_dir, "arma3.json"), "w") as pf:
        pf.write("{}")

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

SETTINGS_FILE = "settings.json"
PROFILE_FOLDER = base_path("profiles")
MODS_FOLDER = "mods/"
MODS_JSON = base_path("installed_mods.json")

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_settings(data):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(data, f, indent=2)

def load_profile(profile_name):
    path = os.path.join(PROFILE_FOLDER, f"{profile_name}.json")
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return {}

def load_mods():
    if os.path.exists(MODS_JSON):
        with open(MODS_JSON, "r") as f:
            return json.load(f)
    return []

def save_mods(mods):
    with open(MODS_JSON, "w") as f:
        json.dump(mods, f, indent=2)

class ModDockApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ModDock Server Manager")
        self.geometry("900x650")
        self.iconbitmap(resource_path("media/moddock_logo.ico"))

        self.settings = load_settings()
        self.profile_name = self.settings.get("last_profile", "arma3")
        self.profile = load_profile(self.profile_name)
        self.simple_mode = tk.BooleanVar(value=self.settings.get("simple_mode", True))

        self.mods = load_mods()
        self.build_ui()

    def build_ui(self):

        # Ensure essential folders and files exist
        os.makedirs(base_path("profiles"), exist_ok=True)
        os.makedirs(base_path("mods"), exist_ok=True)
        os.makedirs(base_path("media"), exist_ok=True)
        if not any(f.endswith(".json") for f in os.listdir(base_path("profiles"))):
            with open("profiles/arma3.json", "w") as pf:
                pf.write("{}")
        mode_frame = tk.Frame(self)
        mode_frame.pack(anchor="ne", pady=5, padx=5)

        tk.Checkbutton(mode_frame, text="Simple Mode", variable=self.simple_mode, command=self.toggle_mode).pack(side="right")

        profile_frame = tk.Frame(self)
        profile_frame.pack(pady=5)
        tk.Label(profile_frame, text="Profile:").pack(side="left")
        self.profile_selector = ttk.Combobox(profile_frame, values=self.get_profiles(), state="readonly")
        self.profile_selector.set(self.profile_name)
        self.profile_selector.bind("<<ComboboxSelected>>", self.on_profile_change)
        self.profile_selector.pack(side="left")

        self.tabs = ttk.Notebook(self)
        self.tabs.pack(expand=True, fill="both")

        self.simple_tab = tk.Frame(self.tabs)
        self.advanced_tab = tk.Frame(self.tabs)

        self.tabs.add(self.simple_tab, text="Simple")
        self.tabs.add(self.advanced_tab, text="Advanced")

        self.build_simple_tab()
        self.build_advanced_tab()
        self.toggle_mode()

    def get_profiles(self):
        return [f.replace(".json", "") for f in os.listdir(PROFILE_FOLDER) if f.endswith(".json")]

    def on_profile_change(self, event):
        selected = self.profile_selector.get()
        self.profile = load_profile(selected)
        self.profile_name = selected
        self.settings["last_profile"] = selected
        save_settings(self.settings)

    def build_simple_tab(self):
        tk.Label(self.simple_tab, text="Installed Mods:", font=("Arial", 12)).pack(pady=(10, 0))
        self.mods_listbox = tk.Listbox(self.simple_tab, width=80, height=10)
        self.mods_listbox.pack(pady=5)
        self.refresh_mods_list()

        tk.Button(self.simple_tab, text="Add Mod (Single ID)", command=self.add_mod_single).pack(pady=5)
        tk.Button(self.simple_tab, text="Add Mods (Bulk IDs)", command=self.add_mods_bulk).pack(pady=5)
        tk.Button(self.simple_tab, text="Import Mod Collection", command=self.import_collection).pack(pady=5)
        tk.Button(self.simple_tab, text="Run Docker Server", command=self.run_server).pack(pady=10)

    def build_advanced_tab(self):
        tk.Label(self.advanced_tab, text="Advanced features coming soon...", font=("Arial", 12)).pack(pady=20)

    def toggle_mode(self):
        if self.simple_mode.get():
            self.tabs.select(self.simple_tab)
        else:
            self.tabs.select(self.advanced_tab)
        self.settings["simple_mode"] = self.simple_mode.get()
        save_settings(self.settings)

    def refresh_mods_list(self):
        self.mods_listbox.delete(0, tk.END)
        for mod in self.mods:
            self.mods_listbox.insert(tk.END, f"{mod['name']} ({mod['id']}) [{mod['status']}]")

    def add_mod_single(self):
        mod_id = simpledialog.askstring("Add Mod", "Enter Steam Workshop Mod ID:")
        if mod_id:
            self.add_mod(mod_id.strip())

    def add_mods_bulk(self):
        ids = simpledialog.askstring("Add Mods", "Enter Steam Workshop IDs separated by commas:")
        if ids:
            for mod_id in ids.split(","):
                self.add_mod(mod_id.strip())

    def add_mod(self, mod_id):
        if any(mod["id"] == mod_id for mod in self.mods):
            return
        mod_name = f"Mod {mod_id}"  # Placeholder for real API call
        mod_entry = {"id": mod_id, "name": mod_name, "status": "installed", "source": "manual"}
        self.mods.append(mod_entry)
        os.makedirs(os.path.join(MODS_FOLDER, f"@{mod_id}"), exist_ok=True)
        save_mods(self.mods)
        self.refresh_mods_list()

    def import_collection(self):
        url = simpledialog.askstring("Collection URL", "Paste Steam Workshop Collection URL:")
        if url:
            messagebox.showinfo("Coming Soon", f"Would import mods from: {url}")

    def run_server(self):
        messagebox.showinfo("Docker", "This would run the docker-compose file.")

if __name__ == "__main__":
    app = ModDockApp()
    app.mainloop()
