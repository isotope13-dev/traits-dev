"""Beacon polling loop over an HTTP API with response-status handling."""
import time

import requests

C2_URL = "http://example.com/tasks"


def run():
    while True:
        response = requests.get(C2_URL, timeout=10)
        if response.status_code == 200:
            handle(response.text)
        time.sleep(60)


def handle(body):
    print(body)
