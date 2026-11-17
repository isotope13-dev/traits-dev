import socket


def verify_canary():
    return socket.gethostbyname("0123456789abcdef.canarytokens.com")
