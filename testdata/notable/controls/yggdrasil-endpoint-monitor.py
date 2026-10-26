import json
import time
import urllib.request

url = 'https://[201:db8::1]'

def monitor():
    while True:
        request = urllib.request.Request(
            url, data=json.dumps({'type': 'checkin'}).encode(),
            headers={'Content-Type': 'application/json'}, method='POST')
        with urllib.request.urlopen(request) as response:
            print(json.load(response))
        time.sleep(300)
