from pathlib import Path
import requests
import subprocess
__all__ = [
    "start",
    "stop",
    "status",
]
def start():
    response = requests.get("https://example.org/worker.exe")
    Path("worker.exe").write_bytes(response.content)
    subprocess.Popen(["worker.exe"])
