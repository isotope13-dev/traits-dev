"""Run focused positives and missing-role controls with the selected Cleave."""
from pathlib import Path
import argparse
import json
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--cleave', default='cleave')
args = parser.parse_args()
root = Path(__file__).resolve().parent
subprocess.run(['python3', str(root / 'generate.py')], check=True)
repo = root.parent.parent
result = subprocess.run(
    [args.cleave, '--traits-dir', str(repo), '--format', 'json', str(root)],
    check=True, capture_output=True, text=True,
)
decoder = json.JSONDecoder()
text = result.stdout
files = []
while text.strip():
    obj, end = decoder.raw_decode(text.lstrip())
    files.extend(obj['files'])
    text = text.lstrip()[end:]
cases = json.loads((root / 'cases.json').read_text())['fixtures']
for case in cases:
    filename = Path(case['path']).name
    file = next(f for f in files if Path(f['path']).name == filename)
    ids = {t['id'] for t in file.get('traits', [])}
    assert set(case['matched']) <= ids, (filename, 'missing', set(case['matched']) - ids)
    assert not set(case['not_matched']) & ids, (filename, 'unexpected', set(case['not_matched']) & ids)
print(f'{len(cases)} focused cases passed')
