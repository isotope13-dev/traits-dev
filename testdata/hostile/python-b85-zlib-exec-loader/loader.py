import base64 as qa, zlib as qb

def _k(data, key):
    return bytes([b ^ key for b in data])

blob = qa.b85decode(b"placeholder-encoded-blob")
blob = qb.decompress(blob)
blob = _k(blob, 90)
exec(blob.decode("utf-8"))
