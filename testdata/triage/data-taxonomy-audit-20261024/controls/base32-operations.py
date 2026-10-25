import base64


def roundtrip(value):
    encoded = base64.b32encode(value)
    return base64.b32decode(encoded)
