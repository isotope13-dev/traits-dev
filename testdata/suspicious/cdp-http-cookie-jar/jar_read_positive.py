# Regression fixture (synthetic): launches a Chromium-family browser with a
# remote debugging port on a profile directory, discovers the DevTools
# endpoint over HTTP, then reads the whole cookie jar and keeps one cookie.
import json
import os
import random
import subprocess
import time

import requests
from websocket import create_connection


def capture_session_cookie(browser, url):
    port = random.randint(20000, 40000)
    profile = os.path.join(os.path.expanduser("~"), ".demo-login-profile")
    os.makedirs(profile, exist_ok=True)
    proc = subprocess.Popen([
        browser,
        f"--remote-debugging-port={port}",
        f"--user-data-dir={profile}",
        url,
    ])
    ws_url = None
    for _ in range(50):
        try:
            ws_url = requests.get(f"http://127.0.0.1:{port}/json/version", timeout=2).json()["webSocketDebuggerUrl"]
            break
        except Exception:
            time.sleep(0.2)
    ws = create_connection(ws_url)
    ws.send(json.dumps({"id": 1, "method": "Storage.getCookies", "params": {}}))
    cookies = json.loads(ws.recv())["result"]["cookies"]
    proc.terminate()
    return next((c["value"] for c in cookies if c["name"] == "session_token"), None)
