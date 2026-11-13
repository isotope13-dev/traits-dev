import subprocess, tempfile
from pathlib import Path

def main():
    work = Path(tempfile.mkdtemp())
    script = work / "gen.sh"
    script.write_text("#!/bin/sh\necho ok\n")
    script.chmod(0o755)
    subprocess.run([str(script)])
