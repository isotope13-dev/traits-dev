#!/usr/bin/env python3
"""Compile inert managed fixtures and scan them; never load their assemblies."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def reports(text):
    decoder = json.JSONDecoder()
    while text.strip():
        text = text.lstrip()
        report, end = decoder.raw_decode(text)
        yield report
        text = text[end:]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cleave', default='cleave')
    parser.add_argument('--compiler', default='mcs')
    parser.add_argument('--sample')
    args = parser.parse_args()
    cases = json.loads((HERE / 'cases.json').read_text())['cases']
    with tempfile.TemporaryDirectory(prefix='clr-controls-') as tmp:
        outputs = Path(tmp) / 'assemblies'
        outputs.mkdir()
        for case in cases:
            command = [args.compiler, '-target:library', '-optimize+',
                       '-out:' + str(outputs / (case['name'] + '.dll'))]
            if case['defines']:
                command.append('-define:' + ','.join(case['defines']))
            subprocess.run(command + [str(HERE / 'Probe.cs')],
                           check=True, text=True, capture_output=True)
        command = [args.cleave, '--traits-dir', str(ROOT), '--no-update-check',
                   '--format', 'json', str(outputs)]
        if args.sample:
            command.append(args.sample)
        result = subprocess.run(command, check=True, text=True, capture_output=True,
                                env={**os.environ, 'CLEAVE_SKIP_CACHE': '1'})
        files = [file for report in reports(result.stdout) for file in report['files']]
        found = {Path(file['path']).name: {t['id']: t['crit'] for t in file.get('traits', [])}
                 for file in files}
        failures = []
        for case in cases:
            traits = found[case['name'] + '.dll']
            for rule, criticality in case.get('required', {}).items():
                if traits.get(rule) != criticality:
                    failures.append(f"{case['name']}: expected {rule}={criticality}, got {traits.get(rule)}")
            for rule in case.get('forbidden', []):
                if rule in traits:
                    failures.append(f"{case['name']}: unexpected {rule}={traits[rule]}")
        if args.sample:
            traits = found[Path(args.sample).name]
            required = {
                'objectives/command-and-control/backdoor/implant::managed-surveillance-plugin-agent': 5,
                'well-known/malware/rat/xeno-rat::xeno-rat-managed-client': 5,
                'objectives/persistence/login/scheduled-task/cli::managed-hidden-logon-task-xml': 4,
                'objectives/persistence/login/startup/registry::managed-run-key-mutation-members': 4,
                'micro-behaviors/crypto/symmetric/aes/library::dotnet-aes-transform-references': 3,
                'micro-behaviors/data/codec::rtl-compress-buffer-reference': 3,
            }
            for rule, criticality in required.items():
                if traits.get(rule) != criticality:
                    failures.append(f'sample: expected {rule}={criticality}, got {traits.get(rule)}')
        if failures:
            raise SystemExit('\n'.join(failures))
    print(f'PASS: {len(cases)} compiled managed controls' + (' and original sample' if args.sample else ''))


if __name__ == '__main__':
    main()
