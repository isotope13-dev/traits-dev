import base64, gzip
encoded = base64.b64encode(gzip.compress(b"sample"))
