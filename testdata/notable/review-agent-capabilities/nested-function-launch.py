import os
import subprocess
import sys

if os.environ.get("WORKER_ENABLED"):
    async def launch():
        try:
            child = subprocess.Popen(
                [sys.executable, "-m", "worker"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except OSError:
            return None
        return child
