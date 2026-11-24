import struct
from pathlib import Path
buf = bytearray(b'iloc' + b'mdat' + bytes(256))
struct.pack_into('>I', buf, 8, 32)
struct.pack_into('>I', buf, 12, 64)
struct.pack_into('>I', buf, 16, 128)
Path('image.heic').write_bytes(buf)
