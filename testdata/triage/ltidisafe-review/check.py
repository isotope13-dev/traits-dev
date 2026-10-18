"""Check the indirect HTTP sender and lifecycle declaration boundaries."""
import json
import subprocess
import sys
from pathlib import Path

base = Path(__file__).resolve().parent
root = base.parents[2]
report = Path(sys.argv[1]).read_text() if len(sys.argv) > 1 else subprocess.check_output(
    ['cleave', '--no-update-check', '--traits-dir', str(root), '--format', 'json', str(base)], text=True)
decoder = json.JSONDecoder()
files = []
position = 0
while position < len(report):
    if report[position].isspace():
        position += 1
        continue
    data, position = decoder.raw_decode(report, position)
    files.extend(data['files'])
for case in json.loads((base / 'cases.json').read_text())['fixtures']:
    hits = [file for file in files if file['path'].endswith('/' + case['path'])]
    assert len(hits) == 1, case['path']
    ids = {trait['id'] for trait in hits[0]['traits']}
    assert set(case['matched']) <= ids, (case['path'], 'missing', set(case['matched']) - ids)
    assert not set(case['not_matched']) & ids, (case['path'], 'unexpected', set(case['not_matched']) & ids)
    print('PASS', case['path'])
