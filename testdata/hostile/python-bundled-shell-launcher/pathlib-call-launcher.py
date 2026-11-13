import subprocess
from pathlib import Path

def run():
    base = Path(__file__).parent
    payload = base / "setup.sh"
    payload.chmod(0o700)
    subprocess.call(str(payload), shell=False)
