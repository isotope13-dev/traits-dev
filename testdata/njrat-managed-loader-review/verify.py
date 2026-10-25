#!/usr/bin/env python3
"""Check managed loader detections against an original PE and isolated mutations.

Usage: python3 testdata/njrat-managed-loader-review/verify.py SAMPLE SCRATCH
No specimen code is executed. Requires dnfile, dncil, cryptography and cleave.
"""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

import dnfile
from dncil.cil.body.reader import read_method_body_from_bytes

ROOT = Path(__file__).resolve().parents[2]
SAMPLE = Path(sys.argv[1]).resolve()
OUT = Path(sys.argv[2]).resolve()
OUT.mkdir(parents=True, exist_ok=True)
BASE = SAMPLE.read_bytes()
assert hashlib.sha256(BASE).hexdigest() == 'fbd4db896bb05fdd2e25a28e7c19885d4f559268f0fef0c944739c255c7455bb'
ETW = 'objectives/evasion/anti-av/blinding::managed-etw-single-byte-ret-patch'
INJECT = 'objectives/execution/payload/process-inject::managed-encrypted-pe-context-transfer'
PERSIST = 'objectives/persistence/login/registry/run-key::managed-concealed-name-self-copy-run-key'
TIMING = 'objectives/anti-analysis/timing/evasion::managed-random-sleep-shortening-check'
UNICODE = 'objectives/evasion/masquerade/naming::zero-width-spliced-executable-name'
EXPECTED = {ETW, INJECT, PERSIST, TIMING, UNICODE}


def scan(path):
    result = subprocess.run([os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT), '--format', 'json', str(path)], capture_output=True, text=True)
    assert result.returncode == 0, (path, result.stderr)
    assert not result.stderr.strip(), result.stderr
    report = json.loads(result.stdout)
    return {t['id']: t for t in report['files'][0]['traits']}, report


def cil_mutation(method, offset, before, after):
    pe = dnfile.dnPE(data=BASE)
    row = pe.net.mdtables.MethodDef.rows[method - 1]
    body = read_method_body_from_bytes(pe.get_data(row.Rva, 65536))
    instruction = next(i for i in body.instructions if i.offset == offset)
    pos = pe.get_offset_from_rva(row.Rva) + offset
    assert BASE[pos:pos + len(before)] == before, (method, offset, instruction)
    return BASE[:pos] + after + BASE[pos + len(before):]


cases = [('original', SAMPLE, EXPECTED)]
mutations = [
    ('etw-no-ret', cil_mutation(127, 0x44, b'\x20\xc3\0\0\0', b'\x20\x90\0\0\0'), {ETW}),
    ('etw-no-rwx', cil_mutation(127, 0x58, b'\x1f\x40', b'\x1f\x20'), {ETW}),
    ('context-other-slot', cil_mutation(56, 0x41f, b'\x1f\x2c', b'\x1f\x2b'), {INJECT}),
    ('allocation-other-protection', cil_mutation(56, 0x2ef, b'\x1f\x40', b'\x1f\x04'), {INJECT}),
    ('copy-not-hidden', cil_mutation(142, 0x73, b'\x18', b'\x17'), {PERSIST}),
    ('elapsed-greater-than', cil_mutation(138, 0x4c, b'\xfe\x04', b'\xfe\x02'), {TIMING}),
    ('ordinary-executable-name', BASE.replace(b'\x0b\x20', b'_\0'), {PERSIST, UNICODE}),
]
for name, data, removed in mutations:
    p = OUT / (name + '.exe')
    p.write_bytes(data)
    cases.append((name, p, EXPECTED - removed))
results = []
for name, path, expected in cases:
    traits, report = scan(path)
    observed = EXPECTED & traits.keys()
    assert observed == expected, (name, expected, observed)
    results.append({'case': name, 'matches': sorted(observed)})
    (OUT / (name + '.json')).write_text(json.dumps(report, indent=2))

# Existing independent fixtures: injection primitives, ordinary managed loading,
# detached pipes and a hostile client with a distinct command vocabulary.
for filename in ['dotnet-normal-loader-controls.exe', 'managed-native-interop-only.exe', 'dotnet-default-manifest.dll', 'csharp-independent-pipes.exe', 'crashpad-client-injection-controls.exe']:
    traits, _ = scan(ROOT / 'testdata/benign' / filename)
    assert not (EXPECTED & traits.keys()), (filename, EXPECTED & traits.keys())
    results.append({'case': filename, 'new_attack_matches': []})
traits, report = scan(ROOT / 'testdata/hostile/xworm-v3-obfuscated-client.exe')
assert len([t for t in traits.values() if t['crit'] == 5]) >= 9
assert 'well-known/malware/rat/xworm::xworm-classic-command-set' in traits
results.append({'case': 'xworm-v3-obfuscated-client.exe', 'hostile_traits': sum(t['crit'] == 5 for t in traits.values())})
(OUT / 'xworm-after.json').write_text(json.dumps(report, indent=2))
(OUT / 'results.json').write_text(json.dumps(results, indent=2))
print(json.dumps(results, indent=2))
