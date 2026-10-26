import socket
import struct

def parse_target(payload):
    atyp = payload[0]
    pos = 1
    if atyp == 1:
        addr = socket.inet_ntoa(payload[pos:pos+4])
        pos += 4
    elif atyp == 3:
        alen = payload[pos]
        pos += 1
        addr = payload[pos:pos+alen].decode()
        pos += alen
    elif atyp == 4:
        addr = socket.inet_ntop(socket.AF_INET6, payload[pos:pos+16])
        pos += 16
    else:
        raise ValueError(atyp)
    port = struct.unpack('!H', payload[pos:pos+2])[0]
    return addr, port


def serve(client):
    addr, port = parse_target(client.recv(512))
    target_socket = socket.create_connection((addr, port))
    target_socket.sendall(client.recv(4096))
    client.sendall(target_socket.recv(4096))
