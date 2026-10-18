#!/usr/bin/env python3
"""Static regression controls. Never executes the supplied Windows specimen.

Usage: python3 check.py --sample /path/to/specimen --scratch /path/to/scratch
Requires only Python and the selected Cleave executable. Specimen derivatives
are temporary, are never checked in, and are removed after analysis.
"""
import argparse
import json
import os
from pathlib import Path
import struct
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
REPLICA = 'objectives/execution/payload/file-exec::native-footer-self-replica-launch'
BOMB = 'objectives/impact/dos/disk::native-footer-replication-disk-bomb'
CHACHA = 'micro-behaviors/crypto/symmetric/stream/chacha::chacha20-quarter-round-rotations-x86-64'
BLAKE = 'micro-behaviors/crypto/hash/digest::blake32-round-rotations-x64'
HEX64 = 'metadata/file/encoding::hex-64-literal'
CLR_NAME = 'micro-behaviors/fs/path/library::mscoree-dll-name'
PS_COMMAND = 'micro-behaviors/process/create/shell/command-flag::powershell-command-text'
POOLS = 'micro-behaviors/data/config/syntax::json-pools-array-field'
DONATE = 'micro-behaviors/data/config/syntax::json-donate-level-field'


def pe_text(code):
    """Nonfunctional PE fixture with one code section; entry point is RET."""
    data = bytearray(1024)
    data[:2] = b'MZ'
    struct.pack_into('<I', data, 0x3c, 0x80)
    data[0x80:0x84] = b'PE\0\0'
    struct.pack_into('<HHIIIHH', data, 0x84, 0x8664, 1, 0, 0, 0, 240, 0x22)
    off = 0x98
    struct.pack_into('<H', data, off, 0x20b)
    struct.pack_into('<I', data, off + 16, 0x1000)
    struct.pack_into('<Q', data, off + 24, 0x140000000)
    struct.pack_into('<II', data, off + 32, 0x1000, 0x200)
    struct.pack_into('<II', data, off + 56, 0x2000, 0x200)
    struct.pack_into('<H', data, off + 68, 3)
    struct.pack_into('<I', data, off + 108, 16)
    sec = off + 240
    data[sec:sec+8] = b'.text\0\0\0'
    struct.pack_into('<IIII', data, sec + 8, 512, 0x1000, 512, 512)
    struct.pack_into('<I', data, sec + 36, 0x60000020)
    data[512] = 0xc3
    data[528:528+len(code)] = code
    return data


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--sample', type=Path, required=True)
    ap.add_argument('--scratch', type=Path, required=True)
    args = ap.parse_args()
    original = args.sample.read_bytes()
    cases = []
    with tempfile.TemporaryDirectory(prefix='replica-controls-', dir=args.scratch) as tmp:
        def add(name, data, yes=(), no=()):
            path = Path(tmp) / name
            path.write_bytes(data)
            cases.append((path, set(yes), set(no)))

        add('renamed.exe', original, (REPLICA, BOMB, BLAKE), (CHACHA,))
        # Lower fan-out retains the replication code but removes the disk-bomb
        # threshold. A huge footer without the replication code is not a bomb.
        low = bytearray(original)
        struct.pack_into('<II', low, len(low)-8, 2, 3)
        add('small-fanout.exe', low, (REPLICA,), (BOMB, CHACHA))
        zero = bytearray(original)
        struct.pack_into('<I', zero, len(zero)-8, 0)
        add('zero-depth.exe', zero, (REPLICA,), (BOMB,))
        # Resolve the replica-path call by byte content, then change its target.
        broken = bytearray(original)
        end = broken.index(bytes.fromhex('48 8b cf e8'), broken.index(bytes.fromhex('43 8b 4c 37 f8 33 ed')))
        broken[end+4] ^= 1
        add('unlinked-launch.exe', broken, (), (REPLICA, BOMB))
        # Counter rewriting must be present, not just self-read/process APIs.
        broken = bytearray(original)
        pos = broken.index(bytes.fromhex('ba 04 00 00 00 48 8d 4c 24 24 4c 8b cb'))
        broken[pos+9] = 0x28
        add('no-depth-rewrite.exe', broken, (), (REPLICA, BOMB))
        unrelated = pe_text(b'\xc3') + bytearray(1024*1024)
        struct.pack_into('<II', unrelated, len(unrelated)-8, 200, 2000000)
        add('unrelated-large-footer.exe', unrelated, (), (REPLICA, BOMB))
        # Arbitrary chosen filenames and pool endpoints cannot gate detection.
        renamed = original.replace(b'C:\\Windows\\System\\', b'D:\\Windows\\System\\')
        renamed = renamed.replace(b'3.120.98.217:8080', b'8.123.45.678:8081')
        add('different-names.exe', renamed, (REPLICA, BOMB), (CHACHA,))
        add('chacha-rol.exe', pe_text(bytes.fromhex('c1 c0 10 01 d8 c1 c1 0c 31 d1 c1 c2 08 01 d0 c1 c3 07')), (CHACHA,), (BLAKE, REPLICA, BOMB))
        add('blake-ror.exe', pe_text(bytes.fromhex('c1 c0 10 01 d8 c1 c9 0c 31 d1 c1 ca 08 01 d0 c1 cb 07')), (BLAKE,), (CHACHA, REPLICA, BOMB))
        add('mixed-rotations.exe', pe_text(bytes.fromhex('c1 c0 10 01 d8 c1 c1 0c 31 d1 c1 ca 08 01 d0 c1 c3 07')), (), (CHACHA, BLAKE, REPLICA, BOMB))
        add('hex-data.py', ('value = "' + 'ab'*32 + '"\n').encode(), (HEX64,))
        add('short-hex.py', ('value = "' + 'ab'*31 + '"\n').encode(), (), (HEX64,))
        library = pe_text(b'mscoree.dll\0')
        library[0x188:0x190] = b'.rdata\0\0'
        add('clr-name-only.exe', library, (CLR_NAME,),
            ('micro-behaviors/dylib/library/family::mscoree-dll-name', REPLICA, BOMB))
        add('powershell-command.exe', pe_text(b'powershell.exe -Command "Get-Date"\0'),
            (PS_COMMAND,), ('micro-behaviors/process/interpreter/powershell/command::embedded-powershell-command',))
        add('configuration.exe', pe_text(b'{"pools": [], "donate-level": 0}\0'), (POOLS, DONATE),
            ('micro-behaviors/crypto/hash/mining::xmrig-config-pools',
             'micro-behaviors/crypto/hash/mining::xmrig-config-donate-level'))
        output = subprocess.check_output([
            os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
            '--format', 'json', '--disable', 'third-party',
            *[str(p) for p, _, _ in cases],
        ])
        # Multi-path analysis emits one compact report per input.
        decoder = json.JSONDecoder()
        remaining = output.decode().lstrip()
        files = {}
        while remaining:
            report, end = decoder.raw_decode(remaining)
            files.update({f['path']: {t['id'] for t in f.get('traits', [])}
                          for f in report['files']})
            remaining = remaining[end:].lstrip()
        for path, yes, no in cases:
            actual = files[str(path)]
            assert yes <= actual, (path.name, 'missing', sorted(yes-actual))
            assert not no & actual, (path.name, 'unexpected', sorted(no & actual))
            print('PASS', path.name)
    print(f'{len(cases)} static controls passed')


if __name__ == '__main__':
    main()
