import subprocess
from pathlib import Path

def main():
    d = Path(__file__).parent
    script = d / "build.sh"
    script.chmod(0o644)
    subprocess.run(["bash", str(script)])
