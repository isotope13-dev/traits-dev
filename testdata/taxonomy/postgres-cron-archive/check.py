"""Static controls only; never execute the database payload fixtures."""
import json
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parents[3]
base = Path(__file__).resolve().parent
cases = json.loads((base / 'cases.json').read_text())
command = [sys.argv[1] if len(sys.argv) > 1 else 'cleave', '--traits-dir',
           str(root), '--format', 'json', *[str(base / c['path']) for c in cases]]
result = subprocess.run(command, check=True, capture_output=True, text=True)
reports = {}
decoder = json.JSONDecoder()
remaining = result.stdout.strip()
while remaining:
    document, end = decoder.raw_decode(remaining)
    reports.update({Path(f['path']).name: f for f in document['files']})
    remaining = remaining[end:].lstrip()
old_prefixes = ('objectives/supply-chain/credential-theft/env::py-harvest-database-url',
                'micro-behaviors/fs/path/config/accounts::unix-account-database-path-reference',
                'micro-behaviors/fs/path/config/accounts::etc-passwd-read')
for case in cases:
    report = reports[case['path']]
    traits = {t['id']: t for t in report['traits']}
    hostile = {i for i, t in traits.items() if t['crit'] == 5}
    assert hostile == set(case['hostile']), (case['path'], hostile)
    assert not any(i in traits for i in old_prefixes), case['path']
    if case['path'] == 'connection-only.py':
        assert 'micro-behaviors/os/env/config::python-database-url' in traits
        assert 'micro-behaviors/data/db/access::psycopg-connect-call' in traits
        assert not any(t['crit'] >= 4 for t in traits.values()), traits
    if case['path'] == 'client.ps1':
        assert 'micro-behaviors/process/create/exec::powershell-call-exe' in traits
    if case['path'] == 'path-only.py':
        assert 'micro-behaviors/fs/path/account-db::unix-account-database-path-reference' in traits
        assert 'micro-behaviors/fs/read/file/target::etc-passwd-read' not in traits
    if case['path'] == 'account-read.py':
        assert 'micro-behaviors/fs/read/file/target::etc-passwd-read' in traits
    print('PASS', case['path'])
