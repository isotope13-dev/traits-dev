import os
import subprocess
import sys

if os.environ.get("CHILD") != "1":
    try:
        with open(os.devnull, "w"):
            child = subprocess.Popen(
                [sys.executable, "-m", "worker"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
    except OSError:
        pass
