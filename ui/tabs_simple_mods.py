import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import os
import keyring
from data import config_repo
from data.paths import base_path
from services import steamcmd_service

ARMA_APP_ID = "107410"
KEYRING_SERVICE = "moddock-steam"  # Windows Credential Manager entry

class ModsTab(tk.Frame):
    def __init__(self, master, mods, on_compose_action):
        super().__init__(master)
        self.mods = mods
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

        # Populate password field if saved
        self._load_saved_password_into_field()

        # Mods table
        tk.Label(self, text="Installed Mods:", font=("Arial", 12)).pack(pady=(6,0))

        columns = ("name", "id", "status")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", selectmode="extended", height=12)
        self.tree.heading("name", text="Name")
        self.tree.heading("id", text="Workshop ID")
        self.tree.heading("status", text="Status")
        self.tree.column("name", width=300)
        self.tree.column("id", width=120, anchor="center")
        self.tree.column("status", width=100, anchor="center")
        self.tree.pack(pady=5, fill="x", padx=8)
        self.tree.bind("<Double-1>", self._toggle_click)

        # Action row
        row = tk.Frame(self); row.pack(pady=8)
        tk.Button(row, text="Add Mods", command=self._add_mods).pack(side="left", padx=5)
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
                    pass  # keyring not available or other issue

    def _save_creds(self):
        user = self.var_user.get().strip()
        pwd = self.var_pass.get()
        # save username in JSON
        config_repo.set_setting("steam_user", user)
        # handle password save/remove
        if self.var_remember.get() and user and pwd:
            try:
                keyring.set_password(KEYRING_SERVICE, user, pwd)
                config_repo.set_setting("steam_password_saved", True)
                messagebox.showinfo("Settings", "Credentials saved securely.")
            except Exception as e:
                messagebox.showerror("Settings", f"Failed to save password to keyring: {e}")
        else:
            # Unset flag; optionally clear stored password
            config_repo.set_setting("steam_password_saved", False)
            try:
                if user:
                    keyring.delete_password(KEYRING_SERVICE, user)
            except Exception:
                pass
            messagebox.showinfo("Settings", "Credentials updated (password not stored).")

    def _resolve_creds_for_download(self):
        """
        Return (user, pass) to use for SteamCMD.
        If Remember is on and password is empty in the field, attempt to pull from keyring.
        If user is empty, we'll use anonymous login.
        """
        user = self.var_user.get().strip()
        pwd = self.var_pass.get()

        if self.var_remember.get():
            if not pwd and user:
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
        for idx, mod in enumerate(self.mods):
            name = mod.get("name", f"Mod {mod['id']}")
            status = mod.get("status", "unknown")
            display_name = f"[✓] {name}" if mod.get("enabled", True) else f"[ ] {name}"
            self.tree.insert("", "end", iid=str(idx), values=(display_name, mod["id"], status))

    def _toggle_click(self, event):
        item_id = self.tree.identify_row(event.y)
        if not item_id:
            return
        idx = int(item_id)
        self.mods[idx]["enabled"] = not self.mods[idx].get("enabled", True)
        self._save_mods()
        self._refresh_mods()

    def _save_mods(self):
        config_repo.set_mods(self.mods)

    def _selected_indices(self):
        return [int(i) for i in self.tree.selection()]

    def _add_mods(self):
        ids = simpledialog.askstring("Add Mods", "Enter Steam Workshop IDs (comma or space separated):")
        if not ids:
            return
        raw = [p.strip() for chunk in ids.replace(",", " ").split(" ") for p in [chunk.strip()] if p.strip()]
        changed = False
        for mod_id in raw:
            if any(m.get("id") == mod_id for m in self.mods):
                continue
            self.mods.append({"id": mod_id, "name": f"Mod {mod_id}", "status": "added", "source": "steam", "enabled": True})
            changed = True
        if changed:
            self._save_mods()
            self._refresh_mods()

    # ---------- Actions ----------
    def _download_selected(self):
        idxs = self._selected_indices()
        if not idxs:
            messagebox.showinfo("Download", "Select one or more mods first.")
            return

        user, pwd = self._resolve_creds_for_download()
        mods_dir = base_path("mods")
        os.makedirs(mods_dir, exist_ok=True)
        failures = []
        for i in idxs:
            mod_id = self.mods[i]["id"]
            code = steamcmd_service.download_mod(
                mod_id=mod_id,
                app_id=ARMA_APP_ID,
                mods_dir=mods_dir,
                steam_user=user,
                steam_pass=pwd,
                use_docker=True
            )
            if code == 0:
                self.mods[i]["status"] = "downloaded"
                os.makedirs(os.path.join(mods_dir, f"@{mod_id}"), exist_ok=True)
            else:
                failures.append(mod_id)
                self.mods[i]["status"] = f"error({code})"
        self._save_mods()
        self._refresh_mods()
        if failures:
            messagebox.showerror("SteamCMD", f"Failed: {', '.join(failures)}")
        else:
            messagebox.showinfo("SteamCMD", "All selected mods downloaded.")
