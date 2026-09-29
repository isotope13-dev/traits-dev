#!/usr/bin/env python3
"""Static controls for math imports and Mach-O code/string ratios."""
import argparse
import json
from pathlib import Path
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--cleave', required=True)
args = parser.parse_args()
root = Path(__file__).resolve().parent.parent
fixtures = root / 'testdata/taxonomy/macos-math-imports'
math = 'micro-behaviors/dylib/library/libm::'
combined = 'micro-behaviors/process/create/api-system::system-with-math-imports'
ratio = 'metadata/binary/section/ratio::text-dominates-cstring'
for name, imports, padded in [('math-shell.macho', True, False),
                               ('math-shell-padded.macho', True, True),
                               ('math-exports.dylib', False, False)]:
    result = subprocess.run([args.cleave, '--traits-dir', str(root), '--format',
                             'json', str(fixtures / name)], capture_output=True,
                            text=True, check=True)
    traits = json.loads(result.stdout)['files'][0]['traits']
    ids = {t['id']: t for t in traits}
    assert not [t for t in traits if t['crit'] >= 4], name
    assert 'objectives/anti-static/obfuscation/payload/encrypted::math-cipher-imports' not in ids
    assert 'metadata/binary/code/density::text-dominates-cstring' not in ids
    matches = [t for t in traits if t['id'].startswith(math)]
    assert len(matches) == (8 if imports else 0), (name, matches)
    assert all(t['crit'] == 3 for t in matches)
    assert (combined in ids) == imports, name
    if padded:
        assert ids[ratio]['crit'] == 3
    print(f'{name}: passed')
