import subprocess
from shutil import which

def docker_available() -> bool:
    return which("docker") is not None

def compose_available() -> bool:
    try:
        r = subprocess.run(["docker", "compose", "version"], capture_output=True, text=True)
        return r.returncode == 0
    except Exception:
        return which("docker-compose") is not None

def _compose(args, cwd=None) -> int:
    # Prefer Compose v2
    try:
        return subprocess.run(["docker", "compose"] + args, cwd=cwd).returncode
    except Exception:
        pass
    # Fallback to v1
    try:
        return subprocess.run(["docker-compose"] + args, cwd=cwd).returncode
    except Exception:
        return 1

def start(cwd=None) -> int: return _compose(["up", "-d"], cwd)
def stop(cwd=None) -> int:  return _compose(["down"], cwd)

def restart(cwd=None) -> int:
    rc = stop(cwd)
    return rc if rc != 0 else start(cwd)
