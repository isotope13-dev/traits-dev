#!/usr/bin/env python3
"""Exercise bound native attribute writes without executing any specimen."""
import argparse
import json
import struct
import subprocess
import tempfile
from pathlib import Path

RULE = 'micro-behaviors/fs/attributes/flags::x86-set-hidden-system-attributes'
ROOT = Path(__file__).resolve().parents[3]


def fixture(mask=6, register=1, call=0x402050, executable=True):
    """Minimal PE with one explicit SetFileAttributesA import and call."""
    b = bytearray(0x600)
    b[:2] = b'MZ'
    struct.pack_into('<I', b, 0x3c, 0x80)
    b[0x80:0x84] = b'PE\0\0'
    struct.pack_into('<HHIIIHH', b, 0x84, 0x14c, 2, 0, 0, 0, 224, 0x102)
    opt = 0x98
    struct.pack_into('<H', b, opt, 0x10b)
    for offset, value in {4: 0x200, 8: 0x200, 16: 0x1000, 20: 0x1000,
                          24: 0x2000, 28: 0x400000, 32: 0x1000,
                          36: 0x200, 56: 0x3000, 60: 0x200, 92: 16,
                          104: 0x2000, 108: 40}.items():
        struct.pack_into('<I', b, opt + offset, value)
    struct.pack_into('<H', b, opt + 68, 3)
    for offset, name, rva, raw, flags in (
        (0x178, b'.text', 0x1000, 0x200,
         0x60000020 if executable else 0x40000040),
        (0x1a0, b'.idata', 0x2000, 0x400, 0xc0000040),
    ):
        struct.pack_into('<8sIIIIIIHHI', b, offset, name, 0x200, rva,
                         0x200, raw, 0, 0, 0, 0, flags)
    struct.pack_into('<IIIII', b, 0x400, 0x2040, 0, 0, 0x2080, 0x2050)
    for offset in (0x440, 0x450):
        struct.pack_into('<II', b, offset, 0x20a0, 0)
    b[0x480:0x48d] = b'KERNEL32.dll\0'
    b[0x4a0:0x4b5] = b'\0\0SetFileAttributesA\0'
    code = (bytes([0x6a, mask, 0x8d, 0x85 + register * 8]) +
            struct.pack('<i', -0x328) + bytes([0x50 + register, 0xff, 0x15]) +
            struct.pack('<I', call) + b'\xc3')
    b[0x200:0x200 + len(code)] = code
    return bytes(b)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('samples', type=Path, nargs=3)
    parser.add_argument('--work-dir', type=Path, required=True)
    parser.add_argument('--cleave', default='cleave')
    args = parser.parse_args()
    cases = {f'sample-{i}.exe': (p.read_bytes(), True)
             for i, p in enumerate(args.samples)}
    for mask in (6, 7):
        for reg in range(3):
            cases[f'neutral-mask-{mask}-reg-{reg}.exe'] = (fixture(mask, reg), True)
    for mask in (0, 1, 2, 4, 0x80):
        cases[f'other-mask-{mask}.exe'] = (fixture(mask), False)
    cases['wrong-import-slot.exe'] = (fixture(call=0x402054), False)
    cases['nonexecutable-data.exe'] = (fixture(executable=False), False)
    cases['unrelated-api-name.exe'] = (
        fixture().replace(b'SetFileAttributesA', b'GetFileAttributesA'), False)
    args.work_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=args.work_dir, prefix='attribute-controls-') as td:
        for name, (data, _) in cases.items():
            (Path(td) / name).write_bytes(data)
        result = subprocess.run([
            args.cleave, '--traits-dir', str(ROOT), '--all-files',
            '--format', 'json', td,
        ], capture_output=True, text=True, check=True)
        assert not result.stderr.strip(), result.stderr
        remaining, seen = result.stdout, set()
        decoder = json.JSONDecoder()
        while remaining.strip():
            report, length = decoder.raw_decode(remaining.lstrip())
            remaining = remaining.lstrip()[length:]
            for file in report['files']:
                name = Path(file['path']).name
                if name not in cases or 'pid' in file:
                    continue
                seen.add(name)
                traits = file.get('traits', [])
                matched = any(t['id'] == RULE for t in traits)
                assert matched == cases[name][1], (name, matched)
                if name.startswith('neutral-'):
                    assert not [t for t in traits if t['crit'] >= 4], (name, traits)
                print(f'{name}: PASS')
        assert seen == cases.keys(), seen
    print(f'{len(cases)} controls passed')


if __name__ == '__main__':
    main()
