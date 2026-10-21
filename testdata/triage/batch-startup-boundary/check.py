#!/usr/bin/env python3
"""Check neutral Startup-copy observations and retain the shutdown consumer."""
import json
import os
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parents[3]
folder = Path(__file__).resolve().parent
result = subprocess.run([os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(root),
                         '--format', 'jsonl', str(folder)], capture_output=True, text=True)
assert result.returncode == 0, result.stderr
reports = [json.loads(line) for line in result.stdout.splitlines() if line.strip()]
cases = json.loads((folder / 'cases.json').read_text())
seen = set()
retired = {
    'objectives/persistence/login/startup/folder::batch-copy-self-to-startup',
    'objectives/persistence/login/startup/folder::batch-self-copy-startup-folder',
    'objectives/persistence/login/startup/folder::batch-copy-to-startup-folder',
    'objectives/persistence/login/self-install/script::batch-self-install-appdata',
}
for file in [file for report in reports for file in report['files']]:
    name = Path(file['path']).name
    if name not in cases:
        continue
    traits = {t['id']: t for t in file.get('traits', [])}
    assert not retired.intersection(traits), (name, retired.intersection(traits))
    for trait, expected in cases[name].items():
        assert (trait in traits) == expected, (name, trait, expected)
    if name != 'startup-shutdown.bat':
        assert all(t['crit'] <= 3 for t in traits.values()), (name, traits)
    else:
        consumer = 'objectives/impact/system/shutdown::batch-startup-persistence-shutdown'
        assert traits[consumer]['crit'] == 5, traits
    seen.add(name)
    print('PASS', name)
assert seen == set(cases), set(cases) - seen
