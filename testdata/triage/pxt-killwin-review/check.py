"""Scan static controls and existing malicious fixtures; never execute samples."""
import json
import os
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
paths = sorted(HERE.glob('*.bat')) + sorted(HERE.glob('*.ps1'))
paths += [ROOT / 'testdata/ps-to-exe-byte-corruption' / name
          for name in ('corruptor.ps1', 'renamed.ps1', 'single-file-transform.ps1')]
paths += [ROOT / 'testdata/hostile/triage20-batch-system-wiper/c5c04a280ed961bd7f2c666e772f0e25ef203a8221092a5a52f6efe06c8e76bd/Trojan.Win32.KillWin.fr']
proc = subprocess.run([os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
                       '--format', 'json', *map(str, paths)],
                      capture_output=True, text=True, check=True)
decoder = json.JSONDecoder()
remaining = proc.stdout
files = {}
while remaining.strip():
    remaining = remaining.lstrip()
    report, end = decoder.raw_decode(remaining)
    remaining = remaining[end:]
    for file in report['files']:
        files[Path(file['path']).name] = file

def ids(name):
    return {trait['id'] for trait in files[name].get('traits', [])}

systemroot = 'micro-behaviors/fs/delete/target::batch-delete-target-systemroot'
bounds = 'micro-behaviors/data/control-flow/branch::powershell-short-prefix-length-bounds'
for name in ('systemroot-file.bat', 'systemroot-directory.bat'):
    assert systemroot in ids(name), name
assert systemroot not in ids('systemroot-reference.bat')
assert bounds in ids('prefix-bounds.ps1')
for name in ('prefix-single-bound.ps1', 'prefix-wide-bound.ps1'):
    assert bounds not in ids(name), name
prefix_attack = 'objectives/impact/destroy/user-data::powershell-recursive-file-prefix-corruption'
for name in ('corruptor.ps1', 'renamed.ps1'):
    assert prefix_attack in ids(name), name
assert prefix_attack not in ids('single-file-transform.ps1')
expected = {
    'objectives/impact/degrade/system/file::batch-system32-dll-glob-wipe',
    'objectives/impact/degrade/system/file::batch-device-manager-console-sabotage',
    'objectives/impact/degrade/system/recovery::batch-driver-restoration-archive-sabotage',
}
assert expected <= ids('Trojan.Win32.KillWin.fr')
for name in ('systemroot-directory.bat', 'systemroot-reference.bat', 'prefix-bounds.ps1',
             'prefix-single-bound.ps1', 'prefix-wide-bound.ps1', 'single-file-transform.ps1'):
    assert not [trait for trait in files[name].get('traits', []) if trait['crit'] >= 4], name
print('10 static placement and retained-attack controls passed.')
