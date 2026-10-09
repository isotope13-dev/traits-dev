#!/usr/bin/env python3
"""Stage originals and semantic near misses away from test-path suppressors."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument('--samples-root', type=Path, required=True)
parser.add_argument('--scratch-root', type=Path, required=True)
args = parser.parse_args()
root = Path(__file__).resolve().parents[3]
dos = (args.samples_root / '95f4270f7cea/pad43_128.com').read_bytes()
ps = (args.samples_root / '83de8a7eb152/ps-cradle-stager.ps1').read_text()
second = (args.samples_root / '1bf9493e2246/ps-cradle-stager.ps1').read_text()
fixtures = {
    'companion.com': dos,
    'shared-dispatch.com': (root / 'testdata/hostile/dos-com/dikshev-44-companion-overwriter.com').read_bytes(),
    'variant.com': dos[:9] + b'\x89\xf2' + dos[11:] + bytes(257),
    'data-buffer.com': dos[:7] + b'\x53' + dos[8:],
    'text-twin.com': dos[:4] + b'TXT' + dos[7:],
    'stager.ps1': ps.encode(),
    'process-policy.ps1': second.encode(),
    'archive-child.ps1': '\n'.join(ps.splitlines()[:-1]).encode(),
    'stage-only.ps1': '\n'.join(ps.splitlines()[:4]).encode(),
    'defender-only.ps1': ps.splitlines()[-1].encode(),
    'quoted-eval.ps1': ("Write-Output '" + ps.splitlines()[4] + "'\n" + ps.splitlines()[-1]).encode(),
}
expected = {
    'companion.com': (3, 0), 'variant.com': (3, 0), 'shared-dispatch.com': (3, 0),
    'stager.ps1': (0, 2), 'process-policy.ps1': (0, 3),
}
with tempfile.TemporaryDirectory(prefix='companion-cradle-', dir=args.scratch_root) as stage:
    for name, data in fixtures.items():
        (Path(stage) / name).write_bytes(data)
    result = subprocess.run(['cleave', '--traits-dir', str(root), '--format', 'json', stage],
                            text=True, capture_output=True, check=True)
    decoder = json.JSONDecoder()
    remaining = result.stdout
    reports = {}
    while remaining.strip():
        report, end = decoder.raw_decode(remaining.lstrip())
        remaining = remaining.lstrip()[end:]
        for file in report['files']:
            reports[Path(file['path']).name] = file
    assert set(reports) == set(fixtures), set(reports)
    for name, file in reports.items():
        traits = file.get('traits', [])
        actual = (sum(t['crit'] == 5 for t in traits), sum(t['crit'] == 4 for t in traits))
        assert actual == expected.get(name, (0, 0)), (name, actual, traits)
        ids = {t['id'] for t in traits}
        assert not any('embedded-powershell-irm-iex' in id or 'ps-fileless-download-eval' in id for id in ids)
        if name == 'process-policy.ps1':
            assert 'micro-behaviors/process/create/flags::execution-policy-bypass-abbrev-flag' not in ids
        print(name, 'hostile/suspicious=', actual)
print('All 11 focused controls passed')
