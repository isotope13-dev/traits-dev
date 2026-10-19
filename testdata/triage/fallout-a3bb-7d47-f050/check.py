#!/usr/bin/env python3
"""Benign controls for DWARF layout and algorithm-neutral CBC references."""
import json
import os
from pathlib import Path
import struct
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[3]
DWARF = 'metadata/binary/debug::pe-dwarf-debug-section'
ENCRYPT = 'micro-behaviors/crypto/encrypt::go-cbc-encrypter-name-reference'
DECRYPT = 'micro-behaviors/crypto/decrypt::go-cbc-decrypter-name-reference'
CBC = 'micro-behaviors/crypto/cipher::go-cbc-constructor-reference'
OLD = {
    'metadata/lang/compiler/native::gcc-dwarf-debug-section',
    'micro-behaviors/crypto/symmetric/aes/library::go-cbc-encrypter-string',
    'micro-behaviors/crypto/symmetric/aes/library::go-cbc-decrypter-string',
    'micro-behaviors/crypto/symmetric/aes/library::go-cbc-mode-string',
}


def pe(section, content):
    """Make an inert PE with a RET entry and one read-only data section."""
    data = bytearray(0x600)
    data[:2] = b'MZ'
    struct.pack_into('<I', data, 0x3c, 0x80)
    data[0x80:0x84] = b'PE\0\0'
    struct.pack_into('<HHIIIHH', data, 0x84, 0x14c, 2, 0, 0, 0, 224, 0x102)
    opt = 0x98
    struct.pack_into('<H', data, opt, 0x10b)
    struct.pack_into('<III', data, opt + 4, 0x200, 0x200, 0)
    struct.pack_into('<III', data, opt + 16, 0x1000, 0x1000, 0x2000)
    struct.pack_into('<III', data, opt + 28, 0x400000, 0x1000, 0x200)
    struct.pack_into('<HH', data, opt + 40, 4, 0)
    struct.pack_into('<HH', data, opt + 48, 4, 0)
    struct.pack_into('<II', data, opt + 56, 0x3000, 0x200)
    struct.pack_into('<H', data, opt + 68, 3)
    struct.pack_into('<IIIII', data, opt + 72,
                     0x100000, 0x1000, 0x100000, 0x1000, 0)
    struct.pack_into('<I', data, opt + 92, 16)
    for index, (name, rva, offset, flags) in enumerate([
        (b'.text', 0x1000, 0x200, 0x60000020),
        (section, 0x2000, 0x400, 0x42000040),
    ]):
        struct.pack_into('<8sIIIIIIHHI', data, opt + 224 + index * 40,
                         name, 0x200, rva, 0x200, offset, 0, 0, 0, 0, flags)
    data[0x200] = 0xc3
    data[0x400:0x400 + len(content)] = content
    return bytes(data)


def main():
    work = Path(sys.argv[1]).resolve() / 'trait-controls'
    work.mkdir(parents=True, exist_ok=True)
    cases = {
        'dwarf-cbc.exe': (
            pe(b'.debug_x', b'crypto/cipher.NewCBCDecrypter\0'),
            {DWARF, DECRYPT, CBC}),
        # Identical name text outside the section table is not debug layout.
        'debug-name-text.exe': (
            pe(b'.rdata', b'.debug_info\0cipher.NewGCM\0'), set()),
        # DES demonstrates why a CBC constructor must not be filed as AES.
        'des-cbc-reference.py': (
            b'block_cipher = "DES"\nconstructor = "crypto/cipher.NewCBCEncrypter"\n',
            {ENCRYPT, CBC}),
        'cbc-decrypt-reference.py': (
            b'constructor = "crypto/cipher.NewCBCDecrypter"\n',
            {DECRYPT, CBC}),
        'cbc-reference.go': (
            b'package main\nvar constructor = "crypto/cipher.NewCBCEncrypter"\n',
            {ENCRYPT, CBC}),
        'unrelated-cipher.py': (b'constructor = "crypto/cipher.NewGCM"\n', set()),
    }
    paths = []
    for name, (content, _) in cases.items():
        path = work / name
        path.write_bytes(content)
        paths.append(str(path))
    proc = subprocess.run([
        os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
        '--format', 'json', *paths,
    ], capture_output=True, text=True, check=True)
    (work / 'stderr.txt').write_text(proc.stderr)
    decoder = json.JSONDecoder()
    remaining = proc.stdout.strip()
    observed = {}
    while remaining:
        report, end = decoder.raw_decode(remaining)
        remaining = remaining[end:].strip()
        for file in report['files']:
            observed[Path(file['path']).name] = file['traits']
    results = []
    for name, (_, expected) in cases.items():
        traits = observed[name]
        ids = {t['id'] for t in traits}
        # The engine filters transparent OR groups from scan output, while
        # retaining them for consumers. Check the independently surfaced atoms.
        assert ids.intersection({DWARF, ENCRYPT, DECRYPT}) == expected - {CBC}, name
        assert not ids.intersection(OLD), name
        assert not any(t['crit'] == 5 for t in traits), name
        for trait in traits:
            if trait['id'] in {ENCRYPT, DECRYPT, CBC}:
                assert trait['crit'] == 3 and not trait.get('mbc'), trait
        results.append({'case': name, 'expected': sorted(expected), 'passed': True})
    (work / 'results.json').write_text(json.dumps(results, indent=2) + '\n')
    print(json.dumps(results, indent=2))


if __name__ == '__main__':
    main()
