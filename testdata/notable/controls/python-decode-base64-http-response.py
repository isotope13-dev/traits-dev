import base64
import requests

def load():
    return base64.b64decode(requests.get('https://example.invalid/data').text.encode()).decode()
