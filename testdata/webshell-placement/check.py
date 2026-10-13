"""Placement regression: webshell atoms live with what they detect.

- Whole-file whitespace ratio is metadata, not an objectives/stager trait.
- A bare `.php` path assignment is a micro-behavior path fact, not a
  Plesk webshell trait (the planter composite references the canonical one).
- Base64/reversed danger-keyword shards are components with honest descs;
  the suspicious composites aggregating them still fire.
"""
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
    by_id = {t['id']: t for t in f['traits']}
    assert set(case['matched']) <= set(by_id), (case['path'], set(case['matched']) - set(by_id))
    assert not set(case['not_matched']) & set(by_id), (case['path'], set(case['not_matched']) & set(by_id))
    for tid, want_crit in case.get('crit', {}).items():
        assert by_id[tid]['crit'] == want_crit, (case['path'], tid, by_id[tid]['crit'])
    for tid, want_desc in case.get('desc', {}).items():
        assert by_id[tid]['desc'] == want_desc, (case['path'], tid, by_id[tid]['desc'])
print(f"{len(cases)} webshell placement controls passed")
