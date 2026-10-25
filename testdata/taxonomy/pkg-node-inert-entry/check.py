#!/usr/bin/env python3
"""Verify inert carriers retain observations and the real dropper retains intent.

No sample is executed. --inert accepts both original small carriers, and
--positive names the recovered original pkg executable.
"""
import argparse
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
OLD = 'objectives/command-and-control/dropper/staging/runtime::pkg-node-bundle-with-admin-check-and-hidden-defender-exclusion'
EVASION = 'objectives/evasion/anti-av/exclusion::pkg-node-bundle-with-admin-check-and-hidden-defender-exclusion'
TEMP = 'micro-behaviors/os/security/defender::defender-exclusion-temp-environment'
ENCODED = 'objectives/anti-static/obfuscation/encoding/content::encoded-powershell'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--inert', type=Path, action='append', required=True)
    ap.add_argument('--positive', type=Path, required=True)
    ap.add_argument('--scratch', type=Path, required=True)
    args = ap.parse_args()
    cases = []
    with tempfile.TemporaryDirectory(prefix='pkg-entry-', dir=args.scratch) as tmp:
        for n, path in enumerate(args.inert):
            renamed = Path(tmp) / f'carrier-{n}.exe'
            renamed.write_bytes(path.read_bytes())
            cases.append((renamed, {TEMP, ENCODED}, {EVASION, OLD}))
        cases.append((args.positive, {EVASION, TEMP, ENCODED}, {OLD}))
        for name, text, yes in [
            ('temp-option', '-ExclusionPath $env:TEMP', True),
            ('tmp-option', '-ExclusionPath %TMP%', True),
            ('query-only', 'Get-MpPreference | Select-Object ExclusionPath', False),
            ('temp-without-option', '$env:TEMP', False),
        ]:
            path = Path(tmp) / (name + '.ps1')
            path.write_text(text + '\n')
            cases.append((path, {TEMP} if yes else set(), {EVASION, OLD} | (set() if yes else {TEMP})))
        output = subprocess.check_output([
            os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
            '--format', 'json', '--disable', 'third-party',
            *[str(path) for path, _, _ in cases],
        ]).decode().lstrip()
        files = {}
        decoder = json.JSONDecoder()
        while output:
            report, end = decoder.raw_decode(output)
            files.update({f['path']: {t['id'] for t in f.get('traits', [])}
                          for f in report['files']})
            output = output[end:].lstrip()
        for path, yes, no in cases:
            actual = files[str(path)]
            assert yes <= actual, (path.name, 'missing', sorted(yes - actual))
            assert not no & actual, (path.name, 'unexpected', sorted(no & actual))
            print('PASS', path.name)
    print(f'{len(cases)} static controls passed')


if __name__ == '__main__':
    main()
