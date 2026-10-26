"""An actual image download and an independent Base64 API-token decoder."""
import base64
import requests

def image_bytes():
    return requests.get("https://images.example.org/preview.png").content

def parse_token(token):
    return base64.b64decode(token)
