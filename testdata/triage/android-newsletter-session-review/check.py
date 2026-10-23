"""Check focused detection boundaries; run from the trait repository root."""
import json
import subprocess
from pathlib import Path

root = Path(__file__).parent
cases = json.loads((root/'cases.json').read_text())['fixtures']
result = subprocess.run(['cleave', '--traits-dir', '.', '--format', 'json', *[c['path'] for c in cases]], text=True, capture_output=True, check=True)
text = result.stdout
reports = {}
decoder = json.JSONDecoder()
while text.strip():
    text = text.lstrip()
    data, end = decoder.raw_decode(text)
    text = text[end:]
    for f in data.get('files', []):
        reports[Path(f['path']).name] = {t['id'] for t in f.get('traits', [])}
for case in cases:
    got = reports[Path(case['path']).name]
    assert not (set(case['matched'])-got), (case['path'], 'missing', set(case['matched'])-got)
    assert not (set(case['not_matched'])&got), (case['path'], 'unexpected', set(case['not_matched'])&got)
print(f'{len(cases)} focused fixtures passed')
