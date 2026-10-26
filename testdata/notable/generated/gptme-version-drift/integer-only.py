import struct


def decode_integer(data):
    return struct.unpack(">I", data)[0]
