import base64
import socket
from os import system

payload = base64.b64decode("cGF5bG9hZA==")
system("python -c " + repr(payload.decode()))
