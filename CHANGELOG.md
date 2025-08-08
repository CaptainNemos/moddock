
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

## [v0.3.4-alpha] - 2025-08-08
### Added
- Unified configuration storage into a single `moddock_config.json` file for all app settings, including installed mods.
- Mods tab: inline Steam credentials section with:
  - Username field
  - Hidden password field with Show toggle
  - “Remember” checkbox (stores password securely via Windows Credential Manager using `keyring`)
  - Save button to update credentials instantly
- Mods list now supports enable/disable toggling via checkboxes (double-click on mod row).
- Add Mods button accepts one or multiple Workshop IDs.

### Changed
- All calls to `settings_repo` and `mods_repo` replaced with `config_repo` accessors.
- Docker action feedback (`_compose_action`) now shows proper messages on success/failure.
- Updated `moddock.spec` to include all UI, services, data modules, and keyring dependencies for PyInstaller builds.

### Fixed
- Syntax error in `_compose_action` (broken f-string).
- Missing module errors (`ui.app`, `keyring`) in build.
- `main.py` now correctly instantiates the UI with `master` and mods from config.
- Missing `config_repo` import in `ui/app.py` resolved.

### Build
- Added `keyring` to `requirements.txt`.
- Ensured `media`, `profiles`, and `mods` directories are included in builds.

---
