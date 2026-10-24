import json
from pathlib import Path
import sys

s = Path(sys.argv[1]).read_text()
decoder = json.JSONDecoder()
files = {}
while s.strip():
    report, end = decoder.raw_decode(s.lstrip())
    s = s.lstrip()[end:]
    for f in report['files']:
        files[Path(f['path']).name] = {t['id'] for t in f.get('traits', [])}
cases = json.loads(Path(__file__).with_name('cases.json').read_text())
for name, case in cases.items():
    assert name in files, name
    for trait in case.get('present', []):
        assert trait in files[name], (name, 'missing', trait)
    for trait in case.get('absent', []):
        assert trait not in files[name], (name, 'unexpected', trait)
print(f'PASS: {len(cases)} focused controls')
