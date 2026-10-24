def construct(first, second):
    return bytes([first & 0xff, (second >> 8) & 0xff])
