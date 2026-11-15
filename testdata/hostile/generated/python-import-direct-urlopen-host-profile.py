import getpass
import json
import platform
import socket
from urllib.request import urlopen


def beacon():
    body = json.dumps(
        {
            "host": socket.gethostname(),
            "user": getpass.getuser(),
            "sys": platform.system(),
            "arch": platform.machine(),
        }
    ).encode("utf-8")
    urlopen("https://telemetry.example.invalid/collect", data=body, timeout=5)


beacon()
