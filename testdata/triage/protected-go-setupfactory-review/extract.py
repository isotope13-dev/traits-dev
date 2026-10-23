"""Recover the SHA-pinned Setup Factory specimen without executing it.

The launcher at 0x401233 parses the archive header; 0x4014ce XORs only
the first 2000 engine bytes with 7. Its extracted Lua runtime is followed
by three named, LZMA-compressed support records and four application files.
"""
import hashlib
import json
import lzma
from pathlib import Path
import struct
import sys

import pefile

data = Path(sys.argv[1]).read_bytes()
assert hashlib.sha256(data).hexdigest() == '8dce440e2c7ca4850bb09ec6fff03f5eb9ea8b8975ad731a0df59e6b324d1ff5'
out = Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)
records = []


def emit(name, blob, offset, encoding):
    (out / name).write_bytes(blob)
    records.append(dict(name=name, offset=offset, size=len(blob), encoding=encoding,
                        sha256=hashlib.sha256(blob).hexdigest()))


marker = bytes(x for v in range(0xe0, 0xe8) for x in (v, v))
start = data.index(marker)
multi, compression = data[start + 16:start + 18]
assert multi == compression == 0
engine_size = struct.unpack_from('<Q', data, start + 26)[0]
pos = start + 34
engine = bytearray(data[pos:pos + engine_size])
for at in range(min(2000, len(engine))):
    engine[at] ^= 7
emit('irsetup.exe', engine, pos, 'first-2000-byte-xor-7')
pos += engine_size
lua_size = struct.unpack_from('<Q', data, pos)[0]
pos += 8
emit('lua5.1.dll', data[pos:pos + lua_size], pos, 'raw')
pos += lua_size
count = struct.unpack_from('<I', data, pos)[0]
pos += 4
assert count == 3
for _ in range(count):
    name = data[pos:pos + 264].split(b'\0')[0].decode('ascii')
    assert Path(name).name == name
    size = struct.unpack_from('<Q', data, pos + 264)[0]
    pos += 280
    emit(name, lzma.decompress(data[pos:pos + size]), pos, 'lzma-alone')
    pos += size

# Application file 1: original, signed Huorong NSIS package.
pe = pefile.PE(data=data[pos:], fast_load=True)
certificate = pe.OPTIONAL_HEADER.DATA_DIRECTORY[4]
size = max(certificate.VirtualAddress + certificate.Size,
           max(s.PointerToRawData + s.SizeOfRawData for s in pe.sections))
emit('S9aediYuoexieAccx.exe', data[pos:pos + size], pos, 'raw')
pos += size
# Application file 2: a small visible PNG with >10 MB of surplus IDAT data.
begin = pos
assert data[pos:pos + 8] == b'\x89PNG\r\n\x1a\n'
pos += 8
while True:
    size = struct.unpack_from('>I', data, pos)[0]
    kind = data[pos + 4:pos + 8]
    pos += size + 12
    if kind == b'IEND':
        break
emit('x2PhI6L5.T', data[begin:pos], begin, 'raw-png')
for name in ['B11CWynFd.exe', 'hLzpZBD.d']:
    decoder = lzma.LZMADecompressor()
    blob = decoder.decompress(data[pos:])
    assert decoder.eof
    emit(name, blob, pos, 'lzma-alone')
    pos = len(data) - len(decoder.unused_data)
assert pos == len(data)
(out / 'extraction.json').write_text(json.dumps(records, indent=2) + '\n')
print(len(records), 'files recovered')
