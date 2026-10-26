import gzip

with gzip.open("sample.gz", "rb") as stream:
    content = stream.read()
