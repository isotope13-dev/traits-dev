"""Check control scope, the phishing consumer, and the XOR instruction loop."""
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
cases = json.loads((HERE / 'cases.json').read_text())['fixtures']
result = subprocess.run(
    [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
     '--format', 'json', *[str(ROOT / c['path']) for c in cases]],
    cwd=ROOT, check=True, capture_output=True, text=True)
decoder = json.JSONDecoder()
remaining = result.stdout
observed = {}
while remaining.strip():
    report, end = decoder.raw_decode(remaining.lstrip())
    remaining = remaining.lstrip()[end:]
    for f in report['files']:
        observed[Path(f['path']).name] = {t['id'] for t in f.get('traits', [])}
for case in cases:
    ids = observed[Path(case['path']).name]
    assert set(case['matched']) <= ids, (case['path'], 'missing', ids)
    assert not set(case['not_matched']) & ids, (case['path'], 'unexpected', ids)
print(f'{len(cases)} controls passed')
