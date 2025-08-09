import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import os
import keyring
import threading
import re
from data import config_repo
from data.paths import base_path
from services import steamcmd_service

ARMA_APP_ID = "107410"
KEYRING_SERVICE = "moddock-steam"  # Windows Credential Manager entry

class ModsTab(tk.Frame):
    def __init__(self, master, mods, on_compose_action):
        super().__init__(master)
        # Ensure dict[str, dict]
        self.mods = mods if isinstance(mods, dict) else {}
        self._build()

    # ---------- UI ----------
    def _build(self):
        # Credentials row
        creds = tk.LabelFrame(self, text="Steam Credentials")
        creds.pack(fill="x", padx=8, pady=(8, 4))

        self.var_user = tk.StringVar(value=config_repo.get_setting("steam_user", ""))
        self.var_pass = tk.StringVar(value="")
        self.var_remember = tk.BooleanVar(value=bool(config_repo.get_setting("steam_password_saved", False)))
        self._pass_hidden = True

        tk.Label(creds, text="Username:").grid(row=0, column=0, sticky="w", padx=8, pady=6)
        tk.Entry(creds, textvariable=self.var_user, width=28).grid(row=0, column=1, sticky="w", pady=6)

        tk.Label(creds, text="Password:").grid(row=0, column=2, sticky="w", padx=(16,8), pady=6)
        self.entry_pass = tk.Entry(creds, textvariable=self.var_pass, width=22, show="*")
        self.entry_pass.grid(row=0, column=3, sticky="w", pady=6)
        tk.Button(creds, text="Show", width=6, command=self._toggle_pass).grid(row=0, column=4, sticky="w", padx=6)

        tk.Checkbutton(creds, text="Remember (securely)", variable=self.var_remember).grid(row=1, column=1, sticky="w", pady=(0,8))
        tk.Button(creds, text="Save", command=self._save_creds).grid(row=1, column=3, sticky="e", pady=(0,8))

        # Load saved password if present
        self._load_saved_password_into_field()

        # Mods table
        tk.Label(self, text="Installed Mods:", font=("Arial", 12)).pack(pady=(6,0))

        columns = ("enabled", "name", "id", "status")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", selectmode="extended", height=12)
        self.tree.heading("enabled", text="✓")
        self.tree.heading("name", text="Name")
        self.tree.heading("id", text="Workshop ID")
        self.tree.heading("status", text="Status")

        self.tree.column("enabled", width=40, anchor="center", stretch=False)
        self.tree.column("name", width=300, anchor="w")
        self.tree.column("id", width=140, anchor="center")
        self.tree.column("status", width=140, anchor="center")

        self.tree.pack(pady=5, fill="x", padx=8)

        # Click in 'enabled' column toggles + selects row; double-click anywhere toggles too
        self.tree.column("id", width=120, anchor="center")
        self.tree.column("status", width=120, anchor="center")

        self.tree.pack(pady=5, fill="x", padx=8)

        # Click to toggle checkbox in the 'enabled' column; double-click anywhere also toggles
        self.tree.column("id", width=120, anchor="center")
        self.tree.column("status", width=120, anchor="center")

        self.tree.pack(pady=5, fill="x", padx=8)

        self.tree.column("id", width=120, anchor="center")
        self.tree.column("status", width=120, anchor="center")

        self.tree.pack(pady=5, fill="x", padx=8)

        self.tree.bind("<Button-1>", self._on_click_enabled_col)
        self.tree.bind("<Double-1>", self._toggle_double_click)

        # Action row
        row = tk.Frame(self); row.pack(pady=8)
        tk.Button(row, text="Add Mods", command=self._add_mods).pack(side="left", padx=5)
        tk.Button(row, text="Enable Selected", command=lambda: self._bulk_set_enabled(True)).pack(side="left", padx=5)
        tk.Button(row, text="Disable Selected", command=lambda: self._bulk_set_enabled(False)).pack(side="left", padx=5)
        tk.Button(row, text="Enable Selected", command=lambda: self._bulk_set_enabled(True)).pack(side="left", padx=5)
        tk.Button(row, text="Disable Selected", command=lambda: self._bulk_set_enabled(False)).pack(side="left", padx=5)
        tk.Button(row, text="Download Selected (SteamCMD)", command=self._download_selected).pack(side="left", padx=5)

        self._refresh_mods()

    # ---------- Creds helpers ----------
    def _toggle_pass(self):
        self._pass_hidden = not self._pass_hidden
        self.entry_pass.config(show="" if not self._pass_hidden else "*")

    def _load_saved_password_into_field(self):
        if self.var_remember.get():
            user = self.var_user.get().strip()
            if user:
                try:
                    saved = keyring.get_password(KEYRING_SERVICE, user)
                    if saved:
                        self.var_pass.set(saved)
                except Exception:
                    pass

    def _save_creds(self):
        user = self.var_user.get().strip()
        pwd = self.var_pass.get()
        config_repo.set_setting("steam_user", user)
        if self.var_remember.get() and user and pwd:
            try:
                keyring.set_password(KEYRING_SERVICE, user, pwd)
                config_repo.set_setting("steam_password_saved", True)
                messagebox.showinfo("Settings", "Credentials saved securely.")
            except Exception as e:
                messagebox.showerror("Settings", f"Failed to save password to keyring: {e}")
        else:
            config_repo.set_setting("steam_password_saved", False)
            try:
                if user:
                    keyring.delete_password(KEYRING_SERVICE, user)
            except Exception:
                pass
            messagebox.showinfo("Settings", "Credentials updated (password not stored).")

    def _resolve_creds_for_download(self):
        user = self.var_user.get().strip()
        pwd = self.var_pass.get()
        if self.var_remember.get() and not pwd and user:
            try:
                saved = keyring.get_password(KEYRING_SERVICE, user)
                if saved:
                    pwd = saved
            except Exception:
                pass
        if self.var_remember.get() and not pwd and user:
            try:
                saved = keyring.get_password(KEYRING_SERVICE, user)
                if saved:
                    pwd = saved
            except Exception:
                pass
        return user, pwd

    # ---------- Mods table ----------
    def _refresh_mods(self):
        self.tree.delete(*self.tree.get_children())
        for mod_id, mod in self.mods.items():
            # ensure string keys and fields
            mod_id = str(mod_id)
            enabled = bool(mod.get("enabled", True))
            name = mod.get("name", f"Mod {mod_id}")
            status = mod.get("status", "unknown")
            checkbox = "☑" if enabled else "☐"
            self.tree.insert("", "end", iid=mod_id, values=(checkbox, name, mod_id, status))
        for idx, mod in enumerate(self.mods):
            enabled = mod.get("enabled", True)
            name = mod.get("name", f"Mod {mod['id']}")
            status = mod.get("status", "unknown")
            checkbox = "☑" if enabled else "☐"   # Unicode checkbox glyphs
            self.tree.insert("", "end", iid=str(idx),
                             values=(checkbox, name, mod["id"], status))

    def _save_mods(self):
        config_repo.set_mods(self.mods)

    def _selected_indices(self):
        return [int(i) for i in self.tree.selection()]

    def _on_click_enabled_col(self, event):
        # Only toggle when clicking in the 'enabled' column
        region = self.tree.identify("region", event.x, event.y)
        if region != "cell":
            return
        col = self.tree.identify_column(event.x)
        if col != "#1":  # first column = 'enabled'
            return
        item_id = self.tree.identify_row(event.y)
        if not item_id:
            return
        idx = int(item_id)
        self.mods[idx]["enabled"] = not self.mods[idx].get("enabled", True)
        self._save_mods()
        self._refresh_mods()

    def _toggle_double_click(self, event):
        # Double-click anywhere on a row toggles enabled state
        item_id = self.tree.identify_row(event.y)
        if not item_id:
            return
        idx = int(item_id)
        self.mods[idx]["enabled"] = not self.mods[idx].get("enabled", True)
        self._save_mods()
        self._refresh_mods()

    def _selected_ids(self):
        # return ID strings from selected rows
        return [str(self.tree.item(iid)["values"][2]) for iid in self.tree.selection()]
        
    def _toggle_double_click(self, event):
        # Double-click anywhere on a row toggles enabled state
        item_id = self.tree.identify_row(event.y)
        if not item_id:
            return
        idx = int(item_id)
        self.mods[idx]["enabled"] = not self.mods[idx].get("enabled", True)
        self._save_mods()
        self._refresh_mods()

    def _bulk_set_enabled(self, value: bool):
        idxs = self._selected_indices()
        if not idxs:
            messagebox.showinfo("Mods", "Select one or more mods first.")
            return
        for i in idxs:
            self.mods[i]["enabled"] = value
        self._save_mods()
        self._refresh_mods()

    def _add_mods(self):
        ids = simpledialog.askstring("Add Mods", "Enter Steam Workshop IDs (comma or space separated):")
        if not ids:
            return
        for i in idxs:
            self.mods[i]["enabled"] = value
        self._save_mods()
        self._refresh_mods()

    def _on_click_enabled_col(self, event):
        region = self.tree.identify("region", event.x, event.y)
        if region != "cell":
            return
        col = self.tree.identify_column(event.x)
        item_id = self.tree.identify_row(event.y)
        if not item_id:
            return
        # Always select the row the user clicked on (more intuitive)
        self.tree.selection_set(item_id)

        if col == "#1":  # first column = 'enabled'
            mod_id = str(item_id)
            if mod_id not in self.mods:
                return
            self.mods[mod_id]["enabled"] = not bool(self.mods[mod_id].get("enabled", True))
        raw = [p.strip() for chunk in ids.replace(",", " ").split(" ") for p in [chunk.strip()] if p.strip()]
        changed = False
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
            changed = True
        if changed:
            self._save_mods()
            self._refresh_mods()

    def _toggle_double_click(self, event):
        item_id = self.tree.identify_row(event.y)
        if not item_id:
            return
        self.tree.selection_set(item_id)
        mod_id = str(item_id)
        if mod_id in self.mods:
            self.mods[mod_id]["enabled"] = not bool(self.mods[mod_id].get("enabled", True))
            self._save_mods()
            self._refresh_mods()

    def _bulk_set_enabled(self, value: bool):
        ids = self._selected_ids()
        if not ids:
            messagebox.showinfo("Mods", "Select one or more mods first.")
            return
        for mod_id in ids:
            if mod_id in self.mods:
                self.mods[mod_id]["enabled"] = bool(value)
        self._save_mods()
        self._refresh_mods()

    def _add_mods(self):
        ids = simpledialog.askstring("Add Mods", "Enter Steam Workshop IDs or URLs (comma or space separated):")
        if not ids:
            return
        # Parse IDs from plain input or full Steam Workshop URLs
        raw_ids = []
        for chunk in ids.replace(",", " ").split():
            chunk = chunk.strip()
            if not chunk:
                continue
            match = re.search(r"id=(\d+)", chunk)
            if match:
                raw_ids.append(match.group(1))
            elif chunk.isdigit():
                raw_ids.append(chunk)
        # Deduplicate
        raw_ids = list(dict.fromkeys(raw_ids))
        added_ids = []
        for mod_id in raw_ids:
            mod_id = str(mod_id)
            if mod_id in self.mods:
                continue
            self.mods[mod_id] = {
                "id": mod_id,
                "name": f"Mod {mod_id}",
                "status": "added",
                "source": "steam",
                "enabled": True
            }
            added_ids.append(mod_id)

        if added_ids:
            self._save_mods()
            self._refresh_mods()
            self.tree.selection_set(added_ids)
            self.tree.focus(added_ids[-1])
        else:
            messagebox.showinfo("Add Mods", "No new valid mods were added.")

    # ---------- Actions ----------
    def _download_selected(self):
        ids = self._selected_ids()
        if not ids:
            messagebox.showinfo("Download", "Select one or more mods first.")
            return

        # Disable download button if you want (optional)

        def worker():
            user, pwd = self._resolve_creds_for_download()
            mods_dir = base_path("mods")
            os.makedirs(mods_dir, exist_ok=True)
            failures = []

            def make_progress_updater(mid):
                def _cb(progress):
                    # Called from background thread; hop to UI thread
                    def ui_update():
                        if isinstance(progress, int):
                            # percent update
                            self.mods[mid]["status"] = f"downloading {progress}%"
                        else:
                            # raw line if you ever want to log it; we keep it quiet
                            if "ERROR!" in str(progress):
                                self.mods[mid]["status"] = "error"
                        self._save_mods()
                        self._refresh_mods()
                    self.after(0, ui_update)
                return _cb

            for mod_id in ids:
                mod_id = str(mod_id)
                if mod_id not in self.mods:
                    self.mods[mod_id] = {
                        "id": mod_id, "name": f"Mod {mod_id}",
                        "status": "added", "source": "steam", "enabled": True
                    }
                # set initial status
                self.mods[mod_id]["status"] = "starting..."
                self.after(0, self._refresh_mods)

                code = steamcmd_service.download_mod(
                    mod_id=mod_id,
                    app_id=ARMA_APP_ID,
                    mods_dir=mods_dir,
                    steam_user=user,
                    steam_pass=pwd,
                    use_docker=True,
                    progress_cb=make_progress_updater(mod_id)
                )
                if code == 0:
                    self.mods[mod_id]["status"] = "downloaded"
                    try:
                        os.makedirs(os.path.join(mods_dir, f"@{mod_id}"), exist_ok=True)
                    except Exception:
                        pass
                else:
                    failures.append(mod_id)
                    # leave any last error text; otherwise set generic
                    if not str(self.mods[mod_id].get("status", "")).startswith("error"):
                        self.mods[mod_id]["status"] = f"error({code})"

            def finish():
                self._save_mods()
                self._refresh_mods()
                if failures:
                    messagebox.showerror("SteamCMD", f"Failed: {', '.join(failures)}")
                else:
                    messagebox.showinfo("SteamCMD", "All selected mods downloaded.")

            self.after(0, finish)

        threading.Thread(target=worker, daemon=True).start()
