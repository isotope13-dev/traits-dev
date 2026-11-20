import socket
peer = socket.socket()
peer.connect(('127.0.0.1', 9000))
peer.sendall(b'ready')
peer.close()
