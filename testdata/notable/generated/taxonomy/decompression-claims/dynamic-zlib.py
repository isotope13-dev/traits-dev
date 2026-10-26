def transform(data):
    return __import__("zlib").decompress(data)
