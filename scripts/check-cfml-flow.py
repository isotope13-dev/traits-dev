#!/usr/bin/env python3
"""End-to-end command provenance, without executing any CFML source."""
import argparse
import json
from pathlib import Path
import subprocess
p = argparse.ArgumentParser()
p.add_argument('--cleave', default='cleave')
a = p.parse_args()
r = Path(__file__).resolve().parents[1]
positive = {'alias-request', 'direct-request', 'guarded-command'}
for path in sorted((r/'testdata/taxonomy/cfml-flow').glob('*.cfm')):
    result = subprocess.run([a.cleave, '--traits-dir', str(r), '--format', 'json', str(path)], capture_output=True, text=True, check=True)
    traits = [t for f in json.loads(result.stdout)['files'] for t in f.get('traits', [])]
    ids = {t['id'] for t in traits}
    match = 'objectives/command-and-control/backdoor/webshell/request::cfml-request-command-shell' in ids
    assert match == (path.stem in positive), (path.name, traits)
    if path.stem not in positive:
        assert not [t for t in traits if t['crit'] >= 4], (path.name, traits)
    print(path.stem + ': passed')
