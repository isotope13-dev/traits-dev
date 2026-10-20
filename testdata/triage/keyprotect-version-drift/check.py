#!/usr/bin/env python3
"""Inert import-table controls for fiber and thread-context capability placement."""
import argparse
import json
import lzma
from pathlib import Path
import struct
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
FIBER = 'micro-behaviors/process/create/fiber::'
MANAGE = 'micro-behaviors/process/fiber::'
INFO = 'micro-behaviors/process/info/thread::'
LIFE = 'micro-behaviors/process/thread/lifecycle::'
OLD = 'objectives/evasion/process/injection/toolkit::fibers-execution'
PROFILE = FIBER + 'fiber-memory-thread-api-profile'


def pe(imports):
    """PE64 with a RET entry point; APIs are imported but never called."""
    b = bytearray(0x1000)
    b[:2] = b'MZ'
    struct.pack_into('<I', b, 0x3c, 0x80)
    b[0x80:0x84] = b'PE\0\0'
    struct.pack_into('<HHIIIHH', b, 0x84, 0x8664, 3, 0, 0, 0, 240, 0x22)
    opt = 0x98
    struct.pack_into('<H', b, opt, 0x20b)
    struct.pack_into('<Q', b, opt + 24, 0x140000000)
    for off, value in [(16, 0x1000), (20, 0x1000), (32, 0x1000),
                       (36, 0x200), (56, 0x4000), (60, 0x200),
                       (108, 16), (120, 0x3000), (124, 40)]:
        struct.pack_into('<I', b, opt + off, value)
    struct.pack_into('<H', b, opt + 68, 3)
    for i, (name, va, raw, size, flags) in enumerate([
        (b'.text', 0x1000, 0x200, 0x200, 0x60000020),
        (b'.rdata', 0x2000, 0x400, 0x400, 0x40000040),
        (b'.idata', 0x3000, 0x800, 0x800, 0xc0000040)]):
        struct.pack_into('<8sIIIIIIHHI', b, opt + 240 + i * 40,
                         name, size, va, size, raw, 0, 0, 0, 0, flags)
    b[0x200] = 0xc3
    struct.pack_into('<IIIII', b, 0x800, 0x3040, 0, 0, 0x31c0, 0x3100)
    b[0x9c0:0x9cd] = b'KERNEL32.dll\0'
    cursor = 0xa00
    for i, name in enumerate(imports):
        payload = b'\0\0' + name.encode() + b'\0'
        b[cursor:cursor + len(payload)] = payload
        for table in (0x840, 0x900):
            struct.pack_into('<Q', b, table + i * 8, cursor + 0x2800)
        cursor += len(payload)
        cursor += cursor % 2
    return b


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cleave', default='cleave')
    parser.add_argument('--scratch', type=Path, required=True)
    args = parser.parse_args()
    args.scratch.mkdir(parents=True, exist_ok=True)
    fibers = ['CreateFiber', 'SwitchToFiber']
    context = ['GetThreadContext', 'SetThreadContext']
    cases = [
        ('fibers-and-context.exe', fibers + context,
         [FIBER+'create-fiber', MANAGE+'switch-to-fiber',
          INFO+'thread-context-pair-get-set', LIFE+'thread-control-apis-2of4', PROFILE], []),
        ('fibers-only.exe', fibers,
         [FIBER+'create-fiber', MANAGE+'switch-to-fiber'], [PROFILE]),
        ('context-only.exe', context,
         [INFO+'thread-context-pair-get-set'], [PROFILE]),
        ('suspend-resume.exe', ['SuspendThread', 'ResumeThread'],
         [INFO+'suspend-thread-import', INFO+'resume-thread-import'],
         [PROFILE, INFO+'thread-context-pair-get-set',
          LIFE+'thread-control-pair-suspend-resume']),
        ('get-only.exe', ['GetThreadContext'],
         [INFO+'get-thread-context-import'], [PROFILE, LIFE+'thread-control-apis-2of4']),
        ('go-runtime.exe', None, [INFO+'thread-context-pair-get-set'], [PROFILE]),
    ]
    with tempfile.TemporaryDirectory(dir=args.scratch) as temp:
        for name, imports, required, absent in cases:
            path = Path(temp) / name
            if imports is None:
                fixture = ROOT / 'testdata/does-nothing/out/does-nothing-windows-amd64.exe.xz'
                path.write_bytes(lzma.decompress(fixture.read_bytes()))
            else:
                path.write_bytes(pe(imports))
            result = subprocess.run([
                args.cleave, '--no-update-check', '--traits-dir', str(ROOT),
                '--disable', 'radare2,upx,third-party', '--format', 'json', str(path)
            ], capture_output=True, text=True)
            assert result.returncode == 0, result.stderr
            report = json.loads(result.stdout)
            files = report.get('files', report.get('raw', {}).get('files', []))
            traits = {t['id']: t['crit'] for f in files for t in f.get('traits', [])}
            assert all(t in traits for t in required), (name, 'missing', set(required)-traits.keys())
            assert all(t not in traits for t in absent+[OLD]), (name, 'unexpected', traits)
            assert all(c not in (4, 5, 'suspicious', 'hostile') for c in traits.values()), (name, traits)
            levels = (2, 'baseline') if imports is None else (3, 'notable')
            assert all(traits[t] in levels for t in required), (name, traits)
            print(name, 'PASS')


if __name__ == '__main__':
    main()
