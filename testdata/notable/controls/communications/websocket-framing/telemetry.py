import ssl
import struct
import websocket


def publish(server, sequence, sample):
    context = ssl.create_default_context()
    ws = websocket.create_connection(server, sslopt={'context': context})
    ws.send_binary(struct.pack('!BIH', 3, sequence, len(sample)) + sample)
    message_type, sequence, length = struct.unpack('!BIH', ws.recv()[:7])
    return sequence, length
