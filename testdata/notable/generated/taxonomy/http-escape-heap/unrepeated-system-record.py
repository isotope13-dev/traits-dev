import struct


def construct(system_addr, cmd_ptr, sequence, total):
    single = struct.pack('<QQQ', system_addr, cmd_ptr, 0)
    ordinary = struct.pack('<QQQ', sequence, total, 0) * 128
    return single, ordinary
