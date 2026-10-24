#!/usr/bin/env python3
"""Static decoder and false-catalog regression controls; never execute fixtures."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
ECHO = 'micro-behaviors/data/decode/char-code::shell-echo-character-escapes'
BASE32 = 'micro-behaviors/data/decode/base32::shell-base32-decode'
OBF = 'objectives/anti-static/obfuscation/encoding/shell::shell-obfuscated-command-execution'
RECONSTRUCT = 'objectives/anti-static/obfuscation/code-metrics/structure::sh-reconstructed-command-name'
CATALOG = 'objectives/execution/exploit/command-injection::reverse-shell-variant-catalog'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cleave', default='cleave')
    parser.add_argument('--scratch', type=Path, required=True,
                        help='Existing scratch directory outside test/example paths')
    args = parser.parse_args()
    expected = {
        'echo-decoders.sh': {ECHO: 3},
        'echo-octal.sh': {ECHO: 3},
        'base32-decoders.sh': {BASE32: 3},
        'base32-long-option.sh': {BASE32: 3},
        'decoder-near-misses.sh': {},
        'command-built-printf.sh': {OBF: 4, RECONSTRUCT: 4},
        'socket-client-and-help.py': {},
    }
    with tempfile.TemporaryDirectory(prefix='decoder-', dir=args.scratch) as folder:
        targets = []
        for name in expected:
            dest = Path(folder) / name
            shutil.copyfile(HERE / name, dest)
            targets.append(str(dest))
        run = subprocess.run([args.cleave, '--no-update-check', '--traits-dir',
                              str(ROOT), '--json', *targets], cwd=ROOT,
                             capture_output=True, text=True, check=True)
        files = [f for line in run.stdout.splitlines()
                 for f in json.loads(line)['files'] if f.get('depth', 0) == 0]
        seen = set()
        for f in files:
            name = Path(f['path']).name
            traits = {t['id']: t['crit'] for t in f.get('traits', [])}
            assert CATALOG not in traits, (name, CATALOG)
            actual = {key: traits[key] for key in [ECHO, BASE32, OBF, RECONSTRUCT] if key in traits}
            assert actual == expected[name], (name, actual, expected[name], run.stderr)
            assert all(t['crit'] < 5 for t in f.get('traits', [])), name
            seen.add(name)
            print('PASS', name, actual)
        assert seen == set(expected), (seen, expected)


if __name__ == '__main__':
    main()
