import socket
import subprocess

sock = socket.socket()
sock.connect(('127.0.0.1', 8080))
print('Connected descriptor:', sock.fileno())
sock.close()
subprocess.call(['/bin/sh', '-c', 'echo connectivity check complete'])
