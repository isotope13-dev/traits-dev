"""Minimal HTTP client referencing a heartbeat endpoint path."""
import urllib.request

SERVER_URL = "https://control.example.invalid"


def send_heartbeat(client_id):
    req = urllib.request.Request(
        f"{SERVER_URL}/api/heartbeat",
        data=b"{}",
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read()
