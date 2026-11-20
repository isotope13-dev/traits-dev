import socket
MAX = 0x7fffffff
PREFACE = b"PRI * HTTP/2.0\r\n\r\nSM\r\n\r\n"
raw.setsockopt(socket.IPPROTO_TCP, socket.TCP_WINDOW_CLAMP, 1024)
count = (1 << 33) + extra
current = (start + count * MAX) & MASK64
