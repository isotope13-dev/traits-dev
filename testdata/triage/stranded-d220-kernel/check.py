"""Inert controls for driver capabilities and HTTP-table vocabulary placement.

Usage: python3 check.py SCRATCH_DIRECTORY
Generated PE files are analyzed statically and never executed.
"""
import json
import os
from pathlib import Path
import runpy
import re
import struct
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(sys.argv[1]).resolve()
OUT.mkdir(parents=True, exist_ok=True)
pe = runpy.run_path(str(ROOT / 'testdata/taxonomy/pe-review-boundaries/check.py'))['pe']
PMC = 'micro-behaviors/os/sysinfo/performance::x64-pmc-read-to-buffer'
DELETE = 'micro-behaviors/os/kernel/device::delete-device-object'
UNLINK = 'micro-behaviors/os/kernel/device::delete-device-symbolic-link'
VOCAB = 'metadata/lang/natural/vocabulary/content-word::'
OLD = 'objectives/command-and-control/remote-command/keywords::file-op-'
pmc = bytes.fromhex('8B 09 0F 33 48 C1 E2 20 48 0B C2 49 89 00')
words = b'MOVE\0COPY\0DELETE\0EXECUTE\0'
tokens = {VOCAB + 'uppercase-' + word + '-token'
          for word in ['move', 'copy', 'delete', 'execute']}
cases = {}


def case(name, image, yes=(), no=(), extension='.exe'):
    path = OUT / (name + extension)
    path.write_bytes(image)
    cases[str(path)] = (set(yes), set(no))


case('pmc-buffer', pe({}, text=pmc), [PMC])
library = pe({}, text=pmc)
struct.pack_into('<H', library, 0x96, 0x2022)
case('pmc-dll', library, [PMC], extension='.dll')
case('pmc-data', pe({}, data=pmc), no=[PMC])
case('pmc-opcode-only', pe({}, text=bytes.fromhex('0F 33')), no=[PMC])
case('msr-is-not-pmc', pe({}, text=pmc.replace(b'\x0f\x33', b'\x0f\x32')), no=[PMC])
case('pmc-without-output', pe({}, text=pmc[:-3]), no=[PMC])
other_arch = pe({}, text=pmc)
struct.pack_into('<H', other_arch, 0x84, 0xAA64)
case('pmc-other-architecture', other_arch, no=[PMC])
case('device-delete-imports',
     pe({'ntoskrnl.exe': ['IoDeleteDevice', 'IoDeleteSymbolicLink']}), [DELETE, UNLINK])
case('device-delete-mentions',
     pe({}, data=b'IoDeleteDevice\0IoDeleteSymbolicLink\0'), no=[DELETE, UNLINK])
case('http-method-table', pe({}, data=b'GET\0POST\0' + words), tokens)
case('action-words-in-code', pe({}, text=words), no=tokens)
case('lowercase-action-words', pe({}, data=words.lower()), no=tokens)
case('action-word-substrings', pe({}, data=b'REMOVE\0COPYRIGHT\0DELETED\0EXECUTED\0'), no=tokens)

r = subprocess.run([os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
                    '--format', 'json', *cases], capture_output=True, text=True)
assert r.returncode == 0, r.stderr
(OUT / 'reports.json').write_text(r.stdout)
decoder = json.JSONDecoder()
remaining = r.stdout.lstrip()
reports = []
while remaining:
    report, end = decoder.raw_decode(remaining)
    reports.extend(report['files'])
    remaining = remaining[end:].lstrip()
assert len(reports) == len(cases)
for f in reports:
    yes, no = cases[f['path']]
    found = {t['id']: t['crit'] for t in f.get('traits', [])}
    # The scan renderer strips unreferenced components. Inspect matcher traces
    # for vocabulary rather than promoting words to make them visible.
    assert yes - tokens <= found.keys(), (f['path'], 'missing', yes - tokens - found.keys())
    assert not no & found.keys(), (f['path'], 'unexpected', no & found.keys())
    assert not any(k.startswith(OLD) for k in found), (f['path'], 'legacy vocabulary')
    assert all(v < 4 for v in found.values()), (f['path'], 'unsupported attack claim')
    for t in yes & {PMC, DELETE, UNLINK}:
        assert found[t] == 3, (f['path'], 'capability must be notable', t)
    if (yes | no) & tokens:
        ids = tokens | {VOCAB + 'uppercase-action-token'}
        trace = subprocess.run([os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
                                'test-rules', f['path'], '--rules', ','.join(sorted(ids))],
                               capture_output=True, text=True)
        assert trace.returncode == 0, trace.stderr
        (OUT / (Path(f['path']).stem + '.trace.txt')).write_text(trace.stdout)
        matched = set(re.findall(r'^MATCHED (\S+)', trace.stdout, re.M))
        assert yes & tokens <= matched, (f['path'], 'missing token match')
        assert not no & matched, (f['path'], 'unexpected token match')
        assert (VOCAB + 'uppercase-action-token' in matched) == bool(yes & tokens)
print(f'PASS: {len(cases)} driver and vocabulary controls')
