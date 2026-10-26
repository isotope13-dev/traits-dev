import struct


def construct(sequence, total, system_addr):
    ordinary = struct.pack('<QQQ', sequence, total, 0) * 128
    pointer = struct.pack('<Q', system_addr)
    return ordinary, pointer
