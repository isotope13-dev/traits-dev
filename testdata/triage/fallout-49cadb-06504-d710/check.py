"""Offline matcher controls. Usage: check.py STORM_SAMPLE SCRATCH_DIRECTORY.

Specimens and generated PE files are only read by static analyzers.
"""
import json
import os
from pathlib import Path
import struct
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
JUNK = 'objectives/anti-static/obfuscation/instruction/junk::x86-long-self-move-padding'
PSTORE = 'micro-behaviors/os/security/protected-storage::pstore-category-internet-explorer'


def pe(data, executable=True, overlay=b''):
    buf = bytearray(0x600)
    buf[:2] = b'MZ'
    struct.pack_into('<I', buf, 0x3c, 0x80)
    buf[0x80:0x84] = b'PE\0\0'
    struct.pack_into('<HHIIIHH', buf, 0x84, 0x14c, 1, 0, 0, 0, 224, 0x102)
    opt = 0x98
    struct.pack_into('<H', buf, opt, 0x10b)
    struct.pack_into('<II', buf, opt + 16, 0x1000, 0x1000)
    struct.pack_into('<I', buf, opt + 28, 0x400000)
    struct.pack_into('<II', buf, opt + 32, 0x1000, 0x200)
    struct.pack_into('<II', buf, opt + 56, 0x2000, 0x400)
    struct.pack_into('<H', buf, opt + 68, 2)
    struct.pack_into('<I', buf, opt + 92, 16)
    sec = opt + 224
    buf[sec:sec + 8] = b'.custom\0'
    struct.pack_into('<IIII', buf, sec + 8, 0x200, 0x1000, 0x200, 0x400)
    struct.pack_into('<I', buf, sec + 36, 0x60000020 if executable else 0x40000040)
    assert len(data) <= 0x200
    buf[0x400:0x400 + len(data)] = data
    return bytes(buf) + overlay


def main():
    storm = Path(sys.argv[1]).read_bytes()
    work = Path(sys.argv[2]) / 'matcher-controls'
    work.mkdir(parents=True, exist_ok=True)
    renamed = storm.replace(b'.htext\0\0', b'.custom\0')
    assert renamed != storm and len(renamed) == len(storm)
    run = b'\x88\xc0' * 32
    mixed = b''.join(bytes([0x88, reg]) for reg in [0xc0, 0xc9, 0xd2, 0xdb] * 8)
    cases = {
        'self-move-32.exe': (pe(run), True, False),
        'mixed-self-moves.exe': (pe(mixed), True, False),
        'self-move-31.exe': (pe(run[:-2]), False, False),
        'moves-between-registers.exe': (pe(b'\x88\xc1' * 32), False, False),
        'non-executable-data.exe': (pe(run, executable=False), False, False),
        'overlay-only.exe': (pe(b'\xc3', overlay=run), False, False),
        'section-boundary.exe': (pe(bytes(0x200 - 62) + run[:62], overlay=run[62:]), False, False),
        'renamed-storm.exe': (renamed, True, False),
        'ie-path.exe': (pe(b'C:\\Program Files\\Internet Explorer\\iexplore.exe\0'), False, False),
        'ie-label.exe': (pe(b'Internet Explorer\0'), False, False),
        'pstore-factory.exe': (pe(b'PStoreCreateInstance\0'), False, False),
        'pstore-ie-label.exe': (pe(b'PStoreCreateInstance\0Internet Explorer\0'), False, True),
        'pstore-ie-path.exe': (pe(b'PStoreCreateInstance\0C:\\Program Files\\Internet Explorer\\iexplore.exe\0'), False, False),
        'pstore-ie-wide.exe': (pe('PStoreCreateInstance\0Internet Explorer\0'.encode('utf-16le')), False, True),
    }
    paths = []
    for name, (data, _, _) in cases.items():
        path = work / name
        path.write_bytes(data)
        paths.append(str(path))
    result = subprocess.run([os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
                             '--format', 'json', *paths], capture_output=True, text=True, check=True)
    (work / 'reports.json').write_text(result.stdout)
    (work / 'stderr.txt').write_text(result.stderr)
    remaining = result.stdout.strip()
    observed = {}
    while remaining:
        report, stop = json.JSONDecoder().raw_decode(remaining)
        for f in report['files']:
            observed[Path(f['path']).name] = {t['id'] for t in f['traits']}
        remaining = remaining[stop:].strip()
    summary = []
    for name, (_, junk, pstore) in cases.items():
        traits = observed[name]
        assert (JUNK in traits) == junk, (name, 'self-move', junk)
        assert (PSTORE in traits) == pstore, (name, 'pstore', pstore)
        summary.append(dict(case=name, self_move=junk, pstore_ie=pstore))
    print(json.dumps(dict(cases=len(cases), failures=[], results=summary), indent=2))


if __name__ == '__main__':
    main()
