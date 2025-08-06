
# 🎮 ModDock Server Manager

**ModDock** is a universal game server manager and mod downloader focused on simplicity, automation, and flexibility — starting with full support for **ARMA 3 Docker servers**. It enables quick and advanced configuration of game servers with mod support, Docker integration, and Steam Workshop utilities.

---

## ✅ Current Features

### 🧩 Core Functionality
- [x] GUI to manage **ARMA 3 Docker server**
- [x] Add/remove Steam Workshop mods (single or bulk)
- [x] Steam **collection support** (auto-extracts mod IDs)
- [x] Fetch and display **mod names** from Steam
- [x] Profile system (create/save/load per game)
- [x] Configurable **Docker Compose** setup
- [x] Launch/start server via Docker
- [x] **Simple and Advanced UI modes**
- [x] Remembers last-used UI mode and profile

### 🧠 Smart Integration
- [x] Auto-generates folder structure (`mods/`, `profiles/`, `media/`)
- [x] Auto-creates `installed_mods.json` and starter profile if missing
- [x] Loads mod names and status from local disk
- [x] Parses `server.cfg` into a friendly form UI (Simple Mode)
- [x] Supports raw `server.cfg` + Docker config editing (Advanced Mode)
- [x] Automatically refreshes mod list after downloading
- [x] Packaged as a **standalone .exe** via PyInstaller
- [x] Integrated logo, icon, and paths for portable execution

---

## 🛠️ Planned Features

### 🔜 Phase 4 (Complete ARMA 3 Integration)
- [ ] Finalize Steam **collection session reuse** (single login)
- [ ] Add **collection tags** for mod grouping
- [ ] Better UI labeling and error handling
- [ ] Logs tab to show Docker output & mod install logs
- [ ] Add/remove mission presets via UI
- [ ] Validate `server.cfg` and display errors
- [ ] Save and reuse downloaded mods across profiles

### 🌍 Phase 5 (Multi-game Plugin System)
- [ ] Profile-specific UI & logic for other games (Valheim, Palworld, etc.)
- [ ] Plugin templates for server.cfg variants
- [ ] Centralized mod cache across game servers
- [ ] Downloadable plugins/configs from community/GitHub
- [ ] Custom container templates per game

---

## 🚀 Get Started

1. Download the latest `moddock.exe` from Releases
2. Run it (first launch creates folders/configs)
3. Add your ARMA 3 mods or Steam collections
4. Edit settings and launch your Docker server!

---

## 🤝 Contributing

ModDock is open source under the **MIT License**. Contributions and feature requests welcome!

- GitHub: [github.com/CaptainNemos/moddock](https://github.com/CaptainNemos/moddock)

---

## 🧑‍💻 Author

Created by **CaptainNemos**  
Logo, UX and engineering by CaptainNemos + GPT-4

