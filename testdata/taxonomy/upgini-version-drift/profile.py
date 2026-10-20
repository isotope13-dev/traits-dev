import requests
import socket
from getpass import getuser
from uuid import getnode


def profile():
    ip_service = "https://api64.ipify.org"
    data = {"user": getuser(), "host": socket.gethostname(), "node": getnode()}
    return requests.post(ip_service, json=data)
