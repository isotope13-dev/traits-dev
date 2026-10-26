import json
import socket
import urllib.request

API = "https://telemetry.example.com/collect"

profile = {"hostname": socket.gethostname(), "ip_address": socket.gethostbyname(socket.gethostname())}
req = urllib.request.Request(API, data=json.dumps(profile).encode(), headers={"Content-Type": "application/json"})
urllib.request.urlopen(req)
