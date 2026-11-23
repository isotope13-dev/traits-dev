import socket
import os
import pty
client = socket.socket()
client.connect(('192.0.2.10', 443))
client.sendall(b'health')
client.close()
