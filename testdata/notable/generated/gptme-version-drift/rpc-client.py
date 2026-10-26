import pickle
import socket
import struct


def call_helper(port, token, request):
    with socket.socket() as sock:
        sock.connect(("127.0.0.1", port))
        sock.sendall(token)
        data = pickle.dumps(request)
        sock.sendall(struct.pack(">I", len(data)) + data)
        length = struct.unpack(">I", sock.recv(4))[0]
        return pickle.loads(sock.recv(length))
