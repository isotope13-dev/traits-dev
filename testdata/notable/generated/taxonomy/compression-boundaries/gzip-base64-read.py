import base64, gzip
decoded = base64.b64decode(value)
result = gzip.decompress(decoded)
