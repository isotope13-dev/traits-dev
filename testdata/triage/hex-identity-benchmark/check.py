"""Check trait regressions with cleave; optionally reuse a saved JSON report."""
import json
import subprocess
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[3]
cases = json.loads(Path(__file__).with_name('cases.json').read_text())['fixtures']
report = Path(sys.argv[1]).read_text() if len(sys.argv) > 1 else subprocess.check_output(
    ['cleave', '--traits-dir', str(root), '--format', 'json', str(Path(__file__).parent)], text=True)
files = {}
decoder = json.JSONDecoder()
i = 0
while i < len(report):
    while i < len(report) and report[i].isspace():
        i += 1
    if i == len(report):
        break
    data, i = decoder.raw_decode(report, i)
    for file in data['files']:
        files[Path(file['path']).name] = file['traits']
for case in cases:
    traits = files[Path(case['path']).name]
    ids = {trait['id'] for trait in traits}
    assert set(case['matched']) <= ids, case['path']
    assert not set(case['not_matched']) & ids, case['path']
    if not case['matched']:
        assert not [t for t in traits if t['crit'] >= 4], case['path']
    print('PASS', case['path'])
