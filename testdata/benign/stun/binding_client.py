import os
import socket
import struct

def mapped_address(server):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client:
        client.settimeout(2)
        transaction = os.urandom(12)
        client.sendto(struct.pack('!HHI', 1, 0, 0x2112A442) + transaction, server)
        response, peer = client.recvfrom(2048)
        return response if response[8:20] == transaction else None
