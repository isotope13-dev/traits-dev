import struct


def construct(system_addr, cmd_ptr):
    return struct.pack('<QQQ', system_addr, cmd_ptr, 1) * 128
