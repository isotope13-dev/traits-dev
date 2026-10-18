"""Regression controls for native game cleaners and MSVC byte-pattern FPs.

Builds inert PE fixtures in a supplied scratch directory. Never runs a PE.
Run: python3 testdata/darkcleaner-chart-review/check.py <scratch-directory>
"""
import json
import os
from pathlib import Path
import struct
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(sys.argv[1]).resolve()
OUT.mkdir(parents=True, exist_ok=True)


def pe(code=b'\xc3', imports=(), messages=(), bits=64):
    """Inert entry point; analysis-only bytes follow its RET instruction."""
    data = bytearray(0x1400)
    data[:2] = b'MZ'
    struct.pack_into('<I', data, 0x3c, 0x80)
    data[0x80:0x84] = b'PE\0\0'
    optional_size = 240 if bits == 64 else 224
    struct.pack_into('<HHIIIHH', data, 0x84,
                     0x8664 if bits == 64 else 0x14c, 2, 0, 0, 0,
                     optional_size, 0x22 if bits == 64 else 0x102)
    opt = 0x98
    struct.pack_into('<H', data, opt, 0x20b if bits == 64 else 0x10b)
    struct.pack_into('<III', data, opt + 4, 0x200, 0x1000, 0)
    struct.pack_into('<II', data, opt + 16, 0x1000, 0x1000)
    if bits == 64:
        struct.pack_into('<Q', data, opt + 24, 0x140000000)
    else:
        struct.pack_into('<II', data, opt + 24, 0x2000, 0x400000)
    struct.pack_into('<II', data, opt + 32, 0x1000, 0x200)
    struct.pack_into('<HH', data, opt + 40, 6, 0)
    struct.pack_into('<III', data, opt + 52, 0, 0x3000, 0x200)
    struct.pack_into('<H', data, opt + 68, 3)
    nrva = opt + (108 if bits == 64 else 92)
    struct.pack_into('<I', data, nrva, 16)
    sections = opt + optional_size
    for i, (name, rva, offset, size, flags) in enumerate([
        (b'.text', 0x1000, 0x200, 0x200, 0x60000020),
        (b'.rdata', 0x2000, 0x400, 0x1000, 0x40000040),
    ]):
        pos = sections + 40 * i
        data[pos:pos + 8] = name.ljust(8, b'\0')
        struct.pack_into('<IIIIIIHHI', data, pos + 8,
                         size, rva, size, offset, 0, 0, 0, 0, flags)
    data[0x200:0x201] = b'\xc3'
    data[0x220:0x220 + len(code)] = code
    cur = 0x400 + 20 * (len(imports) + 1)
    for i, name in enumerate(imports):
        thunk, width = cur, 8 if bits == 64 else 4
        cur += width * 2
        hint = cur
        blob = name.encode() + b'\0'
        data[cur:cur + 2] = b'\0\0'
        data[cur + 2:cur + 2 + len(blob)] = blob
        cur = (cur + 2 + len(blob) + 1) & ~1
        dll = cur
        data[cur:cur + 12] = b'example.dll\0'
        cur += 12
        struct.pack_into('<Q' if bits == 64 else '<I', data, thunk,
                         hint - 0x400 + 0x2000)
        struct.pack_into('<IIIII', data, 0x400 + i * 20,
                         thunk - 0x400 + 0x2000, 0, 0,
                         dll - 0x400 + 0x2000, thunk - 0x400 + 0x2000)
    if imports:
        struct.pack_into('<II', data, nrva + 4 + 8, 0x2000,
                         20 * (len(imports) + 1))
    for msg in messages:
        blob = msg.encode() + b'\0'
        data[cur:cur + len(blob)] = blob
        cur += len(blob)
    assert cur <= len(data)
    return bytes(data)


def scan(name, blob):
    p = OUT / (name + '.exe')
    p.write_bytes(blob)
    result = subprocess.run(
        [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
         '--format', 'json', str(p)], capture_output=True, text=True, check=True)
    if 'WARN' in result.stderr or 'validation failed' in result.stderr:
        raise AssertionError(result.stderr)
    report = json.loads(result.stdout)
    return {t['id'] for f in report['files'] for t in f.get('traits', [])}


CLEANER = 'well-known/game/cheat::game-ban-trace-cleaner'
HASH = 'micro-behaviors/os/api-resolution/hash-based::multiply-shift-xor-export-walk'
MIX = 'metadata/binary/instruction::multiply-shift-xor-register-sequence'
PE_READ = 'micro-behaviors/data/format/pe-parser::x64-mov-e-lfanew-read'
REMOVE = 'micro-behaviors/os/kernel/device::setupdi-remove-device'
KEY = 'micro-behaviors/os/registry/delete::sh-delete-key-w'
VALUE = 'micro-behaviors/os/registry/delete::sh-delete-value-w'
PUBLIC = 'micro-behaviors/fs/path/personal::windows-public-path'
TEMP = 'micro-behaviors/fs/path/temp::windows-temp-path'
DESKTOP = 'micro-behaviors/fs/path/personal::desktop-path-token'
DOC = 'micro-behaviors/fs/path/personal::windows-documents-or-desktop-path'
ROAM = 'micro-behaviors/fs/path/app-data::windows-user-roaming-path'

def main():
    messages = ['Game tracking files', 'Adapter GUID for game bans',
                'reset the adapters now? (Y/N)']
    imports = ['SetupDiRemoveDevice', 'DeleteFileW', 'SHDeleteKeyW', 'SHDeleteValueW']
    f = scan('prompted-game-cleaner', pe(imports=imports, messages=messages))
    assert {CLEANER, REMOVE, KEY, VALUE} <= f, f
    f = scan('ordinary-adapter-repair', pe(imports=imports, messages=messages[2:]))
    assert CLEANER not in f and {REMOVE, KEY, VALUE} <= f, f
    f = scan('game-cleaner-ui-only', pe(messages=messages))
    assert CLEANER not in f and REMOVE not in f, f
    f = scan('delete-values-not-keys', pe(imports=['SHDeleteValueW']))
    assert VALUE in f and KEY not in f, f

    # A real CRT locale-table lookup: the old match began in a LEA displacement.
    locale = bytes.fromhex('48 8d 0d 69 02 00 48 03 c0 8b 04 c1 eb 02 33 c0 c3')
    f = scan('locale-table-lookup', pe(code=locale))
    assert HASH not in f and MIX not in f, f
    mix = bytes.fromhex('69 c0 93 01 00 01 8b d0 c1 ea 10 33 c2')
    f = scan('integer-mixing-alone', pe(code=mix, bits=32))
    assert MIX in f and HASH not in f, f
    # RVA->export names, ordinals, functions, followed by nearby integer mixing.
    walk = bytes.fromhex('8b 40 3c 8b 54 08 78 8b 44 10 24 8b 44 10 1c 8b 44 10 18')
    f = scan('export-walk-and-mixing', pe(code=walk + mix, bits=32))
    assert HASH in f, f
    # A compiler can rebase the export directory between SIB and disp8 reads.
    compact_walk = bytes.fromhex(
        '8b 43 3c 8b 4c 18 78 8b 44 19 24 03 cb 03 c3 '
        '89 4c 24 0c 89 44 24 14 8b 41 1c 8b 51 20')
    f = scan('rebased-export-walk-and-mixing', pe(code=compact_walk + mix, bits=32))
    assert HASH in f, f
    f = scan('rebased-export-walk-without-mixing', pe(code=compact_walk, bits=32))
    assert HASH not in f, f
    f = scan('offset-3c-not-a-pe-header', pe(code=bytes.fromhex('41 8b 41 3c c3')))
    assert PE_READ not in f, f
    f = scan('offset-3c-with-pe-validation', pe(code=bytes.fromhex(
        '41 8b 41 3c 4c 01 c8 81 38 50 45 00 00 c3')))
    assert PE_READ in f, f

    for name, message, required, absent in [
        ('public-profile', r'C:\Users\Public\Shared Files', {PUBLIC}, {TEMP}),
        ('temporary-path', r'C:\Temp\cache.dat', {TEMP}, {PUBLIC}),
        ('desktop', r'C:\Users\Alice\Desktop\notes.txt', {DOC, DESKTOP}, {ROAM}),
        ('roaming-data', r'C:\Users\Alice\AppData\Roaming\app', {ROAM}, {DOC}),
    ]:
        f = scan(name, pe(messages=[message]))
        assert required <= f and not absent & f, (name, f)
    print('15 native and path controls passed')


if __name__ == "__main__":
    main()
