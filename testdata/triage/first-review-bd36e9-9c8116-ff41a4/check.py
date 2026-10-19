"""Check benign manifest shapes and source-bound identity transfer fixtures."""
import json
import subprocess
from pathlib import Path
root = Path(__file__).resolve().parents[3]
report = subprocess.check_output(['cleave', '--traits-dir', str(root), '--format', 'json', str(Path(__file__).parent)], text=True)
decoder = json.JSONDecoder()
i = 0
while i < len(report):
    while i < len(report) and report[i].isspace():
        i += 1
    if i == len(report):
        break
    data, i = decoder.raw_decode(report, i)
    for file in data['files']:
        assert not [t for t in file.get('traits', []) if t['crit'] >= 4], file['path']
        if file['path'].endswith('package.json'):
            ids = {t['id'] for t in file['traits']}
            assert 'metadata/package/dependencies/manifest/source::npm-dependency-confusion-url-label' in ids
        print('PASS', file['path'])
subprocess.run(['python3', str(root / 'testdata/triage/hex-identity-benchmark/check.py')], check=True)
