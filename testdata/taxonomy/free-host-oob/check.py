#!/usr/bin/env python3
"""Check free-hosting versus OOB classification without executing fixtures."""
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
host = 'micro-behaviors/communications/url/host::free-host-gt-tc-domain'
collector = 'micro-behaviors/communications/url/host::oob-endpoint-any'
exfil = 'objectives/exfiltration/oob/endpoint::js-fetch-json-post-oob'
cases = {
    'free-host-api.js': ({host}, {collector, exfil}),
    'collector-post.js': ({collector, exfil}, {host}),
    'unrelated-api.js': (set(), {host, collector, exfil}),
}
# Neutral paths prevent fixture-directory exclusions from masking a regression.
with tempfile.TemporaryDirectory(prefix='free-host-controls-') as staging:
    paths = []
    for name in cases:
        target = Path(staging) / name
        shutil.copyfile(fixtures / name, target)
        paths.append(str(target))
    output = subprocess.run(
        [args.cleave, '--no-update-check', '--traits-dir', str(root),
         '--format=json', *paths], check=True, capture_output=True, text=True).stdout
    decoder = json.JSONDecoder()
    reports = {}
    while output.strip():
        report, end = decoder.raw_decode(output.lstrip())
        output = output.lstrip()[end:]
        reports.update({Path(file['path']).name: file for file in report['files']})
    for name, (required, forbidden) in cases.items():
        traits = reports[name].get('traits', [])
        ids = {trait['id'] for trait in traits}
        assert required <= ids, (name, 'missing', required - ids)
        assert not forbidden & ids, (name, 'unexpected', forbidden & ids)
        if name != 'collector-post.js':
            assert not any(trait['crit'] >= 4 for trait in traits), (name, traits)
print(f'{len(cases)} free-host/OOB controls passed')
