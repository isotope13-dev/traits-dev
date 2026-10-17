"""Static PE controls for register-padding detections; never execute fixtures.

Usage: python3 check.py SCRATCH_DIRECTORY [PADDED_SAMPLE]
"""
import json
import os
from pathlib import Path
import struct
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
PREFIX = 'objectives/anti-static/obfuscation/instruction/junk::'
MOVE = PREFIX + 'x86-long-self-move-padding'
EXCHANGE = PREFIX + 'x86-long-self-exchange-padding'


def pe(data, executable=True, overlay=b'', bits=32):
    buf = bytearray(0x600)
    buf[:2] = b'MZ'
    struct.pack_into('<I', buf, 0x3c, 0x80)
    buf[0x80:0x84] = b'PE\0\0'
    optional_size = 224 if bits == 32 else 240
    struct.pack_into('<HHIIIHH', buf, 0x84,
                     0x14c if bits == 32 else 0x8664,
                     1, 0, 0, 0, optional_size, 0x102)
    opt = 0x98
    struct.pack_into('<H', buf, opt, 0x10b if bits == 32 else 0x20b)
    struct.pack_into('<II', buf, opt + 16, 0x1000, 0x1000)
    if bits == 32:
        struct.pack_into('<I', buf, opt + 28, 0x400000)
    else:
        struct.pack_into('<Q', buf, opt + 24, 0x140000000)
    struct.pack_into('<II', buf, opt + 32, 0x1000, 0x200)
    struct.pack_into('<II', buf, opt + 56, 0x2000, 0x400)
    struct.pack_into('<H', buf, opt + 68, 2)
    struct.pack_into('<I', buf, opt + (92 if bits == 32 else 108), 16)
    sec = opt + optional_size
    buf[sec:sec + 8] = b'.custom\0'
    struct.pack_into('<IIII', buf, sec + 8, 0x200, 0x1000, 0x200, 0x400)
    struct.pack_into('<I', buf, sec + 36,
                     0x60000020 if executable else 0x40000040)
    assert len(data) <= 0x200
    buf[0x400:0x400 + len(data)] = data
    return bytes(buf) + overlay


def main():
    work = Path(sys.argv[1]) / 'register-padding-controls'
    work.mkdir(parents=True, exist_ok=True)
    move8 = b'\x88\xc0' * 32
    move16 = b'\x66\x89\xdb' * 32
    exchange = b'\x87\xdb' * 32
    regs = [0xc0, 0xc9, 0xd2, 0xdb, 0xe4, 0xed, 0xf6, 0xff]
    cases = {
        'move8-original.exe': (pe(move8), {MOVE}),
        'move16-store.exe': (pe(move16), {MOVE}),
        'move16-load.exe': (pe(b'\x66\x8b\xc9' * 32), {MOVE}),
        'move16-mixed-registers.exe':
            (pe(b''.join(bytes([0x66, 0x89, r]) for r in regs * 4)), {MOVE}),
        'move16-long-mode.exe': (pe(move16, bits=64), {MOVE}),
        'move16-31.exe': (pe(move16[:-3]), set()),
        'move16-other-register.exe': (pe(b'\x66\x89\xd8' * 32), set()),
        'move16-data.exe': (pe(move16, executable=False), set()),
        'move16-overlay.exe': (pe(b'\xc3', overlay=move16), set()),
        'move16-boundary.exe':
            (pe(bytes(0x200 - 93) + move16[:93], overlay=move16[93:]), set()),
        'exchange32.exe': (pe(exchange), {EXCHANGE}),
        'exchange8.exe': (pe(b'\x86\xd2' * 32), {EXCHANGE}),
        'exchange-mixed-registers.exe':
            (pe(b''.join(bytes([0x87, r]) for r in regs * 4)), {EXCHANGE}),
        'exchange-31.exe': (pe(exchange[:-2]), set()),
        'exchange-other-register.exe': (pe(b'\x87\xd8' * 32), set()),
        'exchange-long-mode.exe': (pe(exchange, bits=64), set()),
        'exchange-data.exe': (pe(exchange, executable=False), set()),
        'exchange-overlay.exe': (pe(b'\xc3', overlay=exchange), set()),
        'exchange-boundary.exe':
            (pe(bytes(0x200 - 62) + exchange[:62], overlay=exchange[62:]), set()),
        'ordinary-alignment.exe': (pe(b'\x90' * 128), set()),
        'both.exe': (pe(move16 + exchange), {MOVE, EXCHANGE}),
    }
    if len(sys.argv) > 2:
        sample = Path(sys.argv[2]).read_bytes()
        renamed = sample.replace(b'.htext\0\0', b'.custom\0')
        assert len(renamed) == len(sample) and renamed != sample
        cases['renamed-sample.exe'] = (renamed, {MOVE, EXCHANGE})
    paths = []
    for name, (data, _) in cases.items():
        path = work / name
        path.write_bytes(data)
        paths.append(str(path))
    result = subprocess.run(
        [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
         '--format', 'json', *paths], capture_output=True, text=True, check=True)
    (work / 'reports.json').write_text(result.stdout)
    (work / 'stderr.txt').write_text(result.stderr)
    remaining, observed = result.stdout.strip(), {}
    while remaining:
        report, end = json.JSONDecoder().raw_decode(remaining)
        for item in report['files']:
            observed[Path(item['path']).name] = {
                t['id'] for t in item['traits'] if t['id'] in {MOVE, EXCHANGE}}
        remaining = remaining[end:].strip()
    rows = []
    for name, (_, expected) in cases.items():
        assert observed[name] == expected, (name, observed[name], expected)
        rows.append(dict(case=name, traits=sorted(expected)))
    print(json.dumps(dict(cases=len(rows), failures=[], results=rows), indent=2))


if __name__ == '__main__':
    main()
