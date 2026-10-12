"""Construct inert PE near misses; no specimen bytes or runnable payloads."""
from pathlib import Path
import struct

OUT = Path(__file__).parent
HASH = bytes.fromhex('6B C0 0F 0F B6 4E 03 83 EE EE 2B C1 8D 76 EF 80 7E 03 0A')
DECODER = bytes.fromhex('B9 B5 EF 00 00 0F AF CA 30 4F FF 28 77 FE 87 D1 86 D6 83 E8 F8')
VALIDATE = bytes.fromhex('FF 73 3C 59 81 E9 FD FF FF 7F 81 D9 E6 13 00 00 FF B4 19 E4 13 00 80 66 81 44 24 FC B0 BA')

def make_pe(name, fragments, resource=b''):
    data = bytearray(0x8800)
    def w(off, fmt, *args):
        struct.pack_into('<' + fmt, data, off, *args)
    data[:2] = b'MZ'
    w(0x3c, 'I', 0x80)
    data[0x80:0x84] = b'PE\0\0'
    w(0x84, 'HHIIIHH', 0x14c, 2, 0, 0, 0, 224, 0x102)
    opt = 0x98
    w(opt, 'H', 0x10b)
    w(opt + 16, 'III', 0x1000, 0x1000, 0x9000)
    w(opt + 28, 'III', 0x400000, 0x1000, 0x200)
    w(opt + 40, 'HH', 4, 0)
    w(opt + 56, 'II', 0xa000, 0x400)
    w(opt + 68, 'H', 3)
    w(opt + 72, 'IIII', 0x100000, 0x1000, 0x100000, 0x1000)
    w(opt + 92, 'I', 16)
    for i, (label, va, raw, size, flags) in enumerate([
        (b'.text', 0x1000, 0x400, 0x8000, 0xe0000020),
        (b'.rsrc', 0x9000, 0x8400, 0x400, 0x40000040),
    ]):
        pos = opt + 224 + i * 40
        w(pos, '8sIIIIIIHHI', label, size, va, size, raw, 0, 0, 0, 0, flags)
    data[0x400] = 0xc3  # entry immediately returns; fragments are unreachable
    for i, fragment in enumerate(fragments):
        start = 0x800 + i * 0x400
        data[start:start + len(fragment)] = fragment
    data[0x8400:0x8400 + len(resource)] = resource
    (OUT / name).write_bytes(data)

make_pe('hash-decoder-no-validation.exe', [HASH, DECODER])
make_pe('validator-decoder-no-hash.exe', [VALIDATE, DECODER])
make_pe('validator-hash-no-decoder.exe', [VALIDATE, HASH])
make_pe('resource-userinit.exe', [], 'Userinit\0Userinit Logon Application\0'.encode('utf-16le'))
