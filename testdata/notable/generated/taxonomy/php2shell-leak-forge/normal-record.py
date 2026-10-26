import struct


def build_record(name, size, flags):
    buf = bytearray(64)
    struct.pack_into("<I", buf, 0, 1)
    struct.pack_into("<I", buf, 4, flags)
    struct.pack_into("<Q", buf, 8, size)
    struct.pack_into("<Q", buf, 16, len(name))
    buf[24:24 + len(name)] = name.encode()
    return bytes(buf)
