"""Check operation-bound observations and nearby benign controls; execute no sample."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

fixtures = Path(__file__).resolve().parent
root = fixtures.parents[2]
cases = json.loads((fixtures / 'cases.json').read_text())
env = dict(os.environ, CLEAVE_VALIDATE='0')
# Keep path-sensitive fixture exclusions out of the observations being tested.
with tempfile.TemporaryDirectory(prefix='stranded-controls-') as tmp:
    for case in cases:
        shutil.copyfile(fixtures / case['file'], Path(tmp) / case['file'])
    result = subprocess.run(['cleave', '--traits-dir', str(root), '--format', 'json', tmp],
                            capture_output=True, text=True, env=env, check=True)
reports = {}
decoder = json.JSONDecoder()
remaining = result.stdout.strip()
while remaining:
    report, end = decoder.raw_decode(remaining)
    remaining = remaining[end:].lstrip()
    for item in report['files']:
        reports[Path(item['path']).name] = {t['id'] for t in item.get('traits', [])}
for case in cases:
    ids = reports[case['file']]
    for trait in case['present']:
        assert trait in ids, (case['file'], 'missing', trait)
    for trait in case['absent']:
        assert trait not in ids, (case['file'], 'unexpected', trait)
print(f"PASS: {len(cases)} operation and near-miss controls")
