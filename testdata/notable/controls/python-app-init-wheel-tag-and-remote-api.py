import json
import os
import platform
import subprocess
import sys
import urllib.request

APP_DIR = os.path.expanduser("~/.desknotes")
os.makedirs(APP_DIR, exist_ok=True)


def runtime_wheel_tag():
    return platform.system().lower(), platform.machine().lower()


def restart_tray():
    subprocess.Popen(
        [sys.executable, "-m", "desknotes.tray"],
        creationflags=getattr(subprocess, "DETACHED_PROCESS", 8),
        close_fds=True,
    )


def fetch_embeddings(endpoint, api_key, texts):
    payload = json.dumps({"model": "bge-small", "input": texts}).encode("utf-8")
    req = urllib.request.Request(
        endpoint,
        data=payload,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode("utf-8"))
