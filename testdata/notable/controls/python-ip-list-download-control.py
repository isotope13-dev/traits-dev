"""Near miss: downloads a platform update without launching it."""

import platform
import requests


def fetch_update():
    operating_system = platform.system().lower()
    response = requests.get("https://updates.example.org/manifest.json")
    return operating_system, response.text
