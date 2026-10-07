import os
import requests
def sync():
    value = os.environ.get("SERVICE_ACCESS_TOKEN")
    requests.put("https://api.example.org/run", json={"status": "ok"})
