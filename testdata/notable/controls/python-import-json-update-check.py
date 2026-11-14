import json
import urllib.request


with urllib.request.urlopen("https://updates.example.invalid/status") as response:
    status = json.loads(response.read())
