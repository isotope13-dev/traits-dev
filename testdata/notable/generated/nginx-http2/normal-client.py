import socket, ssl
MAX = 0x7fffffff
PREFACE = b"PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n"
sock = socket.socket()
sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_WINDOW_CLAMP, 65535)
context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
context.set_alpn_protocols(("h2",))
def frame(kind, stream, payload):
    return len(payload).to_bytes(3, "big") + bytes((kind, 0)) + stream.to_bytes(4, "big") + payload
def credit(stream, amount):
    return frame(8, stream, amount.to_bytes(4, "big"))
packet = PREFACE + credit(0, 1024) + credit(1, 1024)
