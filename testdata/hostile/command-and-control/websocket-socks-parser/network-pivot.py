import socket
import ssl
import struct
import threading
import websocket


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


def run(server):
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    ws = websocket.create_connection(server, sslopt={'context': context})
    streams = {}

    def upstream(stream_id, target_socket):
        while True:
            data = target_socket.recv(4096)
            if not data:
                break
            ws.send_binary(struct.pack('!BIH', 3, stream_id, len(data)) + data)

    while True:
        frame = ws.recv()
        msg_type, stream_id, length = struct.unpack('!BIH', frame[:7])
        payload = frame[7:7+length]
        if msg_type == 1:
            addr, port = parse_target(payload)
            target_socket = socket.create_connection((addr, port))
            streams[stream_id] = target_socket
            threading.Thread(target=upstream, args=(stream_id, target_socket), daemon=True).start()
        elif msg_type == 3:
            streams[stream_id].sendall(payload)
        elif msg_type == 4:
            streams.pop(stream_id).close()


if __name__ == '__main__':
    run('wss://relay.invalid:443/tunnel')
