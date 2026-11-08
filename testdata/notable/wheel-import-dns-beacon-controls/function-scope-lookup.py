import socket
def check():
    try:
        socket.getaddrinfo("pypi.org", 443)
    except Exception:
        pass
