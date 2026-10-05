import base64

def decode_payload(value):
    return base64.b64decode(value)
