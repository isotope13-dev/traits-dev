#!/usr/bin/env python3
"""Static regression checks. Never executes sample code.

Pass the original DarkCore PE and the extracted/unpacked Salat and Xeno DLL.
Only same-length edits of a copy of the DarkCore PE are made.
"""
import argparse
import json
import os
from pathlib import Path
import subprocess
import tempfile

CLIPPER = 'objectives/impact/crypto-manipulation/clipboard::managed-multicoin-clipboard-replacement-template'
PERSISTENCE = 'objectives/persistence/login/registry/run-key::go-credential-stealer-run-key-write-profile'
CAPABILITY = 'micro-behaviors/mem/combined::game-reference-remote-memory-write-api-profile'


def scan(path):
    result = subprocess.run([os.environ.get('CLEAVE', 'cleave'), '--json', str(path)],
                            check=True, capture_output=True, text=True)
    assert 'validation failed' not in result.stderr, result.stderr
    report = json.loads(result.stdout)
    return {t['id']: t['crit'] for f in report['files'] for t in f.get('traits', [])}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--darkcore', type=Path, required=True)
    parser.add_argument('--salat', type=Path, required=True)
    parser.add_argument('--xeno-dll', type=Path, required=True)
    parser.add_argument('--scratch', type=Path, required=True)
    args = parser.parse_args()
    assert CLIPPER in scan(args.darkcore)
    data = args.darkcore.read_bytes()
    replacements = (
        (b'TrySetText(replacement', b'TryGetText(replacement'),
        (b'replacement = addr', b'candidate__ = addr'),
        (b'^0x[a-fA-F0-9]{40}', b'^0x[a-fA-F0-9]{41}'),
    )
    with tempfile.TemporaryDirectory(dir=args.scratch) as tmp:
        for index, (old, new) in enumerate(replacements):
            assert old in data and len(old) == len(new)
            path = Path(tmp) / f'one-leg-removed-{index}.exe'
            path.write_bytes(data.replace(old, new))
            assert CLIPPER not in scan(path), index
    assert PERSISTENCE in scan(args.salat)
    dll = scan(args.xeno_dll)
    assert dll[CAPABILITY] == 4
    assert 'objectives/impact/ransom/extortion::pe-ransom-extortion-content' not in dll
    assert not any(k.endswith('::pure-self-replicator') for k in dll)
    print('PASS: real clipper, three removed-leg controls, Salat persistence, Xeno DLL')


if __name__ == '__main__':
    main()
