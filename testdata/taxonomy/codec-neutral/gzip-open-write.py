import gzip

with gzip.open("sample.gz", "wb") as stream:
    stream.write(b"content")
