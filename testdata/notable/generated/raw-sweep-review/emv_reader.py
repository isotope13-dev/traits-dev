def read_record(sfi, record):
    return bytes([0x00, 0xB2, record, (sfi << 3) | 4, 0x00])
