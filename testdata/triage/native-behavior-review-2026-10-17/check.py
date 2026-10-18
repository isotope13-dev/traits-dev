"""Inert query controls and nonexecuted sample mutations; no Windows execution.

Usage: python3 check.py SAMPLE_ROOT OUTPUT_DIRECTORY
Runs the current cleave traits through test-rules.
"""
import json
import re
import struct
import subprocess
import sys
from pathlib import Path

ROOT, OUT = map(Path, sys.argv[1:])
OUT.mkdir(parents=True, exist_ok=True)
VM = 'micro-behaviors/os/virtualization/detect::vmware-version-port-query'
READ = 'objectives/credential-access/keychain/extract::pstore-password-report-acquisition'
LOOP = 'metadata/binary/instruction::x86-indirect-eof-transfer-loop'
JOIN = 'objectives/impact/infect/binary/rewrite::packed-drive-executable-joiner'


def image(code, section):
    data = bytearray(0x400)
    data[:2] = b'MZ'
    struct.pack_into('<I', data, 0x3c, 0x80)
    data[0x80:0x84] = b'PE\0\0'
    struct.pack_into('<HHIIIHH', data, 0x84, 0x14c, 1, 1700000000, 0, 0, 224, 0x102)
    opt = 0x98
    struct.pack_into('<H', data, opt, 0x10b)
    for off, value in {4: 0x200, 16: 0x1000, 20: 0x1000, 28: 0x400000,
                       32: 0x1000, 36: 0x200, 56: 0x2000, 60: 0x200,
                       92: 16}.items():
        struct.pack_into('<I', data, opt + off, value)
    struct.pack_into('<H', data, opt + 68, 3)
    struct.pack_into('<8sIIIIIIHHI', data, opt + 224, section, 0x200, 0x1000,
                     0x200, 0x200, 0, 0, 0, 0, 0x60000020)
    data[0x200] = 0xc3  # All signatures are unreachable.
    data[0x220:0x220 + len(code)] = code
    return data


def sample(prefix):
    paths = [p for p in (ROOT / prefix).iterdir()
             if p.is_file() and p.suffix not in ('.BENIGN', '.MALICIOUS')]
    assert len(paths) == 1
    return paths[0]


cases = []
for name, port, command, operand, section, expected in [
    ('vm-edx-text', 0x5658, 10, 32, b'.text', True),
    ('vm-dx-upx', 0x5658, 10, 16, b'UPX0', True),
    ('vm-wrong-port', 0x5659, 10, 16, b'UPX0', False),
    ('vm-wrong-command', 0x5658, 9, 16, b'UPX0', False),
]:
    code = bytes.fromhex('b8 68 58 4d 56 b9') + struct.pack('<I', command)
    code += (b'\x66\xba' + struct.pack('<H', port) if operand == 16
             else b'\xba' + struct.pack('<I', port)) + b'\xed'
    target = OUT / (name + '.exe')
    target.write_bytes(image(code, section))
    cases.append((target, VM, expected))

worm = sample('ddf278c6d2a5')
cases += [(worm, VM, True), (worm, READ, True)]
data = bytearray(worm.read_bytes())
assert data[0x2b50f:0x2b512] == bytes.fromhex('ff 50 44')
data[0x2b511] = 0x48  # Preserve factory and report strings; remove ReadItem ABI.
target = OUT / 'pstore-without-readitem.exe'
target.write_bytes(data)
cases.append((target, READ, False))

infector = sample('d69954c40129')
cases += [(infector, LOOP, True), (infector, JOIN, True)]
data = bytearray(infector.read_bytes())
pattern = re.compile(bytes.fromhex('57 ff d5 83 c4 04 83 f8 ff 74 13 56 50 ff 15')
                     + b'.{4}' + bytes.fromhex('57 ff d5 83 c4 0c 83 f8 ff 75 ed'), re.S)
matches = list(pattern.finditer(data))
assert len(matches) == 2
for match in matches:
    data[match.start() + 8] = 0  # No EOF sentinel in the transfer loop.
target = OUT / 'joiner-without-eof-loop.exe'
target.write_bytes(data)
cases += [(target, LOOP, False), (target, JOIN, False)]

results = []
groups = {}
for target, rule, expected in cases:
    groups.setdefault(target, []).append((rule, expected))
for target, checks in groups.items():
    proc = subprocess.run(['cleave', '--traits-dir', '.', 'test-rules', str(target),
                           '--rules', ','.join(rule for rule, _ in checks)],
                          capture_output=True, text=True, check=True)
    (OUT / (target.name + '.txt')).write_text(proc.stdout + proc.stderr)
    for rule, expected in checks:
        match = re.search(r'^(MATCHED|NOT MATCHED) ' + re.escape(rule) + r'\s',
                          proc.stdout, re.M)
        assert match, (target, rule, proc.stdout, proc.stderr)
        actual = match[1] == 'MATCHED'
        assert actual == expected, (target, rule, expected, actual)
        results.append({'file': target.name, 'rule': rule, 'matched': actual})
        print('PASS', target.name, rule, flush=True)
(OUT / 'results.json').write_text(json.dumps(results, indent=2) + '\n')
