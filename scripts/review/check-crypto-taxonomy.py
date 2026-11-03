#!/usr/bin/env python3
"""Reject legacy algorithm-nested crypto operations and references."""
import argparse
from pathlib import Path
import re

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--traits-dir', type=Path, default=Path(__file__).resolve().parents[2])
args = parser.parse_args()
root = args.traits_dir
crypto = root / 'micro-behaviors/crypto'
operation_names = {'encrypt', 'decrypt', 'sign', 'verify'}
legacy_ref = re.compile(
    r'micro-behaviors/crypto/(?:symmetric/(?:[a-z0-9-]+/)+(?:encrypt|decrypt|sign|verify)'
    r'|asymmetric/(?:encrypt|signature))(?=/|::|[\s"\']|$)'
)
errors = []
for path in (crypto / 'symmetric').rglob('*'):
    if path.is_dir() and path.name in operation_names:
        errors.append(f'{path.relative_to(root)}: retired algorithm-nested operation directory')
for name in ('encrypt', 'signature'):
    path = crypto / 'asymmetric' / name
    if path.is_dir():
        errors.append(f'{path.relative_to(root)}: retired asymmetric directory')
for namespace in ('metadata', 'micro-behaviors', 'objectives', 'well-known'):
    for path in (root / namespace).rglob('*'):
        if not path.is_file() or path.suffix not in ('.yaml', '.yml'):
            continue
        for number, line in enumerate(path.read_text().splitlines(), 1):
            if not line.lstrip().startswith('#') and legacy_ref.search(line):
                errors.append(f'{path.relative_to(root)}:{number}: retired crypto reference')
if errors:
    print('\n'.join(errors))
    raise SystemExit(1)
print('Crypto taxonomy: retired operation directories and references absent.')
