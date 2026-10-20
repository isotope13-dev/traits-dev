"""Check path relationships and import-table evidence without running samples."""
import json
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parents[3]
case_path = Path(__file__).with_name('cases.json')
cases = json.loads(case_path.read_text())['fixtures']
command = [sys.argv[1] if len(sys.argv) > 1 else 'cleave',
           '--traits-dir', str(root), '--json', str(case_path.parent)]
result = subprocess.run(command, cwd=root, capture_output=True, text=True,
                        check=True)
reports = {}
for line in result.stdout.splitlines():
    for file in json.loads(line)['files']:
        reports[Path(file['path']).resolve()] = {
            trait['id']: trait['crit'] for trait in file.get('traits', [])}
for case in cases:
    traits = reports[(root / case['path']).resolve()]
    missing = set(case['matched']) - traits.keys()
    unexpected = set(case['not_matched']) & traits.keys()
    assert not missing, (case['path'], 'missing', missing)
    assert not unexpected, (case['path'], 'unexpected', unexpected)
    if 'max_crit' in case:
        assert max(traits.values(), default=0) <= case['max_crit'], case['path']
    print(Path(case['path']).name + ': PASS')
print(f'{len(cases)} behavioral controls passed')
