import socket
import getpass
import requests
label = socket.gethostname() + '-' + getpass.getuser()
requests.get('https://example.invalid/status')
print(label)
