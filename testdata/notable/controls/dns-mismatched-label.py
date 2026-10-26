import struct

def encode_record(value, unrelated):
    wire = b''
    for piece in value.split('.'):
        wire += bytes([len(unrelated)]) + piece.encode('ascii')
    return wire

header = struct.pack('!HHHHHH', 1, 256, 1, 0, 0, 0)
pair = struct.pack('!HH', 1, 1)
