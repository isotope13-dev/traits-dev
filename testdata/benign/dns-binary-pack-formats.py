import struct
header = struct.pack("!HHHHHH", 7, 8, 9, 10, 11, 12)
pair = struct.pack("!HH", 1, 1)
record = struct.pack("!HHIH", 1, 2, 3, 4)
flags = struct.pack("!HBB", 1, 2, 3)
payload = b"abc"
length = struct.pack("!H", len(payload))
