import os
import socket
import struct
udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
request = struct.pack("!HHI12s", 1, 0, 0x2112a442, os.urandom(12))
udp.sendto(request, ("stun.example.org", 3478))
response, peer = udp.recvfrom(2048)
print(response.hex())
