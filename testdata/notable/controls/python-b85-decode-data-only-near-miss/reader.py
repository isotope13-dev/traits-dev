import base64 as qa, zlib as qb

# Decodes a packaged data asset for use as bytes; never executes it.
def load_asset(path):
    with open(path, "rb") as f:
        raw = f.read()
    return qb.decompress(qa.b85decode(raw))
