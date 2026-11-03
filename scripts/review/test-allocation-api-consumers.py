#!/usr/bin/env python3
"""General allocation consumers accept imports as well as API-name text."""
import argparse
from pathlib import Path
import subprocess

repo = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--cleave', default='../cleave/target/release/cleave')
args = parser.parse_args()
cleave = (repo / args.cleave).resolve()
consumer = 'objectives/execution/payload/process-inject/hollowing/process::process-hollowing-alloc-write-marker'
allocation = 'micro-behaviors/mem/alloc/virtual::virtual-alloc-ex-dup'
fixtures = [
    'testdata/notable/generated/thread-context-api-set/imports-only.dll',
    'testdata/notable/generated/thread-context-api-set/names-without-import-directory.dll',
]
for fixture in fixtures:
    result = subprocess.run(
        [str(cleave), '--traits-dir', str(repo), 'test-rules', '--rules', consumer, str(repo / fixture)],
        check=True, capture_output=True, text=True,
    )
    assert '✓ trait: ' + allocation in result.stdout, (fixture, result.stdout)
print('Generic allocation consumers accept both imports and name references.')
