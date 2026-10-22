"""Check API/syntax boundaries while retaining SEO and regional sabotage coverage."""
import json
import pathlib
import subprocess
import sys

root = pathlib.Path(__file__).resolve().parents[3]
cases = json.loads(pathlib.Path(__file__).with_name('cases.json').read_text())['fixtures']
result = subprocess.run(
    [sys.argv[1] if len(sys.argv) > 1 else 'cleave', '--traits-dir', str(root),
     '--format', 'json'] + [str(root / row['path']) for row in cases],
    check=True, capture_output=True, text=True)
remaining = result.stdout
reports = {}
decoder = json.JSONDecoder()
while remaining.strip():
    report, end = decoder.raw_decode(remaining.lstrip())
    remaining = remaining.lstrip()[end:]
    for file in report['files']:
        reports[file['path']] = file
for row in cases:
    file = reports[str(root / row['path'])]
    ids = {trait['id'] for trait in file.get('traits', [])}
    assert set(row['matched']) <= ids, (row['case_id'], 'missing', set(row['matched']) - ids)
    assert not set(row['not_matched']) & ids, (row['case_id'], 'unexpected', set(row['not_matched']) & ids)
    print('PASS', row['case_id'])
