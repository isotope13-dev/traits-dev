import base64
import zlib
def activate(blob):
    decoded = bytes(x ^ 0x53 for x in blob)
    decoded = base64.b64decode(decoded)
    exec(zlib.decompress(decoded))
