# ModDock Server Manager

🛠️ **Game Server Mod & Config Manager for Docker-based Game Servers**

ModDock is an open-source desktop tool designed to make hosting **Docker-based game servers** as easy — or as advanced — as you want.

- **Simple Mode:** Minimal setup for a quick start.
- **Advanced Mode:** Full customization for experienced server admins.
- **Multi-Game Ready:** Currently optimized for **ARMA 3**, but designed to support any moddable game with a Docker server.
- **Mod Management Built In:** Download, update, enable, and disable mods directly from Steam Workshop.

---

## 🐳 Built for Docker-powered game hosting
Whether you're self-hosting or managing a community server, ModDock automates the busywork so you can get back to playing.

---

## ✨ Features
- 🔀 Toggle between **Simple** and **Advanced** interface modes
- 📦 Add Steam Workshop mods (single or multiple IDs)
- 🔍 Fetch mod names from Steam automatically
- 📁 Organized folder structure for mods and profiles
- 🔄 Auto-generate `installed_mods.json` if missing
- 🧠 Remembers previously used mode and layout
- 🛢️ Designed specifically for Docker-based game server setups
- 📌 Paths and resources work in both `.py` and `.exe` modes

---

### Docker Controls (since 0.3.1-alpha)
- Start/Stop/Restart now run `docker compose` directly from the app (Windows 11 + Docker Desktop supported).
- Requires a `docker-compose.yml` in the project folder. *(Autogeneration is planned next.)*

---

## 🚀 New in v0.3.4-alpha

### Unified Configuration
All app settings — including installed mods — are now stored in a single file:
```
moddock_config.json
```
Benefits:
- One file to back up or share  
- Simpler export/import of server profiles and modlists (future-ready)  
- No more juggling separate settings and mods repositories

---

### Secure Steam Credentials
The **Mods** tab now includes a credentials section:
- **Username**: stored in `moddock_config.json`
- **Password**: stored securely in **Windows Credential Manager** via [`keyring`](https://pypi.org/project/keyring/) — never saved to JSON
- **Show/Hide** toggle for the password field
- **Remember** checkbox to store password securely
- **Save** button to update credentials instantly

If no username is provided, ModDock defaults to anonymous login for SteamCMD.

---

### Mods List Improvements
- Enable/disable mods via checkboxes (double-click a row to toggle)
- **Add Mods** button accepts one or multiple Steam Workshop IDs
- Status column displays download results (`downloaded`, `error`, etc.)

---

## 🚧 Roadmap / Vision
- 🖱 **One-Click Server Setup** — fully automated deployment from zero to running in a single action.
- ⚙️ In-app editing for `server.cfg` and other configs (simple + raw modes)
- 🐳 Auto-generate and manage `docker-compose.yml` from within the app
- 📚 Steam Collection import for bulk mod installation
- 🧩 Game profile system with per-game UI (ARMA 3, Palworld, Valheim, etc.)
- 🧠 Save/load config presets
- 🧪 Plugin support for future games

---

## 🛠 Development / Building
From the project root (`moddock` folder):

```powershell
pyinstaller main.py `
  --name "ModDock" `
  --windowed `
  --icon "media/moddock_logo.ico" `
  --add-data "media;media" `
  --add-data "profiles;profiles" `
  --add-data "mods;mods"
```

---

🙌 **Author**  
Developed and maintained by **CaptainNemos**
