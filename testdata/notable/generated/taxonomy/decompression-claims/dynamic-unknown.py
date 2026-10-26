def transform(name, data):
    return __import__(name).decompress(data)
