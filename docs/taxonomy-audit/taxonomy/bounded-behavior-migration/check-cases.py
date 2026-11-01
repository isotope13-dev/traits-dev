"""Check observed raw traits from one or more local atomscan JSONL reports."""
from pathlib import Path
import json
import sys
here = Path(__file__).resolve().parent
expected = json.loads((here / 'expected.json').read_text())
actual = {}
for name in sys.argv[1:]:
    for line in Path(name).read_text().splitlines():
        report = json.loads(line)
        for file in report['raw']['files']:
            actual[Path(file['path']).name] = {t['id'] for t in file.get('traits', [])}
errors = []
for name, assertions in expected.items():
    if name not in actual:
        errors.append(f'{name}: missing scan')
        continue
    missing = set(assertions['present']) - actual[name]
    unexpected = set(assertions['absent']) & actual[name]
    if missing or unexpected:
        errors.append(f'{name}: missing={sorted(missing)}, unexpected={sorted(unexpected)}')
if errors:
    print('\n'.join(errors))
    raise SystemExit(1)
print(f'Passed {len(expected)} positive and near-miss cases')
