import gzip
with gzip.open("output.gz", "wb") as stream:
    stream.write(b"ordinary data")
