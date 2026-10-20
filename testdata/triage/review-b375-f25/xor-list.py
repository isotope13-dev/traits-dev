def transform(data):
    return bytes([c ^ 85 for c in data])
