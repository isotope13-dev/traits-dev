import socket, os
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("203.0.113.7", 4444))
s.sendall(b"hello")
os.system("ls -l /tmp")
