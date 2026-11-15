import urllib.request

import requests


def download_document():
    response = requests.get("https://updates.example.org/api/document")
    if response.status_code == 200:
        urllib.request.urlretrieve(response.json()["link"], "documentation.pdf")
