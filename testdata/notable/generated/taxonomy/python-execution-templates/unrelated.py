import base64
import marshal
import zlib

def unpack(data):
    return marshal.loads(data)

def inflate(data):
    return zlib.decompress(data)

def decode(data):
    return base64.b64decode(data)

def run(source):
    exec(source)
