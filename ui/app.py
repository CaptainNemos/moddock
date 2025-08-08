import tkinter as tk
from tkinter import ttk, messagebox
import os
from data.paths import base_path, ensure_structure
from data import settings_repo, mods_repo
from services import docker_service
from .tabs_simple import SimpleTab
from .tabs_advanced import AdvancedTab

class ModDockApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ModDock Server Manager")
        self.geometry("900x650")

        ensure_structure()

        self.settings = settings_repo.load()
        self.simple_mode = tk.BooleanVar(value=self.settings.get("simple_mode", True))
        self.mods = mods_repo.load()

        self._build_ui()

    def _build_ui(self):
        mode_frame = tk.Frame(self)
        mode_frame.pack(anchor="ne", pady=5, padx=5)
        tk.Checkbutton(mode_frame, text="Simple Mode",
                       variable=self.simple_mode, command=self._toggle_mode).pack(side="right")

        self.tabs = ttk.Notebook(self)
        self.tabs.pack(expand=True, fill="both")

        self.simple_tab = SimpleTab(self, on_compose_action=self._compose_action)
        self.advanced_tab = AdvancedTab(self)

        self.tabs.add(self.simple_tab, text="Simple")
        self.tabs.add(self.advanced_tab, text="Advanced")
        self._toggle_mode()

    def _toggle_mode(self):
        self.tabs.select(self.simple_tab if self.simple_mode.get() else self.advanced_tab)
        self.settings["simple_mode"] = self.simple_mode.get()
        settings_repo.save(self.settings)

    def _compose_action(self, action: str):
        fn = {"start": docker_service.start, "stop": docker_service.stop, "restart": docker_service.restart}.get(action)
        if not fn: return
        rc = fn(cwd=os.path.dirname(base_path()))
        if rc != 0:
            messagebox.showerror("Docker", f"{action.title()} failed. Check Docker and docker-compose.yml.")
        else:
            messagebox.showinfo("Docker", f"{action.title()} OK.")
