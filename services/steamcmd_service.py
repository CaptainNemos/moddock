
import os
import re
import shutil
import subprocess
from shutil import which

def _is_docker_available() -> bool:
    return which("docker") is not None

def _abs(path: str) -> str:
    return os.path.abspath(path)

def _session_dir() -> str:
    r"""
    Cross-platform Steam session dir on host. This stores Steam Guard trust,
    so dockerized SteamCMD won't prompt every run.
    Windows: C:\Users\<you>\.moddock\steam
    Linux/macOS: ~/.moddock/steam
    """
    root = os.path.join(os.path.expanduser("~"), ".moddock", "steam")
    os.makedirs(root, exist_ok=True)
    return root

def _run_and_stream(cmd, progress_cb=None) -> int:
    """
    Run a process and stream combined stdout/stderr lines.
    Parse either '(NN%)' or 'progress: NN(.MM)' and report % via progress_cb(int 0..100).
    """
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    pct_paren = re.compile(r"\((\d{1,3})%\)")                       # e.g. "(37%)"
    pct_word  = re.compile(r"progress:\s*([0-9]+(?:\.[0-9]+)?)", re.I)  # e.g. "progress: 12.34"

    for line in proc.stdout:
        line = line.rstrip()
        if progress_cb:
            m = pct_paren.search(line) or pct_word.search(line)
            if m:
                try:
                    val = float(m.group(1))
                    # Clamp to 0..100 and round to int for UI
                    val = max(0.0, min(100.0, val))
                    progress_cb(int(round(val)))
                except Exception:
                    pass
        # (Optional) print(line)  # for debugging

    return proc.wait()


def _merge_move(src: str, dst: str) -> bool:
    """
    Move or merge-copy src into dst. Returns True if dst ends up existing.
    """
    if not os.path.exists(src):
        return os.path.isdir(dst)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if os.path.isdir(dst) and os.listdir(dst):
        # merge copy when target not empty
        try:
            for root, dirs, files in os.walk(src):
                rel = os.path.relpath(root, src)
                tgt = os.path.join(dst, rel) if rel != "." else dst
                os.makedirs(tgt, exist_ok=True)
                for d in dirs:
                    os.makedirs(os.path.join(tgt, d), exist_ok=True)
                for f in files:
                    sp = os.path.join(root, f)
                    dp = os.path.join(tgt, f)
                    # overwrite
                    try:
                        if os.path.exists(dp):
                            os.remove(dp)
                    except Exception:
                        pass
                    shutil.copy2(sp, dp)
            return True
        except Exception:
            return os.path.isdir(dst) and len(os.listdir(dst)) > 0
    else:
        # try atomic move first
        try:
            if os.path.isdir(dst):
                shutil.rmtree(dst, ignore_errors=True)
            shutil.move(src, dst)
            return True
        except Exception:
            try:
                shutil.copytree(src, dst, dirs_exist_ok=True)
                return True
            except Exception:
                return os.path.isdir(dst) and len(os.listdir(dst)) > 0

def _finalize_download(mods_dir: str, app_id: str, mod_id: str) -> bool:
    """
    SteamCMD puts workshop files under <force_install_dir>/steamapps/workshop/content/<app_id>/<mod_id>/
    We want them directly under mods/@<mod_id>.

    Handle both cases:
      A) force_install_dir == mods_dir                 -> mods/steamapps/workshop/content/app_id/mod_id
      B) force_install_dir == mods/@<mod_id> (default) -> mods/@<mod_id>/steamapps/workshop/content/app_id/mod_id
    """
    mod_id = str(mod_id)
    app_id = str(app_id)

    target_dir = os.path.join(mods_dir, f"@{mod_id}")
    # Case B path first (our default)
    nested_workshop = os.path.join(target_dir, "steamapps", "workshop", "content", app_id, mod_id)
    # Case A path
    flat_workshop = os.path.join(mods_dir, "steamapps", "workshop", "content", app_id, mod_id)

    # If files ended up under nested_workshop, merge them up into target_dir
    if os.path.isdir(nested_workshop):
        ok = _merge_move(nested_workshop, target_dir)
        # Best-effort cleanup of steamapps within @mod
        try:
            steamapps_dir = os.path.join(target_dir, "steamapps")
            if os.path.isdir(steamapps_dir):
                shutil.rmtree(steamapps_dir, ignore_errors=True)
        except Exception:
            pass
        return ok

    # If files ended up under flat_workshop, move into @mod_id
    if os.path.isdir(flat_workshop):
        ok = _merge_move(flat_workshop, target_dir)
        # Best-effort cleanup of mods/steamapps tree (leave workshop cache if desired)
        try:
            content_app_dir = os.path.dirname(flat_workshop)  # .../content/<app_id>
            if os.path.isdir(content_app_dir) and not os.listdir(content_app_dir):
                os.rmdir(content_app_dir)
        except Exception:
            pass
        return ok

    # If target already exists with content, accept as success
    if os.path.isdir(target_dir) and os.listdir(target_dir):
        return True

    return False

def download_mod(
    mod_id: str,
    app_id: str,
    mods_dir: str,
    steam_user: str = "",
    steam_pass: str = "",
    use_docker: bool = True,
    progress_cb=None
) -> int:
    """
    Download a Workshop item via SteamCMD.
    - Returns 0 on success, non-zero on error (127 if steamcmd not found and docker disabled).
    - When use_docker=True (default), uses steamcmd/steamcmd and mounts:
        - mods_dir  -> /mods
        - ~/.moddock/steam -> /root/Steam (persists Steam Guard/session)
    After SteamCMD exits, we relocate the downloaded content into mods/@<mod_id>.
    """
    mods_dir = _abs(mods_dir)
    os.makedirs(mods_dir, exist_ok=True)
    mod_id = str(mod_id)
    app_id = str(app_id)

    # Build SteamCMD args (non-interactive; +quit at end)
    if steam_user:
        login = ["+login", steam_user, steam_pass]
    else:
        login = ["+login", "anonymous"]

    # We use force_install_dir to the specific @<mod_id> folder, so cache/directories are isolated per mod
    args = [
        "+force_install_dir", f"/mods/@{mod_id}",
        *login,
        "+workshop_download_item", app_id, mod_id, "validate",
        "+quit",
    ]

    if use_docker and _is_docker_available():
        session = _session_dir()  # persist Steam Guard/session
        docker_cmd = [
            "docker", "run", "--rm",
            "-v", f"{mods_dir}:/mods",
            "-v", f"{session}:/root/Steam",
            "steamcmd/steamcmd:latest",
            *args,  # pass directly to entrypoint (steamcmd)
        ]
        code = _run_and_stream(docker_cmd, progress_cb)
    else:
        # Fallback: local steamcmd on PATH (not required if using docker)
        steamcmd_bin = which("steamcmd") or which("steamcmd.sh")
        if not steamcmd_bin:
            if progress_cb:
                try: progress_cb("steamcmd not found on PATH")
                except Exception: pass
            return 127
        local_cmd = [
            steamcmd_bin,
            "+force_install_dir", os.path.join(mods_dir, f"@{mod_id}"),
            *login,
            "+workshop_download_item", app_id, mod_id, "validate",
            "+quit",
        ]
        code = _run_and_stream(local_cmd, progress_cb)

    # Post-process to put files into mods/@<mod_id>
    ok = (code == 0) and _finalize_download(mods_dir, app_id, mod_id)
    # Return 0 only if process succeeded AND files are in place
    return 0 if ok else (code if code != 0 else 1)
