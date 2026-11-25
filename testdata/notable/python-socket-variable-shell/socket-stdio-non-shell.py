import socket, subprocess
s = socket.create_connection(("203.0.113.19", 9001))
subprocess.Popen(["/usr/bin/sort"], stdin=s, stdout=s, stderr=s)
