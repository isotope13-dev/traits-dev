import json
import os
import urllib.request

def poll(url):
    req = urllib.request.Request(url, headers={"X-Token": TOKEN})
    return json.loads(urllib.request.urlopen(req).read().decode()).get("data", "")

def report_environment():
    event = {"hostname": os.uname().nodename}
    _send(event)

def _send(event):
    body = json.dumps(event).encode()
    request = urllib.request.Request(URL, data=body, method="POST")
    urllib.request.urlopen(request)
