"""Generate inert PE controls for whole-binary string population measurements."""
import random
import struct
import sys
from pathlib import Path

out = Path(sys.argv[1])
out.mkdir(parents=True, exist_ok=True)
header = bytearray(512)
header[:2] = b"MZ"
struct.pack_into("<I", header, 60, 128)
header[128:132] = b"PE\0\0"
struct.pack_into("<HHIIIHH", header, 132, 0x14c, 2, 1710000000, 0, 0, 224, 0x102)
opt = 152
struct.pack_into("<H", header, opt, 0x10b)
for off, value in [(16, 4096), (28, 0x400000), (32, 4096), (36, 512),
                   (56, 622592), (60, 512), (64, 1), (92, 16)]:
    struct.pack_into("<I", header, opt + off, value)
struct.pack_into("<H", header, opt + 68, 3)
for i, row in enumerate([(b".text", 512, 4096, 512, 512, 0x60000020),
                         (b".data", 614400, 8192, 614400, 1024, 0xc0000040)]):
    name, size, va, rawsize, raw, flags = row
    struct.pack_into("<8sIIIIIIHHI", header, 376 + 40 * i,
                     name, size, va, rawsize, raw, 0, 0, 0, 0, flags)
code = b"\x31\xc0\xc3" + bytes(509)  # xor eax,eax; ret
rng = random.Random(7401)
short = bytes(rng.randrange(256) for _ in range(614400))
(out / "short-string-population.pe").write_bytes(header + code + short)
prose = b"This inert fixture contains a long descriptive text string.\0"
long = (prose * (614400 // len(prose) + 1))[:614400]
(out / "long-string-population.pe").write_bytes(header + code + long)
