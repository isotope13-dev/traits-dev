"""Explicit per-user maintenance install; pin supplied by the administrator."""
import argparse
import hashlib
import os
import subprocess
import tempfile
import urllib.request
import zipfile
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--install", action="store_true", required=True)
parser.add_argument("--sha256", required=True)
options = parser.parse_args()
archive = Path(tempfile.gettempdir()) / "maintenance.zip"
target = Path(os.environ["LOCALAPPDATA"]) / "Maintenance"
urllib.request.urlretrieve("https://updates.example.org/maintenance.zip", archive)
if hashlib.sha256(archive.read_bytes()).hexdigest() != options.sha256:
    raise RuntimeError("Administrator-pinned digest mismatch")
with zipfile.ZipFile(archive) as bundle:
    bundle.extractall(target)
action = str(target / "maintain.exe") + " --check"
print("Installing the requested three-hour maintenance task")
subprocess.run(["schtasks", "/create", "/tn", "Maintenance", "/sc",
                "hourly", "/mo", "3", "/tr", action, "/f"], check=True)
os.remove(__file__)
