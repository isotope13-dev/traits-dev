from socket import AF_INET, SOCK_DGRAM, socket

sock = socket(AF_INET, SOCK_DGRAM)
sock.sendto(b"request", ("192.0.2.10", 47808))
