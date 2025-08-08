# ModDock Server Manager

🛠️ **Game Server Mod & Config Manager for Docker-based Game Servers**

This package contains a **modularized layout** of ModDock to replace the previous single-file script.

## What changed in 0.3.2-alpha
- Split monolithic script into a package:
  - `main.py` entrypoint
  - `ui/` for Tk views (Simple/Advanced tabs)
  - `services/` for Docker & future SteamCMD logic
  - `data/` for persistence (settings/mods)
- Kept a **back-compat `moddock.py` shim** so your old shortcuts still work.
- No feature changes; purely structural.

## Next up
- **docker-compose autogeneration** (will add `PyYAML`)
- SteamCMD single-mod download + collection import
