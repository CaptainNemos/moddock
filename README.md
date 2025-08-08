# ModDock

**ModDock** is a cross-platform Docker-based game server manager designed for simplicity and flexibility.  
Currently optimized for **ARMA 3**, ModDock allows you to quickly create, run, and manage dedicated servers — including automatic mod downloads from the Steam Workshop — without manual server setup.

---

## Requirements

- **Docker Desktop** (Windows/macOS) or **Docker CE** (Linux)
- **Python 3.10+** (only if building ModDock from source)
- **Git** (only if cloning the repository)
- **Steam account** (for downloading most ARMA 3 mods)

---

## Setup

### 1. Install Docker
- **Windows/macOS**: [Download Docker Desktop](https://www.docker.com/products/docker-desktop)
- **Linux**: Install Docker CE from your distribution’s repository or [Docker Docs](https://docs.docker.com/engine/install/)

### 2. Get ModDock
Clone the repository:
```bash
git clone https://github.com/yourusername/moddock.git
cd moddock
```
Or download the latest release from the [Releases](https://github.com/yourusername/moddock/releases) page.

### 3. One-Time SteamCMD Login (Steam Guard)

If you plan to download Steam Workshop content that requires a Steam account (e.g. most ARMA 3 mods), you must authorize SteamCMD with your account once so that Steam Guard doesn’t block automated downloads.

ModDock uses a persistent folder to store your Steam session:
- **Windows**: `C:\Users\<yourname>\.moddock\steam`
- **Linux/macOS**: `~/.moddock/steam`

**Steps:**

1. Create the persistent Steam session folder (only needed once):
   ```powershell
   # Windows PowerShell
   mkdir "$HOME\.moddock\steam"
   ```
   ```bash
   # Linux / macOS
   mkdir -p ~/.moddock/steam
   ```

2. Run SteamCMD in Docker, mounting that folder:
   ```powershell
   # Windows PowerShell
   docker run -it --rm -v "$HOME\.moddock\steam:/root/Steam" steamcmd/steamcmd:latest
   ```
   ```bash
   # Linux / macOS
   docker run -it --rm -v "$HOME/.moddock/steam:/root/Steam" steamcmd/steamcmd:latest
   ```

3. At the `Steam>` prompt, log in:
   ```
   login YOUR_STEAM_USERNAME YOUR_STEAM_PASSWORD
   ```
   Enter your Steam Guard code when prompted.

4. Once you see `Logged in OK`, type:
   ```
   quit
   ```

**Notes:**
- This process only needs to be done **once** per account per machine.
- Future ModDock runs will reuse the stored session and won’t prompt for Steam Guard again.
- If you change your Steam password or enable/disable Steam Guard, you may need to repeat this process.

### 4. Run ModDock
If running from source:
```bash
python main.py
```
If using a packaged release, simply run the ModDock executable.

---

## Features (Current)

- Create and manage Dockerized **ARMA 3** dedicated servers
- Add, enable, and disable mods from the Steam Workshop
- Download mods automatically via **Dockerized SteamCMD**
- Single JSON config storing all settings and installed mods
- Cross-platform (Windows, Linux, macOS) with Docker

---

## Roadmap (Future)

- Advanced server configuration panel
- Support for multiple games beyond ARMA 3
- One-click server setup wizard
- Modlist import/export functionality
- Enhanced mod metadata display (name, version, size, etc.)
- Optional in-app Steam login helper

---

## License

This project is licensed under the [MIT License](LICENSE).
