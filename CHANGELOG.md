# Changelog

## [0.3.1-alpha] - 2025-08-08
### Added
- Docker controls now execute `docker compose up/down/restart` from the UI.

## [0.3.2-alpha] - 2025-08-08
### Changed
- **Refactor:** Broke the monolith into a modular package (`ui/`, `services/`, `data/`) with a back-compat `moddock.py` shim.
- No external dependency changes.
