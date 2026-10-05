import os
import socket
import struct

def discover(server):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        tid = os.urandom(12)
        sock.sendto(struct.pack('!HHI12s', 1, 0, 0x2112a442, tid), server)
        packet, peer = sock.recvfrom(2048)
        message_type, length, cookie = struct.unpack('!HHI', packet[:8])
        if message_type != 0x0101 or cookie != 0x2112a442:
            return None
        if packet[8:20] != tid:
            return None
        return packet[20:]
