"""Check bound clipboard overwrite detection and address placement controls."""
import argparse
import json
import subprocess
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--cleave', default='cleave')
parser.add_argument('--controls', type=Path, required=True)
args = parser.parse_args()
root = Path(__file__).resolve().parents[2]
fixtures = Path(__file__).resolve().parent
paths = sorted(p for p in fixtures.iterdir() if p.suffix in {'.py', '.js', '.ts'} and p.name != 'check.py')
paths += sorted(args.controls.iterdir())
result = subprocess.run([args.cleave, '--traits-dir', str(root), '--json', *map(str, paths)], check=True, text=True, capture_output=True)
reports = {}
for line in result.stdout.splitlines():
    for report in json.loads(line).get('files', []):
        reports[Path(report['path']).name] = {t['id'] for t in report.get('traits', [])}
prefix = 'objectives/impact/crypto-manipulation/clipboard::'
hostile = prefix + 'polled-eth-clipboard-hijacker'
positives = {'positive.py', 'renamed.py', 'positive.js', 'renamed.ts'}
assert set(reports) == {p.name for p in paths}, 'missing fixture reports'
for name, traits in reports.items():
    assert (hostile in traits) == (name in positives), (name, 'unexpected hostile result')
    if name not in positives:
        assert not any('polled-eth-address-overwrite' in t for t in traits), name
assert prefix + 'py-clipboard-wallet-btc' in reports['btc-only.py']
for name in ['eth-only.py', 'documentation.py']:
    assert prefix + 'py-clipboard-wallet-btc' not in reports[name], name
moved = ['bitcoin-legacy-regex', 'bitcoin-segwit-regex', 'bitcoin-cash-regex',
         'litecoin-segwit-regex', 'litecoin-legacy-regex', 'tron-regex',
         'solana-regex', 'bitcoin-legacy-regex-short', 'bitcoin-cash-prefix',
         'multi-crypto-regex']
for trait in moved:
    assert 'micro-behaviors/data/format/crypto-address::' + trait in reports['address-patterns.py'], trait
    assert not any(t.endswith('::' + trait) for t in reports['no-address-patterns.py']), trait
print(f'{len(reports)} fixtures passed; 4 overwrite variants and all near misses verified.')
