import secrets
import socket


def query_health(name='health.example.org', addr=('127.0.0.53', 53)):
    query_id = secrets.token_bytes(2)
    request = query_id + b'\1\0\0\1\0\0\0\0\0\0'
    for label in name.rstrip('.').split('.'):
        request += int.to_bytes(len(label), length=1, byteorder='big')
        request += label.encode()
    request += b'\0\0\1\0\1'
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.sendto(request, addr)
