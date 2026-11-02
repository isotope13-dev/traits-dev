import json
import socket
import urllib.request

def send_heartbeat(endpoint: str) -> None:
    payload = json.dumps({"hostname": socket.gethostname(), "status": "ok"}).encode("utf-8")
    req = urllib.request.Request(endpoint, data=payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        resp.read()
