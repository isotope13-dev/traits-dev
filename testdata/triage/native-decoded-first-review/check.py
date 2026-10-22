"""Opcode controls for the decoded Rust DLL review; never executes fixtures."""
import itertools
import json
import os
from pathlib import Path
import struct
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)
CLEAVE = os.environ.get('CLEAVE', 'cleave')
XOR = 'micro-behaviors/data/encoding/xor::x64-eight-byte-prng-xor-buffer-loop'
B32 = 'micro-behaviors/data/decode/base32::x64-five-bit-table-byte-decoder'
CPU = 'micro-behaviors/os/virtualization/hypervisor::x64-cpuid-hypervisor-vendor-query'

def pe64(code):
    header = bytearray(0x200)
    header[:2] = b'MZ'
    struct.pack_into('<I', header, 0x3c, 0x80)
    header[0x80:0x84] = b'PE\0\0'
    struct.pack_into('<HHIIIHH', header, 0x84, 0x8664, 1, 0, 0, 0, 240, 0x22)
    o = 0x98
    struct.pack_into('<H', header, o, 0x20b)
    struct.pack_into('<II', header, o + 16, 0x1000, 0x1000)
    struct.pack_into('<QII', header, o + 24, 0x140000000, 0x1000, 0x200)
    struct.pack_into('<II', header, o + 56, 0x2000, 0x200)
    struct.pack_into('<HH', header, o + 68, 3, 0x160)
    struct.pack_into('<I', header, o + 108, 16)
    struct.pack_into('<8sIIIIIIHHI', header, o + 240, b'.text', len(code),
                     0x1000, 0x200, 0x200, 0, 0, 0, 0, 0x60000020)
    assert len(code) < 512
    return bytes(header) + code.ljust(512, b'\xcc')

cases = []
# Every spelling accepted by the original rule remains accepted.
for n, (load, add, select, compare) in enumerate(itertools.product(
        ['4C89D1', '498BCA'], ['4901D1', '4C03CA'],
        ['4C89DF', '498BFB'], ['4D39FA', '4D3BD7'])):
    code = bytes.fromhex(load + '4883E10775104C0FAFC8' + add + '90909090'
                         'C1E103' + select + '48D3EF42303C1649FFC2' + compare + '75D0C3')
    cases.append((f'old-allocation-{n}', code, {XOR}))
new = bytes.fromhex('4C89D94883E107751F4C0FAFC84C03CA4C89CF48C1EF184933F9'
                    '490FAFF84989FA49C1EA224931FAC1E1034C89D748D3EF42303C1E49FFC34D3BFB75C3C3')
cases += [('new-allocation', new, {XOR}),
          ('no-xor-store', new.replace(bytes.fromhex('42303C1E'), bytes.fromhex('42883C1E')), set())]
base32 = bytes.fromhex('89E9C1E1050FB66C14788D570509CD83FF0276C583C7FD89F989EAD3EA'
                       '909090904288143889F949FFC7BAFFFFFFFFD3E2C3')
cases += [('base32-bytes', base32, {B32}),
          ('four-bit-near-miss', base32.replace(bytes.fromhex('C1E105'), bytes.fromhex('C1E104')), set()),
          ('hypervisor-query', bytes.fromhex('B80000004031C94989DB0FA2C3'), {CPU}),
          ('ordinary-cpu-features', bytes.fromhex('B80100000031C94989DB0FA2C3'), set())]
results = []
paths = []
for name, code, expected in cases:
    path = OUT / (name + '.exe')
    path.write_bytes(pe64(code))
    paths.append(path)
run = subprocess.run([CLEAVE, '--json', *map(str, paths)], cwd=ROOT,
                     text=True, capture_output=True, check=True)
reports = [json.loads(line) for line in run.stdout.splitlines() if line.strip()]
assert len(reports) == len(cases), (len(reports), len(cases), run.stderr)
by_name = {}
for report in reports:
    files = report.get('files', report.get('raw', {}).get('files', []))
    by_name[Path(files[0]['path']).stem] = report
for name, code, expected in cases:
    report = by_name[name]
    files = report.get('files', report.get('raw', {}).get('files', []))
    found = {t['id'] for f in files for t in f.get('traits', f.get('findings', []))}
    actual = found & {XOR, B32, CPU}
    assert actual == expected, (name, expected, actual, run.stderr)
    results.append({'case': name, 'expected': sorted(expected), 'actual': sorted(actual)})
(OUT / 'results.json').write_text(json.dumps(results, indent=2) + '\n')
print(f'{len(results)} opcode controls passed')
