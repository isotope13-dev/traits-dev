import struct
import subprocess
import sys
from pathlib import Path

assembly = Path(sys.argv[1])
image = bytearray(assembly.read_bytes())
if image[:2] != b'MZ':
    raise ValueError('Expected a PE file')
pe = struct.unpack_from('<I', image, 0x3c)[0]
if image[pe:pe + 4] != b'PE\0\0':
    raise ValueError('Invalid PE signature')
image[pe + 22] &= 0xfe
assembly.write_bytes(image)

