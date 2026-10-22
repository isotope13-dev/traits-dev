"""Verify the reviewed source-to-sink claims and neutral capability controls."""
import json
import pathlib
import subprocess
import sys
root = pathlib.Path(__file__).resolve().parents[3]
cases = json.loads(pathlib.Path(__file__).with_name('cases.json').read_text())['fixtures']
result = subprocess.run([sys.argv[1] if len(sys.argv) > 1 else 'cleave', '--traits-dir', str(root), '--json', *[str(root / c['path']) for c in cases]], capture_output=True, text=True, check=True)
reports = {}
for line in result.stdout.splitlines():
    for f in json.loads(line)['files']:
        reports[pathlib.Path(f['path']).resolve()] = {t['id'] for t in f.get('traits', [])}
for c in cases:
    traits = reports[(root / c['path']).resolve()]
    for trait in c['matched']:
        assert trait in traits, (c['path'], 'missing', trait, result.stderr)
    for trait in c['not_matched']:
        assert trait not in traits, (c['path'], 'unexpected', trait)
assert not result.stderr.strip(), result.stderr
print(f'{len(cases)} focused cases passed')
