"""Static checks; fixtures are never executed."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import shutil

root = Path(__file__).resolve().parents[3]
cases = json.loads(Path(__file__).with_name('cases.json').read_text())
with tempfile.TemporaryDirectory(prefix='control-', dir=root) as temporary:
    for case in cases['fixtures']:
        scanned = Path(temporary) / Path(case['path']).name
        shutil.copyfile(root / case['path'], scanned)
        result = subprocess.run(
            [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(root),
             '--format', 'json', str(scanned)],
            text=True, capture_output=True,
        )
        assert result.stdout, result.stderr
        report = json.loads(result.stdout)
        traits = {t['id']: t for f in report['files'] for t in f['traits']}
        missing = set(case['matched']) - traits.keys()
        unexpected = set(case['not_matched']) & traits.keys()
        assert not missing and not unexpected, (case['case_id'], missing, unexpected)
        if case['case_id'] in ('ordinary-system-maintenance-task', 'ordinary-ssh-provisioning'):
            assert not any(t['crit'] >= 4 for t in traits.values()), case['case_id']
        print('PASS', case['case_id'])
