#!/usr/bin/env python3
"""A `.pyc` of every CPython release from 3.8 to 3.16 yields its string constants.

Each `token_client-<release>.pyc` fixture was compiled from the same module,
whose `BOT_TOKEN` constant is a Telegram-format token, and each
`hex_secret_client-<release>.pyc` from a near miss whose secret is hex. The
token rule must fire on every release's token module and on no near miss: a
release whose bytecode the engine cannot read would drop the finding.
"""
import argparse
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]
FIXTURES = ROOT / 'testdata/notable/generated/pyc-versions'
RULE = 'micro-behaviors/communications/http/auth::hardcoded-telegram-bot-token-bytecode'
RELEASES = ['38', '39', '310', '311', '312', '313', '314', '315', '316']

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--cleave', default='../cleave/target/release/cleave')
args = parser.parse_args()
names = [f'{module}-{release}.pyc' for release in RELEASES for module in ('token_client', 'hex_secret_client')]
result = subprocess.run(
    [str((ROOT / args.cleave).resolve()), '--traits-dir', str(ROOT), '--min-crit', 'component',
     '--format=json', *(str(FIXTURES / name) for name in names)],
    check=True, capture_output=True, text=True,
)
reports = [json.loads(line)['files'][0] for line in result.stdout.splitlines() if line]
ids = {Path(r['path']).name: {t['id'] for t in r.get('traits', [])} for r in reports}
assert sorted(ids) == sorted(names), sorted(set(names) - set(ids))
for name in names:
    expected = name.startswith('token_client-')
    assert (RULE in ids[name]) == expected, (name, expected)
    print(f'{name}: passed', flush=True)
