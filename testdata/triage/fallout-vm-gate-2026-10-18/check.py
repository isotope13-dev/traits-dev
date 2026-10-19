#!/usr/bin/env python3
"""Scan inert PE controls; never execute their bytes."""
import argparse
import json
import struct
import subprocess
from pathlib import Path

RULE = 'objectives/anti-analysis/vm-detect/instruction::x86-virtualpc-vmware-early-return'
parser = argparse.ArgumentParser()
parser.add_argument('--scratch-dir', type=Path, required=True)
parser.add_argument('--cleave', default='cleave')
parser.add_argument('--sample', type=Path)
args = parser.parse_args()
root = Path(__file__).resolve().parents[3]
args.scratch_dir.mkdir(parents=True, exist_ok=True)


def fixture(edx=False, forward=False):
    data = bytearray(0x600)
    data[:2] = b'MZ'
    struct.pack_into('<I', data, 0x3c, 0x80)
    data[0x80:0x84] = b'PE\0\0'
    struct.pack_into('<HHIIIHH', data, 0x84, 0x14c, 2, 0, 0, 0, 0xe0, 0x102)
    opt = 0x98
    struct.pack_into('<H', data, opt, 0x10b)
    gate_rva, probe_rva = (0x1000, 0x2000) if forward else (0x2000, 0x1000)
    struct.pack_into('<IIIIII', data, opt + 4, 0x400, 0, 0, gate_rva, 0x1000, 0)
    struct.pack_into('<III', data, opt + 28, 0x400000, 0x1000, 0x200)
    struct.pack_into('<HH', data, opt + 40, 4, 0)
    struct.pack_into('<HH', data, opt + 48, 4, 0)
    struct.pack_into('<II', data, opt + 56, 0x3000, 0x200)
    struct.pack_into('<H', data, opt + 68, 3)
    struct.pack_into('<I', data, opt + 92, 16)
    for i, rva in enumerate([0x1000, 0x2000]):
        section = opt + 0xe0 + i * 40
        data[section:section + 8] = b'.code' + bytes([ord('a') + i]) + b'\0\0'
        struct.pack_into('<IIIIIIHHI', data, section + 8,
                         0x200, rva, 0x200, 0x200 + i * 0x200,
                         0, 0, 0, 0, 0x60000020)
    probe = 0x400 if forward else 0x200
    gate = 0x200 if forward else 0x400
    vpc = bytes.fromhex('55 8b ec') + b'\x90' * 16 + bytes.fromhex('b8 01 00 00 00 0f 3f 07 0b c9 c3')
    port = bytes.fromhex('ba 58 56 00 00 ed') if edx else bytes.fromhex('66 ba 58 56 ed')
    vmware = bytes.fromhex('55 8b ec') + b'\x90' * 16 + bytes.fromhex('b8 68 58 4d 56 b9 0a 00 00 00') + port + bytes.fromhex('c9 c3')
    data[probe:probe + len(vpc)] = vpc
    data[probe + 0x80:probe + 0x80 + len(vmware)] = vmware
    branch = bytearray.fromhex('e8 00 00 00 00 0f b6 c0 85 c0 75 0c e8 00 00 00 00 0f b6 c0 85 c0 74 07 33 c0 e9 00 00 00 00')
    struct.pack_into('<i', branch, 1, probe_rva - gate_rva - 5)
    struct.pack_into('<i', branch, 13, probe_rva + 0x80 - gate_rva - 17)
    struct.pack_into('<i', branch, 27, 0x80 - 31)
    data[gate:gate + len(branch)] = branch
    data[gate + 0x80:gate + 0x84] = bytes.fromhex('c9 c2 10 00')
    return data


base = fixture()
cases = {'split-sections-dx': (base, True),
         'split-sections-edx': (fixture(edx=True), True),
         'forward-calls': (fixture(forward=True), True)}


def mutate(name, offset, replacement):
    data = bytearray(base)
    data[offset:offset + len(replacement)] = replacement
    cases[name] = (data, False)


mutate('unrelated-first-callee', 0x401, struct.pack('<i', 0x1080 - 0x2000 - 5))
mutate('unrelated-second-callee', 0x40d, struct.pack('<i', 0x1000 - 0x2000 - 17))
mutate('changed-boolean-branch', 0x40a, b'\x74')
mutate('wrong-vmware-port', 0x280 + 19 + 10 + 2, b'\x59')
mutate('jump-does-not-return', 0x41b, struct.pack('<i', 0x81 - 31))
mutate('probe-only', 0x400, b'\x90' * 31)
mutate('probe-section-not-executable', 0x98 + 0xe0 + 36, struct.pack('<I', 0x40000040))
mutate('callee-outside-image', 0x401, struct.pack('<i', 0x100000))

expected = {}
for name, (data, want) in cases.items():
    path = args.scratch_dir / (name + '.exe')
    path.write_bytes(data)
    expected[str(path)] = want
if args.sample:
    expected[str(args.sample.resolve())] = True

run = subprocess.run([args.cleave, '--traits-dir', str(root), '--format', 'json', *expected],
                     capture_output=True, text=True)
(args.scratch_dir / 'stderr.txt').write_text(run.stderr)
(args.scratch_dir / 'reports.json').write_text(run.stdout)
if run.returncode:
    raise SystemExit(run.stderr or run.stdout)
reports, remaining = [], run.stdout.strip()
while remaining:
    report, end = json.JSONDecoder().raw_decode(remaining)
    reports.extend(report.get('files', [report]))
    remaining = remaining[end:].lstrip()
found = {f['path']: {t['id'] for t in f.get('traits', [])} for f in reports}
for path, want in expected.items():
    assert (RULE in found[path]) == want, (Path(path).name, want, found[path])
print(f'Passed {len(expected)} VM gate positive and near-miss controls')
