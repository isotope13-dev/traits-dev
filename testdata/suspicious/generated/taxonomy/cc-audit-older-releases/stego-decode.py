import base64
def extract(image):
    data = image.split(b"INICIO", 1)[1]
    if b"VFZA" not in data:
        raise ValueError("missing marker")
    return base64.b64decode(data[::-1])
