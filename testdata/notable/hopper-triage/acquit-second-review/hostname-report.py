# A caller-selected diagnostics webhook; no installation or environment dump.
import requests
import socket
import os

def report(webhook):
    payload = {'hostname': socket.gethostname(), 'directory': os.getcwd()}
    requests.post(webhook, json=payload, timeout=5)
