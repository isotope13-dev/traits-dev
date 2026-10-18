#!/usr/bin/env python3
"""Static regression controls; do not execute the specimen or its payloads."""
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

here = Path(__file__).resolve().parent
root = here.parents[1]
iam = 'micro-behaviors/communications/http/services/aws-iam::iam-user-create-call'
logon = 'micro-behaviors/os/privilege/token::logon-user'
retired = 'micro-behaviors/process/create/shell/staged::createprocess-shellcode-api'
cases = {
    'iam-create.php': ({iam}, set()),
    'cms-create.php': (set(), {iam}),
    'process-selector.cs': (set(), {retired}),
    'logon-name.c': ({logon}, set()),
    'logon-nearmiss.c': (set(), {logon}),
}
with tempfile.TemporaryDirectory(prefix='.registry-review-', dir=root) as staging:
    paths = []
    for name in cases:
        target = Path(staging) / name
        shutil.copyfile(here / name, target)
        paths.append(str(target))
    result = subprocess.run(
        ['cleave', '--traits-dir', str(root), '--format', 'json', *paths],
        capture_output=True, text=True, check=True,
    )
decoder = json.JSONDecoder()
remaining = result.stdout.strip()
files = []
while remaining:
    report, consumed = decoder.raw_decode(remaining)
    files.extend(report['files'])
    remaining = remaining[consumed:].lstrip()
for report in files:
    name = Path(report['path']).name
    if name not in cases:
        continue
    present, absent = cases[name]
    actual = {t['id'] for t in report.get('traits', [])}
    assert present <= actual, (name, 'missing', present - actual)
    assert not absent & actual, (name, 'unexpected', absent & actual)
    print(name, 'PASS')
assert len(files) == len(cases), 'Missing control reports'
