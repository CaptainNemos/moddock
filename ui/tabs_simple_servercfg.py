import tkinter as tk
from tkinter import messagebox
import os
from data.paths import base_path

class ServerCfgTab(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        tk.Button(self, text="Edit server.cfg", command=self._edit_server_cfg).pack(pady=10)

    def _edit_server_cfg(self):
        cfg_path = base_path("server.cfg")
        if not os.path.exists(cfg_path):
            template = (
                'hostname = "My ARMA Server";\n'
                "password = \"\";\n"
                "passwordAdmin = \"\";\n"
                "maxPlayers = 32;\n"
                "verifySignatures = 2;\n"
                "voteMissionPlayers = 1;\n"
                "voteThreshold = 0.33;\n"
            )
            with open(cfg_path, "w", encoding="utf-8") as f:
                f.write(template)
        win = tk.Toplevel(self)
        win.title("Edit server.cfg")
        win.geometry("700x500")
        txt = tk.Text(win, wrap="none")
        txt.pack(expand=True, fill="both")
        with open(cfg_path, "r", encoding="utf-8") as f:
            txt.insert("1.0", f.read())
        def save_cfg():
            with open(cfg_path, "w", encoding="utf-8") as f:
                f.write(txt.get("1.0", "end-1c"))
            messagebox.showinfo("server.cfg", "Saved.")
        tk.Button(win, text="Save", command=save_cfg).pack(pady=6)
