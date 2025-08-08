import tkinter as tk
from tkinter import simpledialog
from data import mods_repo

class SimpleTab(tk.Frame):
    def __init__(self, master, on_compose_action):
        super().__init__(master)
        self.on_compose_action = on_compose_action
        self.mods = master.mods
        self._build()

    def _build(self):
        tk.Label(self, text="Installed Mods:", font=("Arial", 12)).pack(pady=(10,0))
        self.mods_list = tk.Listbox(self, width=80, height=10); self.mods_list.pack(pady=5)
        self._refresh_mods()

        tk.Button(self, text="Add Mod (Single ID)", command=self._add_mod_single).pack(pady=5)
        tk.Button(self, text="Add Mods (Bulk IDs)", command=self._add_mods_bulk).pack(pady=5)
        tk.Button(self, text="Import Mod Collection", command=self._import_collection).pack(pady=5)

        frame = tk.Frame(self); frame.pack(pady=10)
        for label, action in [("Start","start"),("Stop","stop"),("Restart","restart")]:
            tk.Button(frame, text=label, command=lambda a=action: self.on_compose_action(a)).pack(side="left", padx=5)
        tk.Label(self, text="Requires docker-compose.yml in the project folder.").pack(pady=4)

    def _refresh_mods(self):
        self.mods_list.delete(0, tk.END)
        for mod in self.mods:
            self.mods_list.insert(tk.END, f"{mod['name']} ({mod['id']}) [{mod['status']}]")

    def _add_mod_single(self):
        mod_id = simpledialog.askstring("Add Mod", "Enter Steam Workshop Mod ID:")
        if mod_id:
            self._add_mod(mod_id.strip())

    def _add_mods_bulk(self):
        ids = simpledialog.askstring("Add Mods", "Enter Steam Workshop IDs separated by commas:")
        if ids:
            for mod_id in ids.split(","):
                self._add_mod(mod_id.strip())

    def _add_mod(self, mod_id):
        if any(m["id"] == mod_id for m in self.mods): return
        mod = {"id": mod_id, "name": f"Mod {mod_id}", "status": "installed", "source": "manual"}
        self.mods.append(mod)
        mods_repo.save(self.mods)
        self._refresh_mods()

    def _import_collection(self):
        # placeholder; wired when steamcmd_service lands
        pass
