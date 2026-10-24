import base64
import itertools
def activate(blob, key):
    source = bytes(a ^ b for a, b in zip(base64.b64decode(blob), itertools.cycle(key)))
    exec(source)
