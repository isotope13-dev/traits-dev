"""Run static detector controls; fixture scripts are never executed."""
import json
import os
import pathlib
import subprocess
import tempfile
import shutil

ROOT = pathlib.Path(__file__).resolve().parents[3]
CASES = json.loads(pathlib.Path(__file__).with_name('cases.json').read_text())
engine = os.environ.get('CLEAVE', 'cleave')
# Stage outside testdata so test-directory suppressors cannot mask a regression.
with tempfile.TemporaryDirectory(prefix='loader-controls-', dir=ROOT) as temporary:
    for case in CASES['fixtures']:
        shutil.copyfile(ROOT / case['path'], pathlib.Path(temporary) / pathlib.Path(case['path']).name)
    result = subprocess.run(
        [engine, '--traits-dir', str(ROOT), '--format', 'json', temporary],
        cwd=ROOT, check=True, text=True, capture_output=True,
    )
if result.stderr.strip():
    raise AssertionError(result.stderr)
reports = {}
remaining = result.stdout.strip()
decoder = json.JSONDecoder()
while remaining:
    report, end = decoder.raw_decode(remaining)
    for file in report.get('files', []):
        reports[pathlib.Path(file['path']).name] = {
            trait['id'] for trait in file.get('traits', [])
        }
    remaining = remaining[end:].lstrip()
for case in CASES['fixtures']:
    ids = reports[pathlib.Path(case['path']).name]
    assert set(case['matched']) <= ids, (case['path'], set(case['matched']) - ids)
    assert not set(case['not_matched']) & ids, (case['path'], set(case['not_matched']) & ids)
print(f"Passed {len(CASES['fixtures'])} static detector controls")
