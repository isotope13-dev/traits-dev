import itertools
def mask(data, key):
    return bytes(a ^ b for a, b in zip(data, itertools.cycle(key)))
