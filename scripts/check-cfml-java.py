#!/usr/bin/env python3
"""Java class construction must not supply a process-execution leg."""
import argparse
import json
from pathlib import Path
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--cleave', default='cleave')
args = parser.parse_args()
root = Path(__file__).resolve().parents[1]
for name in ['java-only', 'maintenance']:
    path = root / 'testdata/taxonomy/cfml-java' / (name + '.cfm')
    scan = subprocess.run([args.cleave, '--traits-dir', str(root), '--format', 'json', str(path)],
                          capture_output=True, text=True, check=True)
    traits = [t for f in json.loads(scan.stdout)['files'] for t in f['traits']]
    ids = {t['id'] for t in traits}
    assert 'micro-behaviors/process/interpreter/runtime/jvm::cfml-java-createobject' in ids
    assert 'micro-behaviors/process/create/exec::cfm-java-object-instantiation' not in ids
    assert not [t for t in traits if t['crit'] >= 5], (name, traits)
    assert not [t for t in traits if t['crit'] >= 4], (name, traits)
    print(name + ': zero hostile or suspicious findings')
