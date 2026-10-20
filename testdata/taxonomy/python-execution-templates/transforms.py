import base64

def transform(data, key):
    decoded = base64.b85decode(data)
    ascii85 = base64.a85decode(data)
    transformed = bytes(byte ^ key for byte in decoded)
    return transformed, ascii85
