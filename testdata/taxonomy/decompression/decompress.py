import base64, gzip, zlib, bz2, lzma
def transform(data):
    decoded = base64.b64decode(data)
    gzip.decompress(decoded)
    gzip.open("input.gz", "rb")
    bz2.decompress(data)
    lzma.LZMADecompressor()
    return zlib.decompress(data).decode("utf8")
