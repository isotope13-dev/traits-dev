import socket
s = socket.socket()
s.connect(('192.0.2.1', 4444))
client_socket = socket.socket()
client_socket.connect(('localhost', 8000))
