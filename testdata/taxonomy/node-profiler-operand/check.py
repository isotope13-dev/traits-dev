#!/usr/bin/env python3
"""Verify profiler operands without executing npm scripts."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument('--cleave', default='cleave')
args = parser.parse_args()
fixtures = Path(__file__).resolve().parent
root = fixtures.parents[2]
trait = 'objectives/evasion/masquerade/extension-mismatch::npm-script-node-non-script-suffix'
cases = {
    'profiler': False,
    'payload-after-profiler': True,
    'payload-before-profiler': True,
    'profiled-script': True,
    # `node ./commands/change.pack` resolves change.pack.js: `.pack` is the
    # trailing stem word of a compound script name, like `.spec`.
    'pack-compound': False,
}
with tempfile.TemporaryDirectory(prefix='node-operand-controls-') as staging:
    paths = []
    for name in cases:
        target = Path(staging) / name / 'package.json'
        target.parent.mkdir()
        shutil.copyfile(fixtures / name / 'package.json', target)
        paths.append(str(target))
    output = subprocess.run(
        [args.cleave, '--no-update-check', '--traits-dir', str(root),
         '--format=json', *paths], check=True, capture_output=True, text=True).stdout
    decoder = json.JSONDecoder()
    reports = {}
    while output.strip():
        report, end = decoder.raw_decode(output.lstrip())
        output = output.lstrip()[end:]
        reports.update({Path(file['path']).parent.name: file for file in report['files']})
    for name, expected in cases.items():
        traits = reports[name].get('traits', [])
        ids = {finding['id'] for finding in traits}
        assert (trait in ids) == expected, (name, expected, ids)
        if not expected:
            assert not any(finding['crit'] >= 4 for finding in traits), (name, traits)
print(f'{len(cases)} Node profiler operand controls passed')
