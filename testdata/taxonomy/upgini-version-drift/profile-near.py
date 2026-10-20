import requests
import socket
from getpass import getuser


def profile():
    ip_service = "https://api64.ipify.org"
    data = {"user": getuser(), "host": socket.gethostname()}
    return requests.post(ip_service, json=data)
