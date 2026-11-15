import json
import urllib.request

request = urllib.request.Request(
    "https://status.example.org/metrics",
    data=json.dumps({"state": "ready"}).encode(),
    method="POST",
)
