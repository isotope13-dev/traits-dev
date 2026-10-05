import gzip
with gzip.open("input.gz", "rb") as stream:
    data = stream.read()
