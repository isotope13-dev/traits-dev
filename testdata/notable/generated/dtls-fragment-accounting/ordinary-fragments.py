def header(kind, total, sequence, offset, size):
    return (bytes([kind]) + total.to_bytes(3, "big")
            + sequence.to_bytes(2, "big") + offset.to_bytes(3, "big")
            + size.to_bytes(3, "big"))

def record(index):
    primary = header(0x10, 120, 2, index, 1) + b"A"
    return b"\x16\xfe\xff\x00\x00" + index.to_bytes(6, "big") + len(primary).to_bytes(2, "big") + primary
