#!/usr/bin/env python3
"""Check lifecycle commands and retained injection/rewrite consumers statically."""
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[3]
CLEAVE = os.environ.get('CLEAVE', 'cleave')
P = 'micro-behaviors/os/package-manager/hook-install::'

def documents(text):
    decoder = json.JSONDecoder()
    while text.strip():
        value, end = decoder.raw_decode(text.lstrip())
        yield value
        text = text.lstrip()[end:]


def check_cases(filename):
    cases = json.loads(filename.read_text())['cases']
    result = subprocess.run([CLEAVE, '--traits-dir', str(ROOT), '--format', 'json'] +
                            [str(ROOT / c['path']) for c in cases],
                            capture_output=True, text=True, check=True)
    reports = {f['path']: f for report in documents(result.stdout) for f in report['files']}
    for case in cases:
        traits = {t['id']: t for t in reports[str(ROOT / case['path'])].get('traits', [])}
        # A pure OR group can be omitted as redundant in rendered findings.
        expected = set(case['matched']) - {P + 'install-hook-runs-pkg-install'}
        assert expected <= traits.keys(), (case['path'], set(case['matched']) - traits.keys())
        assert not set(case['not_matched']) & traits.keys(), (case['path'], set(case['not_matched']) & traits.keys())
        for ident, trait in traits.items():
            if ident.startswith(P) and ident.split('::')[1] in {
                'preinstall-runs-npm-install', 'postinstall-runs-npm-install',
                'preinstall-runs-yarn-add', 'postinstall-runs-yarn-add',
                'preinstall-runs-pnpm-add', 'postinstall-runs-pnpm-add',
                'install-hook-runs-pkg-install', 'preinstall-runs-npm-ci'}:
                assert trait['crit'] == 3, (ident, trait)
        print('PASS', case['path'])


if __name__ == '__main__':
    check_cases(ROOT / 'testdata/triage/nuxeo-lifecycle/cases.json')
    check_cases(ROOT / 'testdata/triage/vscode-version-drift/cases.json')
