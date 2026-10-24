#!/usr/bin/env python3
"""Keep concealment observations without promoting ordinary inventory to theft.

Never execute fixture code. The repository's known-benign corpus forbids every
suspicious objective, so the deliberately concealed telemetry control lives here
and explicitly requires its four supported suspicious observations.
"""
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
cases = [
    (ROOT / 'testdata/benign/local-response-named-eval.js', 0, 0, {
        'metadata/lang/source/syntax/call/arguments::eval-response-named-data-argument': 3,
        'micro-behaviors/process/interpreter/eval/direct::js-eval-object-property': 3,
    }),
    (HERE / 'inventory-telemetry.js', 0, 4, {
        'objectives/anti-static/obfuscation/string/array::hex-decoded-table-method-dispatch': 4,
        'objectives/exfiltration/stealer/system-info/identity::hex-table-axios-host-identity-post': 4,
        'objectives/exfiltration/stealer/system-info/network::hex-table-axios-mac-inventory-post': 4,
        'objectives/exfiltration/stealer/system-info/platform::hex-table-axios-platform-post': 4,
    }),
    (ROOT / 'testdata/hostile/stranded-byte-review/renamed-export.js', 6, 5, {
        'objectives/exfiltration/stealer/env::js-concealed-env-post-with-response-eval': 5,
        'objectives/exfiltration/stealer/env::js-hex-table-env-post': 5,
        'objectives/exfiltration/stealer/system-info/identity::js-concealed-host-identity-post': 5,
        'objectives/execution/payload/script-eval::concealed-client-eval-response-data': 5,
    }),
]
result = subprocess.run(
    [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT), '--format', 'json',
     *(str(c[0]) for c in cases)], check=True, capture_output=True, text=True)
remaining = result.stdout
reports = {}
decoder = json.JSONDecoder()
while remaining.strip():
    report, end = decoder.raw_decode(remaining.lstrip())
    remaining = remaining.lstrip()[end:]
    reports.update({Path(f['path']).resolve(): f for f in report['files']})
for path, hostile, suspicious, required in cases:
    traits = reports[path.resolve()]['traits']
    observed = {t['id']: t['crit'] for t in traits}
    assert sum(t['crit'] == 5 for t in traits) == hostile, path
    assert sum(t['crit'] == 4 for t in traits) == suspicious, path
    for key, crit in required.items():
        assert observed.get(key) == crit, (path, key, observed.get(key))
    print('PASS', path.relative_to(ROOT))
