#!/usr/bin/env python3
"""Only the explicit false setting should match the OS Login observation."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = os.environ.get('CLEAVE', str(ROOT.parent / 'cleave/target/release/cleave'))
RULE = 'micro-behaviors/os/virtualization/configure::python-oslogin-false-metadata-call'
CASES = {
    'false': ("md.SetMetadata('enable-oslogin', False, PROJECT_LEVEL)", True),
    'double-quote': ('md.SetMetadata("enable-oslogin", False)', True),
    'true': ("md.SetMetadata('enable-oslogin', True)", False),
    'variable': ("md.SetMetadata('enable-oslogin', enabled)", False),
    'other-key': ("md.SetMetadata('other-key', False)", False),
    'other-method': ("md.GetMetadata('enable-oslogin', False)", False),
    'comment': ("# md.SetMetadata('enable-oslogin', False)", False),
    'string': ('''print("md.SetMetadata('enable-oslogin', False)")''', False),
}
with tempfile.TemporaryDirectory(prefix='oslogin-metadata-') as tmp:
    paths = []
    for name, (source, _) in CASES.items():
        path = Path(tmp) / (name + '.py')
        path.write_text(source + '\n')
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
print('OS Login metadata observation requires an explicit false argument')
