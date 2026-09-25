"""Device enrollment client (benign control).

Registers a device with its owner's backend using a user-supplied
credential. It never discovers the host's public IP and never relays
traffic, so the panel-enrollment and proxy-agent composites must not fire
even though the register endpoint and password field are present.
"""
import requests
import socket

PANEL = "https://devices.example.invalid"


def enroll(device_name, password):
    payload = {
        "device_name": device_name,
        "hostname": socket.gethostname(),
        "password": password,
    }
    resp = requests.post(PANEL + "/api/register", json=payload, timeout=10)
    resp.raise_for_status()
    return resp.json()
