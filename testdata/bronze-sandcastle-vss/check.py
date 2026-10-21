"""Check VSS acquisition across languages and source/destination near misses."""
import argparse
import json
from pathlib import Path
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--cleave', default='cleave')
parser.add_argument('--controls', type=Path, required=True)
args = parser.parse_args()
root = Path(__file__).resolve().parents[2]
prefix = 'objectives/credential-access/files/password-database::'
positive = root / 'testdata/hostile/bronze-sandcastle-vss'
gaps = Path(__file__).resolve().parent / 'fact-gaps'
result = subprocess.run(
    [args.cleave, '--traits-dir', str(root), '--format', 'jsonl',
     str(positive), str(args.controls), str(gaps)],
    check=True, capture_output=True, text=True,
)
if result.stderr.strip():
    raise AssertionError(result.stderr)
files = [f for line in result.stdout.splitlines()
         for f in json.loads(line).get('files', [])]
expected = {'.cmd': 'batch-shadow-copy-ntds-source',
            '.ps1': 'powershell-shadow-copy-ntds-source',
            '.c': 'native-shadow-copy-ntds-source',
            '.rs': 'native-shadow-copy-ntds-source',
            '.py': 'shadow-copy-ntds-copy-call',
            '.rb': 'shadow-copy-ntds-copy-call',
            '.php': 'shadow-copy-ntds-copy-call'}
seen = set()
for f in files:
    path = Path(f['path'])
    seen.add(path)
    ids = {x['id'] for x in f.get('traits', [])}
    if path.parent == positive:
        assert prefix + expected[path.suffix] in ids, path
        assert prefix + 'shadow-copy-ntds-dump' in ids, path
    else:
        assert not any(x.startswith(prefix) for x in ids), (path, ids)
        if path.parent == gaps:
            assert 'micro-behaviors/fs/path/account-db::shadow-copy-ntds-database-path' in ids, path
assert len(seen) == len(list(positive.iterdir())) + len(list(args.controls.iterdir())) + 2, seen
print(f'{len(seen)} VSS acquisition and near-miss checks passed')
