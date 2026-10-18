#!/usr/bin/env python3
"""Static regression controls. This never executes a fixture shell script."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument('--cleave', default='cleave')
parser.add_argument('--work-dir', required=True)
args = parser.parse_args()
seed = Path(__file__).with_name('loader.sh').read_text()
payload = 'objectives/execution/payload/file-exec::shell-curl-hidden-chmod-detached-script'
decoy = 'objectives/evasion/decoy/lure::authentication-success-hidden-shell-payload'
raw_ip = 'objectives/command-and-control/dropper/file-exec/command/shell::raw-ip-shell-fetch-chmod-detach'
# expected: (bound hidden chain, authentication decoy, raw-IP download)
cases = {
    'positive': (seed, (True, True, False)),
    'no-auth': (seed.replace('echo "Authenticated"\n', ''), (True, False, False)),
    'different-launch': (seed.replace('nohup bash "$STAGE_DIR/worker.sh"',
                                     'nohup bash "$STAGE_DIR/local.sh"'), (False, False, False)),
    'different-chmod': (seed.replace('chmod +x "$STAGE_DIR/worker.sh"',
                                     'chmod +x "$STAGE_DIR/local.sh"'), (False, False, False)),
    'different-parent': (seed.replace('-o "$STAGE_DIR/', '-o "$OTHER_DIR/'), (False, False, False)),
    'visible-parent': (seed.replace('$HOME/.cache', '$HOME/cache'), (False, False, False)),
    'visible-stdout': (seed.replace('> /dev/null', '> worker.log'), (False, False, False)),
    'visible-stderr': (seed.replace('2>&1', '2> worker.err'), (False, False, False)),
    'comments': ('#!/bin/bash\n' + '\n'.join('# ' + x for x in seed.splitlines()), (False, False, False)),
    'jwt-ip': (seed.replace('/worker"', '/worker?st=eyJpcCI6IjIxMy41NS4xODQuMzcifQ"'), (True, True, False)),
    'raw-ip': (seed.replace('https://example.invalid', 'http://8.3.4.5'), (True, True, True)),
}
with tempfile.TemporaryDirectory(prefix='hidden-auth-', dir=args.work_dir) as tmp:
    for name, (source, _) in cases.items():
        (Path(tmp) / (name + '.sh')).write_text(source)
    result = subprocess.run([args.cleave, '--format', 'json', tmp], text=True,
                            capture_output=True, check=True)
    # Directory analysis may stream adjacent JSON report objects.
    remaining = result.stdout.strip()
    reports = {}
    while remaining:
        report, end = json.JSONDecoder().raw_decode(remaining)
        reports.update((Path(f['path']).stem, f) for f in report['files'])
        remaining = remaining[end:].lstrip()
    for name, (_, expected) in cases.items():
        traits = {t['id']: t['crit'] for t in reports[name].get('traits', [])}
        actual = tuple(t in traits for t in (payload, decoy, raw_ip))
        assert actual == expected, (name, expected, actual)
        if name != 'raw-ip':
            assert not any(c == 5 for c in traits.values()), (name, traits)
        for trait in (payload, decoy):
            if trait in traits:
                assert traits[trait] == 4, (name, trait, traits[trait])
        print(name + ': PASS')
print(str(len(cases)) + ' static controls passed')
