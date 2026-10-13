"""Cookie-client capability is visible without unsupported theft claims.

Scan both archive controls and related source/redirect controls. No fixture
code is executed. Assert severity as well as presence so neutral observations
cannot silently regain hostile severity.
"""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

root = Path(__file__).resolve().parents[3]
cases = json.loads(Path(__file__).with_name('cases.json').read_text())['fixtures']
controls = Path(__file__).parent.parent / 'pi-cookie-client-triage'
cases += json.loads((controls / 'cases.json').read_text())['fixtures']
# Keep standalone controls outside testdata so path-based test exclusions
# cannot hide the directory-enumeration observation being exercised.
with tempfile.TemporaryDirectory(prefix='pi-cookie-controls-') as scratch:
    for path in controls.iterdir():
        if path.suffix in ('.js', '.ts'):
            shutil.copyfile(path, Path(scratch) / path.name)
    result = subprocess.run(
        [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(root), '--format', 'json',
         str(Path(__file__).parent), scratch],
        cwd=root, capture_output=True, text=True, check=True,
    )
remaining = result.stdout.strip()
decoder = json.JSONDecoder()
files = {}
while remaining:
    report, consumed = decoder.raw_decode(remaining)
    remaining = remaining[consumed:].lstrip()
    for entry in report['files']:
        path = Path(entry['path'])
        if path.parent == Path(scratch):
            path = (controls / path.name).relative_to(root)
        elif path.is_absolute():
            path = path.relative_to(root)
        files[str(path)] = {trait['id']: trait['crit'] for trait in entry.get('traits', [])}
checks = 0
for case in cases:
    actual = files[case['path']]
    for expected, present in [('matched', True), ('not_matched', False)]:
        for trait in case[expected]:
            assert (trait in actual) == present, (case['path'], expected, trait)
            checks += 1
    for trait, criticality in case.get('criticality', {}).items():
        assert actual[trait] == criticality, (case['path'], trait, actual[trait], criticality)
        checks += 1
print(f'{checks} trait assertions passed')
