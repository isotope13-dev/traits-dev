with custom_lzma_open("payload.xz", "rt") as source:
    data = source.read()
