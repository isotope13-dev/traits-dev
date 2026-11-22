import base64

def run(encoded_source):
    exec(base64.b64decode(encoded_source))
