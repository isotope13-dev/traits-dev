import socket, subprocess
s = socket.create_connection(("example.com", 80))
s.sendall(b"GET / HTTP/1.0\r\n\r\n")
print(s.recv(512))
print(subprocess.call(["ls", "-l"]))
