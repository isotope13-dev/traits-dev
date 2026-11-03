#!/usr/bin/env python3
"""Check packet activation and cd00r indicators after taxonomy migration."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[2]
assert not (repo / 'objectives/command-and-control/trigger/packet').exists()
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--cleave', default='../cleave/target/release/cleave')
args = parser.parse_args()
with tempfile.TemporaryDirectory(prefix='packet-activation-') as tmp:
    root = Path(tmp)
    cases = {
        'knock.sh': 'nping --tcp -p 80 --flags SYN,RST,FIN --source-port 1200 --data=1234 -c 1 example.com\n',
        'ordinary.sh': 'nping --tcp -p 80 --flags SYN --source-port 1200 example.com\n',
        'cd00r.c': '#define CDR_PORTS 1\n#define CDR_CODERESET 1\n#define CDR_SENDER_ADDR 1\n/* packet coded backdoor */\nvoid cdr_open_door(void) {}\n',
        'unrelated.c': 'void open_door(void) {}\n',
    }
    for name, source in cases.items():
        (root / name).write_text(source)
    result = subprocess.run(
        [str((repo / args.cleave).resolve()), '--traits-dir', str(repo), '--min-crit', 'component',
         '--format=json', *(str(root / name) for name in cases)],
        check=True, capture_output=True, text=True,
    )
    reports = [json.loads(line)['files'][0] for line in result.stdout.splitlines() if line]
    ids = {Path(r['path']).name: {t['id'] for t in r.get('traits', [])} for r in reports}
    activation = 'objectives/execution/trigger/packet::nping-backdoor-activation'
    family = 'well-known/malware/backdoor/cd00r::source'
    assert activation in ids['knock.sh'], ids['knock.sh']
    assert activation not in ids['ordinary.sh']
    assert family in ids['cd00r.c'], ids['cd00r.c']
    assert family not in ids['unrelated.c']
    print('Packet activation and cd00r evidence remain distinct from ordinary traffic.')
