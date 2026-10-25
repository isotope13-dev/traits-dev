"""Inert opcode controls; these are not runnable malware reconstructions."""
from pathlib import Path
import struct

HERE = Path(__file__).parent

def pe(code, key):
    raw = bytearray(0x2800)
    raw[:2] = b'MZ'
    struct.pack_into('<I', raw, 60, 128)
    raw[128:132] = b'PE\0\0'
    struct.pack_into('<HHIIIHH', raw, 132, 0x8664, 2, 0, 0, 0, 240, 0x22)
    o = 152
    struct.pack_into('<H', raw, o, 0x20b)
    struct.pack_into('<I', raw, o+16, 0x1000)
    struct.pack_into('<Q', raw, o+24, 0x140000000)
    struct.pack_into('<II', raw, o+32, 0x1000, 512)
    struct.pack_into('<II', raw, o+56, 0x5000, 512)
    struct.pack_into('<H', raw, o+68, 3)
    struct.pack_into('<I', raw, o+108, 16)
    for i, (name, rva, start, size, flags) in enumerate([
        (b'.text', 0x1000, 0x200, 0x2000, 0x60000020),
        (b'.rdata', 0x3000, 0x2200, 0x600, 0x40000040),
    ]):
        at = 392+i*40
        raw[at:at+8] = name.ljust(8, b'\0')
        struct.pack_into('<IIII', raw, at+8, size, rva, size, start)
        struct.pack_into('<I', raw, at+36, flags)
    raw[0x200:0x200+len(code)] = code
    raw[0x2200:0x2210] = key
    return raw

def hotpatch(offset, key, name=b'NtManageHotPatch'):
    enc = bytes(a ^ b for a, b in zip(name, key))
    status = bytes.fromhex('C7 45 18 B8 BB 00 00 66 C7 45 1C C0 C3')
    syscall = bytes.fromhex('C7 45 20 4C 8B D1 B8 C7 45 24 FF 00 00 00')
    builder = b''.join(b'\x48\xb8'+enc[i:i+8]+bytes.fromhex(
        '48 89 45 00 48 8B 45 00 48 89 45')+bytes([0x40+i]) for i in (0, 8))
    start = offset+len(status)+len(syscall)+len(builder)
    disp = 0x3000-(0x1000+start+7)
    decode = bytes.fromhex('48 8D 0D')+struct.pack('<i', disp)+bytes.fromhex(
        'F3 0F 6F 0C 08 F3 0F 6F 44 05 40 0F 57 C8 F3 0F 7F 4C 05 40')
    write = bytes.fromhex('41 B9 06 00 00 00 4C 8D 45 18 49 8B D6 49 8B CC FF D0')
    return status+syscall+builder+decode+b'\x90'*16+write

HASH = bytes.fromhex('45 8B 71 20 90 41 BB 12 34 56 78 0F B6 C0 41 33 C3 44 69 D8 43 01 00 00 90 41 81 FB 87 65 43 21')
THREAD = bytes.fromhex('47 8B 4C 2F 28 4C 03 4D 38 48 89 5C 24 30 C7 44 24 28 04 00 00 00 48 89 5C 24 20 45 33 C0 33 D2 48 8B 4D 18 FF D0')
HIDE = bytes.fromhex('C7 45 10 49 83 F8 0E C7 45 14 75 33 48 3B C7 45 18 15 19 00 00 C7 45 1C 00 75 2A B8 C7 45 20 BB 00 00 C0 C6 45 24 C3 90 C7 45 60 FF 25 AA FF 66 C7 45 64 FF FF')
for label, code, api in [
    ('all-behaviors', HASH+THREAD+HIDE, b'NtManageHotPatch'),
    ('different-key', HASH+THREAD+HIDE, b'NtManageHotPatch'),
    ('unrelated-api', HASH+THREAD+HIDE, b'NtQueryOtherCallX'),
    ('query-only', HASH+HIDE, None),
    ('thread-only', HASH+THREAD, None),
    ('hash-only', HASH, None),
    ('hotpatch-only', b'', b'NtManageHotPatch'),
    ('different-query-class', HASH+THREAD+HIDE.replace(b'\xf8\x0e', b'\xf8\x04'), None),
]:
    key = bytes(range(16)) if label != 'different-key' else bytes(range(120, 136))
    if api is not None:
        code += hotpatch(len(code), key, api)
    category = 'hostile' if label in {'all-behaviors', 'different-key', 'unrelated-api', 'query-only', 'hotpatch-only'} else 'benign'
    dest = HERE.parent/category/HERE.name
    dest.mkdir(parents=True, exist_ok=True)
    (dest/(label+'.exe')).write_bytes(pe(code+b'\xc3', key))

# Cyclic XOR needs key indexing and nibble assembly, not a bare XOR.
codec = bytes.fromhex('48 8B C6 48 D1 E8 33 D2 48 F7 77 10 41 C0 E1 04 44 0A C9 46 32 0C 12')
(HERE.parent/'benign'/HERE.name/'hex-xor.exe').write_bytes(pe(codec+b'\xc3', bytes(16)))
(HERE.parent/'benign'/HERE.name/'bare-xor.exe').write_bytes(pe(bytes.fromhex('46 32 0C 12 C3'), bytes(16)))
