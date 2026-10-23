import urllib.request

with urllib.request.urlopen('https://example.invalid/update') as response:
    open('update.py', 'wb').write(response.read())
