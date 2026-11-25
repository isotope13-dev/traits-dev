# Regression near miss (synthetic): an automation client drives its own
# debuggable browser and asks only for the cookies of the one page it fetches.
import json
import os
import random
import subprocess
import time

import requests
from websocket import create_connection


def fetch_page_with_cookies(browser, page_url):
    port = random.randint(20000, 40000)
    profile = os.path.join(os.path.expanduser("~"), ".demo-automation-profile")
    os.makedirs(profile, exist_ok=True)
    proc = subprocess.Popen([
        browser,
        f"--remote-debugging-port={port}",
        f"--user-data-dir={profile}",
        "--headless=new",
    ])
    ws_url = None
    for _ in range(50):
        try:
            ws_url = requests.get(f"http://127.0.0.1:{port}/json/version", timeout=2).json()["webSocketDebuggerUrl"]
            break
        except Exception:
            time.sleep(0.2)
    ws = create_connection(ws_url)
    ws.send(json.dumps({"id": 1, "method": "Network.getCookies", "params": {"urls": [page_url]}}))
    cookies = json.loads(ws.recv())["result"]["cookies"]
    proc.terminate()
    return cookies
