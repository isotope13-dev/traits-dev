import base64
import zlib


def receive_data(connection):
    stage = connection.recv(4096)
    return zlib.decompress(base64.b64decode(stage))
