import struct
network = struct.pack("!II", 1, 2)
big = struct.pack(">II", 1, 2)
little = struct.pack("<II", 1, 2)
