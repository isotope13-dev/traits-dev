#!/usr/bin/env python3
"""Check scan evidence for PostgreSQL exploit and benign boundary fixtures."""
import json
import sys
from pathlib import Path


def files(path):
    for line in Path(path).read_text().splitlines():
        report = json.loads(line)
        yield from report.get('raw', report)['files']


hostile_ids = {
    'objectives/privilege-escalation/exploit/database::pg-cron-definer-backdoor',
    'objectives/execution/exploit/service-command-injection::large-object-archive-command-overwrite',
}
positive = list(files(sys.argv[1]))
assert {Path(f['path']).name for f in positive} == {
    'reconstructed-chain.sql', 'driver-variant.py', 'powershell-client.ps1',
}
for f in positive:
    traits = {t['id']: t for t in f['traits']}
    assert all(traits.get(i, {}).get('crit') == 5 for i in hostile_ids), f['path']
    assert sum(t.get('crit') == 5 for t in f['traits']) >= 2, f['path']
    assert 'objectives/supply-chain/credential-theft/env::py-harvest-database-url' not in traits

controls = list(files(sys.argv[2]))
assert len(controls) == 8, len(controls)
for f in controls:
    traits = {t['id']: t for t in f['traits']}
    assert not hostile_ids.intersection(traits), f['path']
    if Path(f['path']).name == 'database-client.py':
        assert traits['micro-behaviors/os/env/config::python-database-url']['crit'] == 3
    if Path(f['path']).name == 'mixed-maintenance.sql':
        assert 'micro-behaviors/data/db/postgresql::definer-dynamic-query' not in traits
    if Path(f['path']).name == 'unrelated-env.py':
        assert 'micro-behaviors/os/env/config::python-database-url' not in traits
print(f'{len(positive)} exploit samples meet the hostile floor; {len(controls)} controls pass')
