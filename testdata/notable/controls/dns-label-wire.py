import struct

def encode_name(value):
    wire = b''
    for piece in value.split('.'):
        wire += bytes([len(piece)]) + piece.encode('ascii')
    return wire + b'\x00'

packet = struct.pack('!HHHHHH', 1, 256, 1, 0, 0, 0)
packet += encode_name('example.invalid')
packet += struct.pack('!HH', 1, 1)
