"""Check neutral findings and absence of attack intent on benign controls."""
import json
import os
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parents[2]
cases = json.loads(Path(__file__).with_name('cases.json').read_text())['fixtures']
env = dict(os.environ, CLEAVE_TRAITS_DIR=str(root), CLEAVE_VALIDATE='0',
           SCAN_HOPPER='', SCAN_FETCH='none', SCAN_FORMAT='json')
result = subprocess.run(['atomscan', '--no-update', '--mode', 'slow', 'path',
                         *[str(root / c['path']) for c in cases]],
                        env=env, text=True, capture_output=True)
assert result.returncode == 0, result.stderr
files = {}
for line in result.stdout.splitlines():
    for f in json.loads(line)['raw']['files']:
        files[str(Path(f['path']).resolve())] = f
for case in cases:
    f = files[str(root / case['path'])]
    ids = {t['id'] for t in f['traits']}
    assert set(case['matched']) <= ids, (case['path'], set(case['matched']) - ids)
    assert not set(case['not_matched']) & ids, (case['path'], ids)
    assert all(t['crit'] < 4 for t in f['traits']), (case['path'], f['traits'])
print(f'{len(cases)} neutral attribution controls passed')
