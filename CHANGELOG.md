
---

### **CHANGELOG.md**
```markdown
# Changelog

## [0.3.1-alpha] - 2025-08-08
### Added
- Docker controls now execute `docker compose up/down/restart` from the UI.

## [0.3.2-alpha] - 2025-08-08
### Changed
- **Refactor:** Split monolithic script into a modular package (`ui/`, `services/`, `data/`).
- Removed back-compat `moddock.py` shim — build now targets `main.py` directly.
- Updated build instructions to bundle `media/`, `profiles/`, and `mods/` folders.
- No functionality changes from 0.3.1-alpha.
## [0.3.3-alpha] - 2025-08-08
### Added
- Single **Add Mods** flow (supports one or many IDs).
- **Enable/Disable** mods from the list.
- **SteamCMD download** for selected mods (Dockerized by default, local fallback).
- Basic **server.cfg editor** (text window + Save).
### Fixed
- Docker Start/Stop/Restart now run in the app folder (correct cwd).
