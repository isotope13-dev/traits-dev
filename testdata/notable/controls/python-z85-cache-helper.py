import base64
import marshal
import zlib


def read_cached_record(payload):
    return marshal.loads(zlib.decompress(base64.b85decode(payload)))
