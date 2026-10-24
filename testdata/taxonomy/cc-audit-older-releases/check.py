#!/usr/bin/env python3
"""Statically check relocated evidence and encoded deletion targets."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
LOADS = 'metadata/lang/source/syntax/call/invocation::python-loads-bytes-literal-text'
HEX = 'micro-behaviors/data/decode/char-code::shell-printf-hex-byte-sequence'
CURL = 'micro-behaviors/communications/http/curl::javascript-exec-curl-command-text'
PRINTF = 'micro-behaviors/communications/http/curl::printf-curl-name-format'
DELETE = 'objectives/impact/destroy/encoded-payload::shell-encoded-root-delete-command'
BEACON = 'objectives/command-and-control/channel/transport::raw-ip-netcat-binary-protocol-loop'
MARSHAL = 'objectives/command-and-control/dropper/builder::python-marshal'
RETIRED = {
    'objectives/command-and-control/dropper/builder::loads-b',
    'micro-behaviors/data/encode/hex::shell-hex-byte-sequence',
    'micro-behaviors/communications/http/download/curl::curl-in-js-exec',
    'micro-behaviors/communications/http/download/curl::printf-curl-name-format',
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--scratch', type=Path, required=True)
    parser.add_argument('--cleave', default='cleave')
    args = parser.parse_args()
    checks = {
        'byte-loads.py': ({LOADS: 3}, set()),
        'loads-near-miss.py': ({}, {LOADS}),
        'marshal-wrapper.py': ({LOADS: 3, MARSHAL: 4}, set()),
        'hex-fragment.sh': ({HEX: 3}, set()),
        'hex-near-miss.sh': ({}, {HEX}),
        'hex-netcat-loop.sh': ({HEX: 3, BEACON: 5}, set()),
        'printf-curl.sh': ({PRINTF: 3}, set()),
        'printf-name-only.sh': ({PRINTF: 3}, set()),
        'exec-curl.js': ({CURL: 3}, set()),
        'exec-near-miss.js': ({}, {CURL}),
        'encoded-root.sh': ({DELETE: 4}, set()),
        'encoded-temp.sh': ({}, {DELETE}),
        'encoded-home.sh': ({}, {DELETE}),
        'encoded-git.sh': ({}, {DELETE}),
        'plain-root-string.sh': ({}, {DELETE}),
    }
    # Filenames and test-directory exclusions must not determine these checks.
    with tempfile.TemporaryDirectory(prefix='cc-audit-controls-', dir=args.scratch) as tmp:
        paths = []
        for name in checks:
            dest = Path(tmp) / name
            shutil.copyfile(HERE / name, dest)
            paths.append(str(dest))
        run = subprocess.run(
            [args.cleave, '--no-update-check', '--traits-dir', str(ROOT),
             '--json', *paths], capture_output=True, text=True, check=True)
        seen = set()
        for line in run.stdout.splitlines():
            for file in json.loads(line)['files']:
                if file.get('depth', 0):
                    continue
                name = Path(file['path']).name
                traits = {t['id']: t['crit'] for t in file.get('traits', [])}
                present, absent = checks[name]
                assert not RETIRED.intersection(traits), (name, RETIRED.intersection(traits))
                assert not absent.intersection(traits), (name, absent.intersection(traits))
                for key, crit in present.items():
                    assert traits.get(key) == crit, (name, key, traits.get(key), crit)
                seen.add(name)
                print('PASS', name)
        assert seen == set(checks), (seen, set(checks))


if __name__ == '__main__':
    main()
