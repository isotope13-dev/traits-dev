#!/usr/bin/env python3
"""Check request/response boundaries and retained wallet header exports."""
import json
import os
from pathlib import Path
import subprocess
import struct
import tempfile

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
PREFIX = 'micro-behaviors/communications/http/header/custom::fetch-header-'
SEED = PREFIX + 'seed-variable'
MNEMONIC = PREFIX + 'mnemonic-variable'
WALLET = 'objectives/exfiltration/stealer/wallet::'
CASES = {
    'route-response.ts': (set(), {SEED, MNEMONIC}),
    'sibling-body.js': (set(), {SEED, MNEMONIC}),
    'quoted-source.js': (set(), {SEED, MNEMONIC}),
    'ordinary-seed.js': ({SEED}, {MNEMONIC, WALLET + 'js-wallet-seed-header-exfiltration'}),
    'both-values.ts': ({SEED, MNEMONIC}, set()),
    'validator-export.js': ({SEED, WALLET + 'js-seed-validation-header-exfiltration'}, set()),
    '../../hostile/xrpl-wallet-header-exfil.js': (
        {SEED, MNEMONIC, WALLET + 'js-wallet-seed-header-exfiltration', WALLET + 'js-wallet-mnemonic-header-exfiltration'}, set()),
}
# Minimal non-executing ELF fixtures exercise the retained .rodata condition.
def elf_with_rodata(payload):
    names = b'\0.shstrtab\0.rodata\0'
    data_offset = 64 + len(names)
    shoff = (data_offset + len(payload) + 7) & ~7
    ident = b'\x7fELF' + bytes([2, 1, 1]) + bytes(9)
    header = struct.pack('<16sHHIQQQIHHHHHH', ident, 1, 62, 1, 0, 0, shoff, 0, 64, 0, 0, 64, 3, 1)
    sections = bytes(64)
    sections += struct.pack('<IIQQQQIIQQ', 1, 3, 0, 0, 64, len(names), 0, 0, 1, 0)
    sections += struct.pack('<IIQQQQIIQQ', 11, 1, 2, 0, data_offset, len(payload), 0, 0, 1, 0)
    return (header + names + payload).ljust(shoff, b'\0') + sections

native = tempfile.TemporaryDirectory(prefix='.native-', dir=HERE)
length_trait = 'micro-behaviors/communications/http/header/content-length::maxint-http-content-length-header'
for name, value, matched in [('maxint.elf', 2147483647, True), ('smaller.elf', 2147483646, False)]:
    path = Path(native.name) / name
    path.write_bytes(elf_with_rodata(f'Content-Length: {value}'.encode() + b'\0'))
    CASES[str(path)] = ({length_trait}, set()) if matched else (set(), {length_trait})
paths = [HERE / name for name in CASES]
run = subprocess.run([os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT), '--format', 'json', *map(str, paths)], capture_output=True, text=True, check=True)
decoder = json.JSONDecoder()
reports = []
remaining = run.stdout.strip()
while remaining:
    report, end = decoder.raw_decode(remaining)
    reports.append(report)
    remaining = remaining[end:].lstrip()
files = {Path(f['path']).resolve(): f for report in reports for f in report['files']}
for name, (present, absent) in CASES.items():
    f = files[(HERE / name).resolve()]
    traits = {t['id']: t for t in f.get('traits', [])}
    assert present <= traits.keys(), (name, 'missing', present - traits.keys())
    assert not absent & traits.keys(), (name, 'unexpected', absent & traits.keys())
    for trait in (SEED, MNEMONIC):
        if trait in traits:
            assert traits[trait]['crit'] == 3, (name, 'header variable must be notable')
    print('PASS', name)

# This baseline atom can be omitted from presentation; test its matcher directly.
for name, expected in [('json-charset.js', True), ('json-no-charset.js', False)]:
    check = subprocess.run([os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT), 'test-rules', str(HERE / name), '--rules', 'micro-behaviors/communications/http/header/content-type::json-content-type-charset'], capture_output=True, text=True, check=True)
    assert ('\nMATCHED ' in check.stdout) == expected, (name, check.stdout, check.stderr)
    print('PASS', name)
native.cleanup()
