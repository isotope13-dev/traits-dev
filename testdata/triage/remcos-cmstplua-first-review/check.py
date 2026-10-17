#!/usr/bin/env python3
"""Check neutral COM references and the RC4 transform's operation boundary.

Controls are inert PE images with RET entry points. No sample is executed.
The RC4 code uses a DWORD state table, unlike the older byte-table signatures.
"""
import json
import os
from pathlib import Path
import runpy
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
image = runpy.run_path(str(ROOT / 'testdata/triage/first-review/build_pe_fixtures.py'))['image']
RC4 = 'micro-behaviors/crypto/symmetric/stream/rc4::x86-dword-state-prga-buffer-xor'
CLSID = 'micro-behaviors/os/com/elevate::cmstplua-clsid'
SOURCE = CLSID + '-source'
OLD = 'objectives/privilege-escalation/elevation-control/uac-bypass/com::cmstplua-clsid'
BYPASS = 'objectives/privilege-escalation/elevation-control/uac-bypass/com::cmstplua-uac-bypass'
# Both swaps, sum modulo 256, keystream lookup, XOR, and the loop back-edge.
prga = bytes.fromhex(
    '46 81 e6 ff 00 00 80 79 08 4e 81 ce 00 ff ff ff 46 '
    '8b 44 b4 10 03 f8 81 e7 ff 00 00 80 79 08 4f 81 cf 00 ff ff ff 47 '
    '8a c8 8b 44 bc 10 89 44 b4 10 0f b6 c1 89 44 bc 10 '
    '8b 4c b4 10 03 c8 81 e1 ff 00 00 80 79 08 49 81 c9 00 ff ff ff 41 '
    '8a 44 8c 10 30 04 2b 43 3b da 72 a6'
)
guid = b'{3E5FC7F9-9A51-4367-9063-A120244FBEC7}'

def pe(code=b'', data=b''):
    result = bytearray(image(imports=False, overlay=False, rwx=False))
    result[0x220:0x220+len(code)] = code
    result[0x620:0x620+len(data)] = data
    return bytes(result)

cases = [
    ('prga.exe', pe(prga), {RC4}, {CLSID, BYPASS}),
    # An indexed state permutation without the output XOR is not this transform.
    ('permutation.exe', pe(prga.replace(b'\x30\x04\x2b', b'\x88\x04\x2b')), set(), {RC4}),
    ('data-reference.exe', pe(data=prga), set(), {RC4}),
    ('class-reference.exe', pe(data=guid+b'\0'), {CLSID}, {BYPASS, RC4, OLD}),
    ('both.exe', pe(prga, guid+b'\0'), {CLSID, RC4}, {BYPASS, OLD}),
    ('class-reference.cpp', b'const char *class_id = "'+guid+b'";\n', {SOURCE}, {BYPASS, OLD, OLD+'-source'}),
]
scratch = os.environ.get('TRIAGE_SCRATCH', str(ROOT.parents[1] / 'scratch'))
with tempfile.TemporaryDirectory(prefix='com-rc4-controls-', dir=scratch) as work:
    targets = []
    for name, content, _, _ in cases:
        target = Path(work) / name
        target.write_bytes(content)
        targets.append(str(target))
    run = subprocess.run([os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT), '--json', *targets],
                         cwd=ROOT, text=True, capture_output=True)
    assert run.returncode == 0, run.stderr or run.stdout
reports = {}
for line in run.stdout.splitlines():
    for report in json.loads(line).get('files', []):
        reports[Path(report['path']).name] = {t['id']: t for t in report.get('traits', [])}
for name, _, present, absent in cases:
    actual = reports[name]
    assert present <= actual.keys(), (name, 'missing', present-actual.keys())
    assert not absent & actual.keys(), (name, 'unexpected', absent & actual.keys())
    for trait in present:
        assert actual[trait]['crit'] == 3, (name, trait, actual[trait])
print(f'PASS: {len(cases)} COM-reference and RC4 operation controls')
