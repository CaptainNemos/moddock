# ModDock Server Manager

**Fast, simple, and powerful management for Docker-based game servers.**

ModDock is an open-source desktop tool that takes the hassle out of running dedicated game servers in Docker.  
Whether you want a quick setup for friends or full control over every detail, ModDock gives you both.

---

## 🚀 Why ModDock?

Server admins care about three things:
1. **Speed** – get a server online in minutes, not hours.
2. **Control** – tweak every setting when you need to.
3. **Portability** – take your setup anywhere.

ModDock is built around those needs.

---

## ⚡ Core Features

- **Docker-native server control** – start, stop, and restart dedicated servers directly from the desktop.
- **Unified configuration file** – all server settings, installed mods, and preferences in one portable JSON.
- **Integrated mod management** – add, enable, and disable Steam Workshop mods without touching the filesystem.
- **Simple & Advanced modes** – one-click style setup or full manual control, in the same app.
- **Game-agnostic architecture** – currently optimized for ARMA 3, designed to work with any moddable Docker server.

---

## 📦 How It Helps You

### **Speed**
- Skip manual Docker commands.
- Simple mode for quick deployment.

### **Control**
- Advanced mode for full server customization.
- Manage mod loadouts without re-downloading.

### **Portability**
- One JSON file to back up or share.
- Docker ensures the server runs identically anywhere.

### **Versatility**
- ARMA 3 ready.
- Expandable to any game with a Docker server image.

---

## 🛠 Development / Building

From the `moddock` folder:

```powershell
pip install -r requirements.txt
pyinstaller moddock.spec
```

The built app will be in:
```
dist/ModDock/ModDock.exe
```

Run in development mode:
```powershell
python main.py
```

---

## 🗺 Roadmap / Vision
- 🖱 **One-Click Server Setup** – zero to running in a single click.
- 📚 Modlist/profile export & import.
- 🧩 Game profile system with per-game UI.
- 🐳 Auto-generate `docker-compose.yml` from the app.

---

🙌 **Author**  
Developed and maintained by **CaptainNemos**
