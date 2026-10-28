import socket
sock = socket.socket()
sock.connect(("localhost", 8080))
message = sock.recv(4096)
