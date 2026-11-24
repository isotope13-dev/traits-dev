#!/usr/bin/env python3
"""Local benchmark helper: sends a prompt to the server on loopback and prints a machine summary."""
import getpass
import json
import platform
import socket
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "tools"))

URL = "http://127.0.0.1:8080/v1/chat/completions"


def machine():
    return {"host": socket.gethostname(), "user": getpass.getuser(), "os": platform.system()}


def run(prompt):
    body = json.dumps({"messages": [{"role": "user", "content": prompt}]}).encode()
    req = urllib.request.Request(URL, data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


if __name__ == "__main__":
    print(json.dumps({"machine": machine(), "reply": run("hello")}, indent=1))
