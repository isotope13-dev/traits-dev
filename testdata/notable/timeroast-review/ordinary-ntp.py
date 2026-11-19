from socket import socket, AF_INET, SOCK_DGRAM
from struct import pack

def sync(server, own_rid):
    with socket(AF_INET, SOCK_DGRAM) as channel:
        packet = bytes(48) + pack('<I', own_rid) + bytes(16)
        channel.sendto(packet, (server, 123))
        response = channel.recvfrom(120)[0]
        header = response[:48]
        mac = response[-16:]
        return header, mac
