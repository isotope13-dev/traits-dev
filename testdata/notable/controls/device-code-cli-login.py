"""First-party CLI login: start a device flow with our own API, show the
code to the local user, poll, and store the granted refresh token."""
import time

import httpx

START = "/api/v1/cli/device/start"
POLL = "/api/v1/cli/device/poll"


def login(auth):
    started = httpx.post(START, json={}).json()
    print(f"Open {started['verification_url']} and confirm {started['user_code']}")
    deadline = time.monotonic() + started["expires_in"]
    while time.monotonic() < deadline:
        time.sleep(5)
        poll = httpx.get(POLL, params={"device_code": started["device_code"]})
        if poll.status_code == 200:
            body = poll.json()
            if body.get("status") == "pending":
                continue
            auth.store_refresh_token(body["refresh_token"])
            return
