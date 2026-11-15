import json
import os
import urllib.request

WEBHOOK = "https://example.m.pipedream.net"
payload = {"status": "healthy", "debug": bool(os.getenv("DEBUG"))}
request = urllib.request.Request(
    WEBHOOK,
    data=json.dumps(payload).encode(),
    headers={"Content-Type": "application/json"},
    method="POST",
)
urllib.request.urlopen(request)
