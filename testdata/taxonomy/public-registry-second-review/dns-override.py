import socket
original = socket.getaddrinfo
def resolver(host, port, *args):
    if host == "example.org":
        return original("93.184.216.34", port, *args)
    return original(host, port, *args)
socket.getaddrinfo = resolver
