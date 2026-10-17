"""Verify response binding and messaging authority/abuse boundaries."""
import json
import subprocess
from pathlib import Path

root = Path(__file__).resolve().parents[3]
cases = json.loads(Path(__file__).with_name('cases.json').read_text())['fixtures']
result = subprocess.run(
    ['cleave', '--traits-dir', '.', '--format', 'json'] + [c['path'] for c in cases],
    cwd=root, capture_output=True, text=True, check=True,
)
decoder = json.JSONDecoder()
remaining = result.stdout.strip()
files = []
while remaining:
    report, end = decoder.raw_decode(remaining)
    files.extend(report['files'])
    remaining = remaining[end:].lstrip()
for case in cases:
    report = next(f for f in files if f['path'] == case['path'])
    traits = {t['id']: t['crit'] for t in report.get('traits', [])}
    for trait in case['matched']:
        assert trait in traits, (case['path'], 'missing', trait)
    for trait in case['not_matched']:
        assert trait not in traits, (case['path'], 'unexpected', trait)
    assert max(traits.values(), default=0) <= case.get('max_crit', 5), case['path']
print(f'{len(cases)} focused controls passed')
