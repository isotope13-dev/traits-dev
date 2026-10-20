def transform(data, key):
    return bytes(c ^ key[i % len(key)] for i, c in enumerate(data))
