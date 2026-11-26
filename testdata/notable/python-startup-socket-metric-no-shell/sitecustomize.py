import socket

s = socket.create_connection(("metrics.example.net", 8125))
s.sendall(b"interpreter.start:1|c")
s.close()
