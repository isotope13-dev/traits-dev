"""Run behavioral matcher controls without executing any specimen."""
import json
import os
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parents[3]
cases = json.loads(Path(__file__).with_name('cases.json').read_text())
paths = [str(root / case['path']) for case in cases]
env = dict(os.environ, CLEAVE_VALIDATE='0')
result = subprocess.run([env.get('CLEAVE', 'cleave'), '--traits-dir', str(root),
                         '--format', 'json', *paths], env=env,
                        capture_output=True, text=True, check=True)
stream = result.stdout.lstrip()
reports = {}
decoder = json.JSONDecoder()
while stream:
    report, consumed = decoder.raw_decode(stream)
    stream = stream[consumed:].lstrip()
    top = report['files'][0]
    reports[str(Path(top['path']).resolve())] = top
for case, path in zip(cases, paths):
    traits = {t['id'] for t in reports[path].get('traits', [])}
    for expected in case.get('present', []):
        assert expected in traits, (case['path'], 'missing', expected)
    for excluded in case.get('absent', []):
        assert excluded not in traits, (case['path'], 'unexpected', excluded)
print(json.dumps({'passed': len(cases), 'specimens_executed': False}))
