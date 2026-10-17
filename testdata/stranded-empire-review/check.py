"""Check saved atomscan JSONL against this directory's focused cases."""
import json
import sys
from pathlib import Path

cases = json.loads(Path(__file__).with_name('cases.json').read_text())['fixtures']
reports = {}
for line in Path(sys.argv[1]).read_text().splitlines():
    for item in json.loads(line)['raw']['files']:
        if '!!' not in item['path'] and '##' not in item['path']:
            reports[str(Path(item['path']).resolve())] = item
for case in cases:
    report = reports[str(Path(case['path']).resolve())]
    traits = {t['id']: t for t in report.get('traits', [])}
    assert set(case['matched']) <= traits.keys(), (case['path'], 'missing', set(case['matched']) - traits.keys())
    assert not set(case['not_matched']) & traits.keys(), (case['path'], 'unexpected')
    assert not any(t['crit'] == 5 for t in traits.values()), (case['path'], 'hostile false positive')
    assert sum(t['crit'] == 4 for t in traits.values()) <= 1, (case['path'], 'suspicious count')
print(f'{len(cases)} focused controls passed')
