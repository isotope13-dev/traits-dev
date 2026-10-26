def transform(data):
    return __import__("bz2").decompress(data)
