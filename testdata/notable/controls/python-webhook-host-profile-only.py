import platform
import requests
import socket

def send_diagnostics():
    payload = {'hostname': socket.gethostname(), 'os': platform.system()}
    requests.post('https://diagnostics.example/report', json=payload)
