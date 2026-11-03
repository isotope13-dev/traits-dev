#!/usr/bin/env python3
"""A public ACL option must appear as a build-step argument."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = os.environ.get('CLEAVE', str(ROOT.parent / 'cleave/target/release/cleave'))
RULE = 'micro-behaviors/os/virtualization/configure::cloudbuild-public-read-acl-argument'
CASES = {
    'grant': ("steps:\n  - args: ['storage', '--add-acl-grant=AllUsers:R']\n", True),
    'other-acl': ("steps:\n  - args: ['--add-acl-grant=projectOwners:R']\n", False),
    'remove': ("steps:\n  - args: ['--remove-acl-grant=AllUsers:R']\n", False),
    'elsewhere': ("description: '--add-acl-grant=AllUsers:R'\nsteps: []\n", False),
    'comment': ("# --add-acl-grant=AllUsers:R\nsteps: []\n", False),
}
with tempfile.TemporaryDirectory(prefix='cloudbuild-acl-') as tmp:
    paths = []
    for name, (source, _) in CASES.items():
        path = Path(tmp) / (name + '.yaml')
        path.write_text(source)
        paths.append(str(path))
    proc = subprocess.run([CLEAVE, '--traits-dir', str(ROOT), '--format=json', *paths],
                          check=True, capture_output=True, text=True,
                          env={**os.environ, 'CLEAVE_SKIP_CACHE': '1'})
    reports = [json.loads(line)['files'][0] for line in proc.stdout.splitlines() if line]
    assert len(reports) == len(CASES)
    for report in reports:
        name = Path(report['path']).stem
        found = any(trait['id'] == RULE for trait in report.get('traits', []))
        assert found == CASES[name][1], (name, found, CASES[name][1])
print('public-read ACL observation requires a build-step grant option')
