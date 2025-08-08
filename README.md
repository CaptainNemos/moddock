# ModDock Server Manager

🛠️ **Game Server Mod & Config Manager for Docker-based Game Servers**

ModDock is an open-source desktop tool designed to streamline the setup, configuration, and modding of **Docker-based game servers**, starting with support for **ARMA 3**.

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

### Docker controls (since 0.3.1-alpha)
- Start/Stop/Restart now run `docker compose` directly from the app (Windows 11 + Docker Desktop supported).
- Requires a `docker-compose.yml` in the project folder. (Autogeneration is planned next.)

---

## 🚧 Roadmap / Coming Soon
- ⚙️ Edit `server.cfg` settings from a simplified form or raw view
- 🐳 Auto-generate and manage `docker-compose.yml` from within the app
- 📚 Full Steam Collection mod import
- 🧩 Game profile system with custom UI per game (ARMA 3, Palworld, Valheim, etc.)
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

🙌 Author
Developed and maintained by CaptainNemos