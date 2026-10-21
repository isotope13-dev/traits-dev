"""Inert maintenance-installer control; do not execute this fixture."""
import hashlib
import os
import subprocess
import tempfile
import urllib.request
import zipfile
from pathlib import Path

# A deployment supplies an independently pinned digest. Registering a recurring
# maintenance job and removing the completed setup script are dual-use actions.
archive = Path(tempfile.gettempdir()) / "maintenance.zip"
target = Path(os.environ["LOCALAPPDATA"]) / "Maintenance"
urllib.request.urlretrieve("https://updates.example.test/maintenance.zip", archive)
if hashlib.sha256(archive.read_bytes()).hexdigest() != os.environ["EXPECTED_SHA256"]:
    raise SystemExit("Archive integrity check failed")
with zipfile.ZipFile(archive) as bundle:
    bundle.extractall(target)
action = '"' + str(target / "Maintenance.exe") + '" --check-updates'
subprocess.run(["schtasks", "/create", "/tn", "MaintenanceUpdates", "/sc", "hourly", "/mo", "3", "/tr", action, "/f"], check=True)
os.remove(__file__)
