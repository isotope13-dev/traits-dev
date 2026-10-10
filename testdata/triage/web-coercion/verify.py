"""Run positive and benign near-miss controls against the current traits."""
import json
import subprocess
from pathlib import Path

root = Path(__file__).resolve().parents[3]
fixture_dir = Path(__file__).resolve().parent
result = subprocess.run(
    ['cleave', '--traits-dir', str(root), '--format', 'json', str(fixture_dir)],
    check=True, capture_output=True, text=True, timeout=300,
)
# Directory scans emit consecutive report objects even with --format json.
remaining = result.stdout
files = {}
decoder = json.JSONDecoder()
while remaining.strip():
    remaining = remaining.lstrip()
    report, end = decoder.raw_decode(remaining)
    remaining = remaining[end:]
    for item in report.get('files', []):
        files[Path(item['path']).resolve()] = {t['id'] for t in item['traits']}

cases = json.loads((fixture_dir / 'cases.json').read_text())
for case in cases['fixtures']:
    traits = files[(root / case['path']).resolve()]
    missing = set(case['matched']) - traits
    unexpected = set(case['not_matched']) & traits
    assert not missing and not unexpected, (case['path'], missing, unexpected)
    print('PASS', Path(case['path']).name)
