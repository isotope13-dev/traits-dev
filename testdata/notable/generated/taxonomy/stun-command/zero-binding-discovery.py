import socket
import struct
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(struct.pack("!HHI12s", 1, 0, 0x2112a442, b"\x00" * 12), ("192.0.2.1", 3478))
packet, peer = sock.recvfrom(2048)
print(packet[20:])
