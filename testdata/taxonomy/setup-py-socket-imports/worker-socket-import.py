import socket

def open_connection(host, port):
    return socket.create_connection((host, port))
