#!/usr/bin/env python3
"""Check direct NoAutoUpdate property-one observations and boundaries."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = os.environ.get('CLEAVE', str(ROOT.parent / 'cleave/target/release/cleave'))
RULE = 'micro-behaviors/os/registry/policy/write::powershell-no-auto-update-property-one'
RESET = 'micro-behaviors/os/registry/policy/write::powershell-auto-update-options-four'
source = 'New-ItemProperty -Path $path -Name NoAutoUpdate -Value 1 -PropertyType DWord\n'
cases = {
    'enabled': (source, True),
    'quoted': (source.replace('NoAutoUpdate', "'NoAutoUpdate'"), True),
    'mixed-case': (source.lower(), True),
    'crlf': (source.replace('\n', '\r\n'), True),
    'zero': (source.replace('-Value 1', '-Value 0'), False),
    'ten': (source.replace('-Value 1', '-Value 10'), False),
    'expression': (source.replace('-Value 1', '-Value 1+1'), False),
    'comment': ('# ' + source, False),
    'comment-fragment': ('New-ItemProperty -Path $path # -Name NoAutoUpdate -Value 1\n', False),
    'different-value': (source.replace('NoAutoUpdate', 'OtherValue'), False),
    'restore': (source.replace('NoAutoUpdate', 'AUOptions').replace('-Value 1', '-Value 4'), False),
    'other-auto-option': (source.replace('NoAutoUpdate', 'AUOptions').replace('-Value 1', '-Value 3'), False),
    'commented-restore': ('# ' + source.replace('NoAutoUpdate', 'AUOptions').replace('-Value 1', '-Value 4'), False),
}
with tempfile.TemporaryDirectory(prefix='no-auto-update-') as tmp:
    paths = []
    for name, (content, _) in cases.items():
        path = Path(tmp) / (name + '.ps1')
        path.write_text(content, newline='')
        paths.append(str(path))
    proc = subprocess.run([CLEAVE, '--traits-dir', str(ROOT), '--format=json', *paths],
                          check=True, capture_output=True, text=True,
                          env={**os.environ, 'CLEAVE_SKIP_CACHE': '1'})
    reports = [json.loads(line)['files'][0] for line in proc.stdout.splitlines() if line]
    assert len(reports) == len(cases)
    for f in reports:
        name = Path(f['path']).stem
        got = any(t['id'] == RULE for t in f.get('traits', []))
        assert got == cases[name][1], (name, got, cases[name][1])
        reset = any(t['id'] == RESET for t in f.get('traits', []))
        assert reset == (name == 'restore'), (name, reset)
print('NoAutoUpdate observation requires a value-one command, excluding comments and expressions')
