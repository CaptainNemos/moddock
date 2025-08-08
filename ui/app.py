import tkinter as tk
from tkinter import ttk
from ui.tabs_simple_mods import ModsTab
from ui.tabs_simple_servercfg import ServerCfgTab
from ui.tabs_simple_docker import DockerTab
from ui.tabs_advanced import AdvancedTab
from data import config_repo

class ModDockApp(tk.Frame):
    def __init__(self, master, mods):
        super().__init__(master)
        self.master = master
        self.mods = mods
        self.current_view = tk.StringVar(value=config_repo.get_setting("last_view", "simple"))
        self._build()

    def _build(self):
        toggle_frame = tk.Frame(self)
        toggle_frame.pack(fill="x", pady=4)
        tk.Button(toggle_frame, text="Simple", command=lambda: self._switch_view("simple")).pack(side="left", padx=2)
        tk.Button(toggle_frame, text="Advanced", command=lambda: self._switch_view("advanced")).pack(side="left", padx=2)

        self.content_frame = tk.Frame(self)
        self.content_frame.pack(fill="both", expand=True)
        self._switch_view(self.current_view.get())  # load saved view

    def _switch_view(self, view):
        self.current_view.set(view)
        config_repo.set_setting("last_view", view)   # save to config
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        if view == "simple":
            self._build_simple_view()
        else:
            self._build_advanced_view()

    def _build_simple_view(self):
        nb = ttk.Notebook(self.content_frame)
        nb.pack(fill="both", expand=True)

        nb.add(ModsTab(nb, self.mods, self._compose_action), text="Mods")
        nb.add(ServerCfgTab(nb), text="Server Config")
        nb.add(DockerTab(nb, self._compose_action), text="Docker Control")

    def _build_advanced_view(self):
        AdvancedTab(self.content_frame).pack(fill="both", expand=True)

    def _compose_action(self, action: str):
        from data.paths import base_path
        from services import docker_service
        fn = {
            "start": docker_service.start,
            "stop": docker_service.stop,
            "restart": docker_service.restart,
        }.get(action)
        if not fn:
            return

        rc = fn(cwd=base_path())  # run compose inside the app folder
        from tkinter import messagebox
        if rc != 0:
            messagebox.showerror(
                "Docker",
                f"{action.title()} failed. Check Docker Desktop and docker-compose.yml.",
            )
        else:
            messagebox.showinfo("Docker", f"{action.title()} OK.")

