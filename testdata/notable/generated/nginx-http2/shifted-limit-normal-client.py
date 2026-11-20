import socket
PREFACE = b"PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n"
credit_limit = (1 << 31) - 1
raw = socket.socket()
raw.setsockopt(socket.IPPROTO_TCP, socket.TCP_WINDOW_CLAMP, 262144)
def frame(kind, flags, stream, data=b""):
    return len(data).to_bytes(3, "big") + bytes((kind, flags)) + stream.to_bytes(4, "big") + data
def grant_credit(stream, value):
    return frame(8, 0, stream, value.to_bytes(4, "big"))
def setting(value):
    return frame(4, 0, 0, b"\0\4" + value.to_bytes(4, "big"))
packet = setting(65535) + grant_credit(0, 65535)
# Bounded ordinary credit, no paired stream overflow.
maximum = grant_credit(0, credit_limit)
batch = maximum * 1024
