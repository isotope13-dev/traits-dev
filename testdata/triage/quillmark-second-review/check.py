#!/usr/bin/env python3
"""Static regression: harmless install hooks versus encoded secret export."""
import argparse
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[3]
DIRECT = 'micro-behaviors/process/interpreter/eval/direct::python-exec-base64-result'
DECODE = 'micro-behaviors/data/decode/base64::b64decode-call'
CONCEAL = 'objectives/anti-static/obfuscation/control-flow/logic::b64decode-exec'
HOOK = 'metadata/build/package/recipe/setup-hooks::cmdclass-install-phase-override'
RELEASE = 'metadata/build/package/recipe/setup-hooks::placeholder-first-release-packaging-hook'
ENV = 'objectives/exfiltration/stealer/env::python-env-harvest'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cleave', default='cleave')
    args = parser.parse_args()
    paths = [Path(__file__).with_name('pypi-quillmark-encoded-install-hook-linux.tar.gz'),
             Path(__file__).with_name('ordinary-hook.py'),
             Path(__file__).with_name('encoded-exfil-hook.py'),
             ROOT / 'testdata/hostile/py-b64-exec-dropper.py']
    result = subprocess.run([args.cleave, '--no-update-check', '--traits-dir', str(ROOT),
                             '--disable', 'radare2,upx', '--format', 'json',
                             *map(str, paths)], check=True, capture_output=True, text=True)
    decoder = json.JSONDecoder()
    remaining = result.stdout
    reports = {}
    while remaining.strip():
        report, end = decoder.raw_decode(remaining.lstrip())
        remaining = remaining.lstrip()[end:]
        reports.update({f['path']: f for f in report['files']})
    for path in paths:
        report = reports[str(path)]
        traits = {t['id']: t for t in report.get('traits', [])}
        if path.name.startswith('pypi-quillmark'):
            assert {DIRECT, DECODE, CONCEAL, HOOK, RELEASE} <= traits.keys()
            assert not any(t['crit'] >= 5 for t in traits.values())
            assert {t['id'] for t in traits.values() if t['crit'] == 4} == {CONCEAL}
            assert not any(t.startswith('objectives/supply-chain/') for t in traits)
        elif path.name == 'ordinary-hook.py':
            assert HOOK in traits
            assert not any(t['crit'] >= 4 for t in traits.values())
        elif path.name == 'encoded-exfil-hook.py':
            assert {DIRECT, DECODE, CONCEAL, HOOK, ENV} <= traits.keys()
            assert traits[ENV]['crit'] == 5
        else:
            assert {DIRECT, DECODE, CONCEAL,
                    'objectives/anti-static/obfuscation/payload/loader::python-urllib-exec-with-concealed-code',
                    'objectives/anti-static/obfuscation/payload/encoded/exec::decoded-shell-command'} <= traits.keys()
        print('PASS', path.name)


if __name__ == '__main__':
    main()
