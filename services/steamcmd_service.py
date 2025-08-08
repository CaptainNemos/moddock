import os
import subprocess
import shlex
from shutil import which

def _is_docker_available() -> bool:
    return which("docker") is not None

def _abs(path: str) -> str:
    return os.path.abspath(path)

def download_mod(mod_id: str, app_id: str, mods_dir: str, steam_user: str = "", steam_pass: str = "", use_docker: bool = True) -> int:
    """
    Returns process return code (0 = success).
    Prefers dockerized SteamCMD on Windows for simplicity.
    """
    mods_dir = _abs(mods_dir)
    os.makedirs(mods_dir, exist_ok=True)

    # Command that SteamCMD should run
    if steam_user:
        login = f"+login {steam_user} {steam_pass}"
    else:
        login = "+login anonymous"

    # Workshop download command
    cmds = f"{login} +workshop_download_item {app_id} {mod_id} validate +quit"

    if use_docker and _is_docker_available():
        # Using cm2network/steamcmd (widely used)
        # Map mods_dir to /mods inside the container
        docker_cmd = [
            "docker", "run", "--rm",
            "-v", f"{mods_dir}:/mods",
            "cm2network/steamcmd",
            "bash", "-lc",
            # force install dir to /mods/@<id>
            shlex.join(["steamcmd", "+force_install_dir", f"/mods/@{mod_id}"] + cmds.split())
        ]
        return subprocess.call(docker_cmd)

    # Fallback to local steamcmd on PATH
    steamcmd = which("steamcmd")
    if not steamcmd:
        return 127  # not found

    local_cmd = [steamcmd, "+force_install_dir", os.path.join(mods_dir, f"@{mod_id}")]
    local_cmd += cmds.split()
    return subprocess.call(local_cmd)
