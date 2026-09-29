#!/usr/bin/env python3
"""Check CFML file provenance through Cleave without executing sample source."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

p = argparse.ArgumentParser()
p.add_argument('--cleave', default='cleave')
a = p.parse_args()
r = Path(__file__).resolve().parents[1]
fixtures = r / 'testdata/taxonomy/cfml-file-flow'
assert hashlib.sha256((fixtures / 'original-file-shell.cfm').read_bytes()).hexdigest() == (
    'c349de0e5fd85a6603d3edc01a2efff254b0a8a85288a7419c9750e24fc29589'
)
positive = {'direct-request', 'aliased-request', 'original-file-shell', 'request-accessor', 'replace-write'}
expected = {
    'request-accessor': (True, True),
    'wrong-accessor': (False, True),
    'replace-write': (True, True),
    'replace-search-only': (True, False),
    'opaque-call': (True, False),
    'direct-request': (True, True),
    'aliased-request': (True, True),
    'original-file-shell': (True, True),
    'fixed-paths': (False, False),
    'unrelated-request': (False, False),
    'read-only-request': (True, False),
    'content-only-request': (False, False),
    'split-write-calls': (True, False),
    'overwritten-alias': (False, False),
}
paths = sorted(fixtures.glob('*.cfm'))
assert {path.stem for path in paths} == set(expected)
for path in paths:
    result = subprocess.run(
        [a.cleave, '--traits-dir', str(r), '--format', 'json', str(path)],
        capture_output=True, text=True, check=True,
    )
    traits = [t for f in json.loads(result.stdout)['files'] for t in f.get('traits', [])]
    ids = {t['id'] for t in traits}
    observed = (
        bool(ids & {
            'micro-behaviors/fs/read/file/full::cffile-request-read-path',
            'micro-behaviors/fs/read/file/full::cffile-parameter-read-path',
        }),
        'micro-behaviors/fs/write/content::cffile-request-write-path-content' in ids,
    )
    assert observed == expected[path.stem], (path.name, observed, traits)
    match = 'objectives/command-and-control/backdoor/webshell/file-manager::cfml-browser-file-webshell' in ids
    assert match == (path.stem in positive), (path.name, traits)
    if path.stem not in positive:
        assert not [t for t in traits if t['crit'] >= 4], (path.name, traits)
    print(path.stem + ': passed', flush=True)
