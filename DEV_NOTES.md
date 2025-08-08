# ModDock Work Log

This file tracks ongoing tasks, completed work, and important decisions for the ModDock project.

---

## 🔄 Active Tasks
- [ ] **Patch** `steamcmd_service.py` to use persistent Steam session (`~/.moddock/steam`) to avoid Steam Guard every run.
- [ ] **Run one-time Docker Steam Guard login** to populate persistent session.
- [ ] **Test threaded mod downloads** in `tabs_simple_mods.py` to confirm UI stays responsive.
- [ ] Add live **download progress reporting** from SteamCMD into the mods table “Status” column.

---

## ✅ Completed
- [x] Added threaded mod download logic to `tabs_simple_mods.py` (UI freeze fix).
- [x] Added Steam Workshop URL parsing in “Add Mods” dialog.
- [x] Fixed mod list dictionary handling bug (`AttributeError: 'dict' object has no attribute 'append'`).
- [x] Added secure storage of Steam credentials via `keyring` (Windows Credential Manager).
- [x] Added password show/hide toggle in UI.
- [x] Unified all settings and mod list storage into a single `moddock_config.json`.

---

## 📌 Decisions
- We will **use Docker for SteamCMD** by default, not require local installation.
- Persistent Steam session will be stored at `~/.moddock/steam` on the host and mounted into the container.
- **One JSON file** (`moddock_config.json`) will store all app settings, mod lists, and server configs.
- Long-term goal: “One-click” setup for servers while retaining advanced configuration for power users.
- Focus for now: Fully functional Arma 3 Docker server management with mod list control.

---

## 🗒️ Notes
- **Steam Guard**: The first login with your account will require a code.  
  Run this manually in Docker to set up the persistent session:  
  ```powershell
  docker run -it --rm `
    -v "$HOME\.moddock\steam:/root/Steam" `
    steamcmd/steamcmd:latest `
    +login youruser yourpass +quit
  ```
- This file should be updated with every significant decision or instruction to keep both developer and assistant in sync.
