import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
import os
from data import mods_repo
from data.paths import base_path
from services import compose_generator  # coming soon; not used yet here
from services import steamcmd_service

ARMA_APP_ID = "107410"

class SimpleTab(tk.Frame):
    def __init__(self, master, on_compose_action):
        super().__init__(master)
        self.on_compose_action = on_compose_action
        self.mods = master.mods  # list of dicts
        self._steam_user = None
        self._steam_pass = None
        self._build()

    def _build(self):
        # Title
        tk.Label(self, text="Installed Mods:", font=("Arial", 12)).pack(pady=(10,0))

        # Mods list
        self.mods_list = tk.Listbox(self, width=80, height=12, selectmode=tk.EXTENDED)
        self.mods_list.pack(pady=5, fill="x", padx=8)
        self._refresh_mods()

        # Row of actions
        row = tk.Frame(self); row.pack(pady=8)

        tk.Button(row, text="Add Mods", command=self._add_mods).pack(side="left", padx=5)
        tk.Button(row, text="Toggle Enable/Disable", command=self._toggle_enabled).pack(side="left", padx=5)
        tk.Button(row, text="Download Selected (SteamCMD)", command=self._download_selected).pack(side="left", padx=5)
        tk.Button(row, text="Edit server.cfg", command=self._edit_server_cfg).pack(side="left", padx=5)

        # Docker controls
        frame = tk.Frame(self); frame.pack(pady=10)
        for label, action in [("Start","start"),("Stop","stop"),("Restart","restart")]:
            tk.Button(frame, text=label, command=lambda a=action: self.on_compose_action(a)).pack(side="left", padx=6)

        tk.Label(self, text="Tip: generate or place docker-compose.yml in the app folder, then Start.", fg="#555").pack(pady=(6,0))

    def _refresh_mods(self):
        self.mods_list.delete(0, tk.END)
        for mod in self.mods:
            enabled = mod.get("enabled", True)
            status = mod.get("status", "unknown")
            self.mods_list.insert(tk.END, f"[{'✓' if enabled else ' '}] {mod.get('name','Mod')} ({mod.get('id')}) [{status}]")

    def _save(self):
        mods_repo.save(self.mods)

    def _add_mods(self):
        ids = simpledialog.askstring("Add Mods", "Enter Steam Workshop IDs (comma or space separated):")
        if not ids:
            return
        # split by comma/space
        raw = [p.strip() for chunk in ids.replace(",", " ").split(" ") for p in [chunk.strip()] if p.strip()]
        added = 0
        for mod_id in raw:
            if any(m.get("id") == mod_id for m in self.mods):
                continue
            self.mods.append({
                "id": mod_id,
                "name": f"Mod {mod_id}",
                "status": "added",
                "source": "steam",
                "enabled": True
            })
            added += 1
        if added:
            self._save()
            self._refresh_mods()

    def _selected_indices(self):
        return list(self.mods_list.curselection())

    def _toggle_enabled(self):
        idxs = self._selected_indices()
        if not idxs:
            messagebox.showinfo("Mods", "Select one or more mods to toggle.")
            return
        for i in idxs:
            self.mods[i]["enabled"] = not self.mods[i].get("enabled", True)
        self._save()
        self._refresh_mods()

    def _ensure_creds(self):
        # read from env first
        if self._steam_user is None:
            self._steam_user = os.environ.get("STEAM_USER", "")
        if self._steam_pass is None:
            self._steam_pass = os.environ.get("STEAM_PASSWORD", "")

        if not self._steam_user:
            self._steam_user = simpledialog.askstring("Steam Login", "Steam username (leave empty for anonymous):") or ""
        if self._steam_user and not self._steam_pass:
            self._steam_pass = simpledialog.askstring("Steam Login", "Steam password:", show="*") or ""

    def _download_selected(self):
        idxs = self._selected_indices()
        if not idxs:
            messagebox.showinfo("Download", "Select one or more mods first.")
            return

        self._ensure_creds()
        mods_dir = base_path("mods")
        os.makedirs(mods_dir, exist_ok=True)

        use_docker = True  # You’re on Windows 11 + Docker Desktop; default to dockerized SteamCMD
        failures = []
        for i in idxs:
            mod_id = self.mods[i]["id"]
            code = steamcmd_service.download_mod(
                mod_id=mod_id,
                app_id=ARMA_APP_ID,
                mods_dir=mods_dir,
                steam_user=self._steam_user,
                steam_pass=self._steam_pass,
                use_docker=use_docker
            )
            if code == 0:
                self.mods[i]["status"] = "downloaded"
                # Optional: create @<id> folder marker
                try: os.makedirs(os.path.join(mods_dir, f"@{mod_id}"), exist_ok=True)
                except Exception: pass
            else:
                failures.append(mod_id)
                self.mods[i]["status"] = f"error({code})"

        self._save()
        self._refresh_mods()

        if failures:
            messagebox.showerror("SteamCMD", f"Failed: {', '.join(failures)}")
        else:
            messagebox.showinfo("SteamCMD", "All selected mods downloaded.")

    def _edit_server_cfg(self):
        cfg_path = base_path("server.cfg")
        if not os.path.exists(cfg_path):
            # very minimal ARMA 3 template
            template = (
                'hostname = "My ARMA Server";\n'
                "password = \"\";\n"
                "passwordAdmin = \"\";\n"
                "maxPlayers = 32;\n"
                "verifySignatures = 2;\n"
                "voteMissionPlayers = 1;\n"
                "voteThreshold = 0.33;\n"
            )
            try:
                with open(cfg_path, "w", encoding="utf-8") as f:
                    f.write(template)
            except Exception as e:
                messagebox.showerror("server.cfg", f"Failed to create: {e}")
                return

        # Simple text editor window
        win = tk.Toplevel(self)
        win.title("Edit server.cfg")
        win.geometry("700x500")
        txt = tk.Text(win, wrap="none")
        txt.pack(expand=True, fill="both")

        try:
            with open(cfg_path, "r", encoding="utf-8") as f:
                txt.insert("1.0", f.read())
        except Exception as e:
            messagebox.showerror("server.cfg", f"Failed to load: {e}")

        def save_cfg():
            try:
                with open(cfg_path, "w", encoding="utf-8") as f:
                    f.write(txt.get("1.0", "end-1c"))
                messagebox.showinfo("server.cfg", "Saved.")
            except Exception as e:
                messagebox.showerror("server.cfg", f"Failed to save: {e}")

        tk.Button(win, text="Save", command=save_cfg).pack(pady=6)
