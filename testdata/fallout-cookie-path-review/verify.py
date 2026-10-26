#!/usr/bin/env python3
"""Resolve/mutate original CIL and scan controls; never execute specimens.

Usage: python3 verify.py SAMPLE SCRATCH
Requires dnfile, dncil, and the source-matched cleave CLI.
"""
import json
import os
from pathlib import Path
import struct
import subprocess
import sys

import dnfile
from dncil.cil.body import CilMethodBody
from dncil.cil.body.reader import CilMethodBodyReaderBytes
from dncil.clr.token import StringToken

ROOT = Path(__file__).resolve().parents[2]
SAMPLE, OUT = map(Path, sys.argv[1:])
OUT.mkdir(parents=True, exist_ok=True)
PATH = 'micro-behaviors/fs/path/cookie::managed-chromium-cookie-path-components'
COOKIE = 'objectives/exfiltration/stealer/browser::managed-keylogger-cookie-store-upload-profile'
LINE = 'micro-behaviors/data/format/string::managed-loopback-line-call-layout'
HOSTS = 'objectives/evasion/hosts-file/block-security::managed-keylogger-security-hosts-sinkhole-profile'
base = SAMPLE.read_bytes()
pe = dnfile.dnPE(data=base)
methods = []
strings = {}
for row in pe.net.mdtables.MethodDef:
    if not row.Rva:
        continue
    start = pe.get_offset_from_rva(row.Rva)
    body = CilMethodBody(CilMethodBodyReaderBytes(pe.get_data(row.Rva, 40000)))
    methods.append((row, start, body))
    for ins in body.instructions:
        if isinstance(ins.operand, StringToken):
            strings[pe.net.user_strings.get(ins.operand.rid).value] = ins.operand.value


def replace(blob, old, new):
    assert old in blob and len(old) == len(new)
    return blob.replace(old, new)


def patch(blob, offset, expected, replacement):
    assert len(expected) == len(replacement)
    assert blob[offset:offset + len(expected)] == expected
    return blob[:offset] + replacement + blob[offset + len(expected):]


# Find the Cookies operand in the actual six-argument profile-path array.
# No hardcoded metadata token or RVA is assumed.
paths = []
for row, start, body in methods:
    for i, ins in enumerate(body.instructions):
        if isinstance(ins.operand, StringToken) and ins.operand.value == strings['Cookies']:
            if i >= 1 and body.instructions[i - 1].opcode.name == 'ldc.i4.5':
                paths.append((start, body.instructions, i))
assert len(paths) == 1
start, instructions, index = paths[0]
cookie_operand = start + instructions[index].offset + 1
array_reload = start + instructions[index + 2].offset + 1
combine_call = start + instructions[index + 3].offset

cases = {
    'original.exe': (base, (True, True, True, True)),
    # The mutable label may disappear without removing the cookie source.
    'renamed-record.exe': (replace(base, 'RECORD:'.encode('utf-16le'),
                                 'EVENTS:'.encode('utf-16le')), (True, True, True, True)),
    'wrong-cookie-operand.exe': (patch(base, cookie_operand,
                                     struct.pack('<I', strings['Cookies']),
                                     struct.pack('<I', strings['History'])),
                                 (False, False, True, True)),
    'different-path-array.exe': (patch(base, array_reload, base[array_reload:array_reload+1],
                                     bytes([base[array_reload] + 1])),
                                 (False, False, True, True)),
    'no-path-combine-call.exe': (patch(base, combine_call, b'\x28', b'\x00'),
                                (False, False, True, True)),
    'no-base64-api.exe': (replace(base, b'ToBase64String\0', b'ToBase64StrinX\0'),
                          (True, False, True, True)),
    'no-upload-api.exe': (replace(base, b'UploadString\0', b'UploadStrinX\0'),
                          (True, False, True, True)),
    'no-recorder.exe': (replace(base, b'WH_KEYBOARD_LL\0', b'WH_KEYBOARD_XX\0'),
                        (True, False, True, False)),
}
# Both independently present sinkhole loops must cease matching. Keeping the
# original prefix text in #US tests token resolution, rather than text erasure.
rebound, removed_calls = base, base
line_sites = 0
for row, start, body in methods:
    for i, ins in enumerate(body.instructions):
        if isinstance(ins.operand, StringToken) and ins.operand.value == strings['127.0.0.1 ']:
            rebound = patch(rebound, start + ins.offset + 1,
                            struct.pack('<I', strings['127.0.0.1 ']),
                            struct.pack('<I', strings[' ']))
            sink = body.instructions[i + 3]
            assert sink.opcode.name == 'callvirt'
            removed_calls = patch(removed_calls, start + sink.offset, b'\x6f', b'\x00')
            line_sites += 1
assert line_sites == 2
cases['rebound-loopback-prefix.exe'] = rebound, (True, True, False, False)
cases['no-line-write-calls.exe'] = removed_calls, (True, True, False, False)
cases['no-line-writer-api.exe'] = replace(base, b'WriteLine\0', b'WriteLinX\0'), (True, True, False, False)

for name, (content, expected) in cases.items():
    (OUT / name).write_bytes(content)
proc = subprocess.run([os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
                       '--format', 'json', str(OUT)], capture_output=True, text=True, check=True)
assert not proc.stderr.strip(), proc.stderr
(OUT / 'scans.json').write_text(proc.stdout)
rest, decoder, seen, results = proc.stdout, json.JSONDecoder(), set(), []
while rest.strip():
    report, length = decoder.raw_decode(rest.lstrip())
    rest = rest.lstrip()[length:]
    for f in report['files']:
        name = Path(f['path']).name
        if name not in cases or 'pid' in f:
            continue
        actual = {t['id'] for t in f.get('traits', [])}
        observed = tuple(rule in actual for rule in [PATH, COOKIE, LINE, HOSTS])
        assert observed == cases[name][1], (name, observed, cases[name][1])
        seen.add(name)
        results.append({'case': name, 'path_cookie_line_hosts': observed})
assert seen == cases.keys(), cases.keys() - seen
(OUT / 'results.json').write_text(json.dumps(results, indent=2) + '\n')
print(f'PASS: {len(results)} original-CIL controls; two loopback write sites verified')
