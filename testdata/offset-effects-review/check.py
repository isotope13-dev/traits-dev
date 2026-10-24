#!/usr/bin/env python3
"""Check encoded window-hide values and self-path binding. Executes no sample."""
import json
import os
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
scratch = Path(sys.argv[1])
scratch.mkdir(parents=True, exist_ok=True)
source = (ROOT/'testdata/hostile/romulus-route-b-method.ps1').read_text()
key = int(re.search(r'\$key=(\d+)', source)[1])
program = ''.join(chr(int(n)+key) for n in re.search(r'\$codes=@\((.*?)\)', source, re.S)[1].split(','))
HIDE = 'objectives/evasion/process/hidden/window::offset-archive-window-hide'
SELF = 'objectives/evasion/self-delete/file/script::offset-archive-stored-selfpath-removal'
HIDE_SYNTAX = 'metadata/lang/encoding::negative-offset-showwindow-hide-zero'
SELF_SYNTAX = 'metadata/lang/encoding::negative-offset-stored-selfpath-removal'
CHAIN = 'objectives/execution/payload/file-exec::offset-passworded-archive-hidden-launch'


def wrap(code, offset=704123, env='__ST', invoke=True):
    return (f'$env:{env}=$MyInvocation.MyCommand.Path\n$key={offset}\n$codes=@(' +
            ','.join(str(ord(c)-offset) for c in code) + ')\n' +
            "$program='';for($index=0;$index -lt $codes.Length;$index++)" +
            '{$program+=[char]([int64]$codes[$index]+$key)}\n' +
            ('[scriptblock]::Create($program).Invoke()\n' if invoke else 'Write-Output $program\n'))

cases = []


def add(name, text, yes=(), no=()):
    path = scratch/name
    path.write_text(text)
    cases.append((path, set(yes), set(no)))


for offset in (2345, 17234, 234567, 9182734, 91827345, 918273456):
    add(f'rekey-{offset}.ps1', wrap(program, offset), (HIDE, SELF, CHAIN))
renamed = program.replace('$hwnd', '$windowHandle2').replace('__ST', 'StoredScript2')
add('renamed.ps1', wrap(renamed, env='StoredScript2'), (HIDE, SELF))
add('normal-window.ps1', wrap(program.replace('::ShowWindow($hwnd,0)', '::ShowWindow($hwnd,5)')),
    (SELF, CHAIN), (HIDE, HIDE_SYNTAX))
add('different-env.ps1', wrap(program.replace('Remove-Item -LiteralPath $env:__ST',
                                              'Remove-Item -LiteralPath $env:OTHER')),
    (HIDE, CHAIN), (SELF, SELF_SYNTAX))
add('prefix-env.ps1', wrap(program.replace('Remove-Item -LiteralPath $env:__ST',
                                           'Remove-Item -LiteralPath $env:__ST_EXTRA')),
    (HIDE, CHAIN), (SELF, SELF_SYNTAX))
add('no-deletion.ps1', wrap(program.replace('Remove-Item', 'Get-Item')), (HIDE, CHAIN), (SELF, SELF_SYNTAX))
add('no-self-assignment.ps1', wrap(program).replace('=$MyInvocation.MyCommand.Path', "='C:\\data.txt'"),
    (HIDE, CHAIN), (SELF, SELF_SYNTAX))
add('unevaluated.ps1', wrap(program, invoke=False), (HIDE_SYNTAX, SELF_SYNTAX), (HIDE, SELF, CHAIN))
add('benign-encoded-hide.ps1', wrap('[Demo]::ShowWindow($handle,0)\n'), (HIDE_SYNTAX,), (HIDE, SELF, CHAIN))
add('benign-encoded-self-cleanup.ps1', wrap('Remove-Item -LiteralPath $env:__ST -Force\n'),
    (SELF_SYNTAX,), (HIDE, SELF, CHAIN))
# Corrupt a high decimal digit: a suffix-only decimal matcher must not pass.
needle = ','.join(str(ord(c)-key) for c in '::ShowWindow($')
parts = needle.split(',')
parts[3] = str(int(parts[3])-1000)
add('corrupt-hide.ps1', wrap(program).replace(needle, ','.join(parts)), (SELF, CHAIN), (HIDE, HIDE_SYNTAX))

run = subprocess.run([os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT), '--format', 'json',
                      *[str(path) for path, _, _ in cases]], capture_output=True, text=True)
assert run.returncode == 0, run.stderr
reports = {}
remaining = run.stdout.lstrip()
while remaining:
    report, end = json.JSONDecoder().raw_decode(remaining)
    remaining = remaining[end:].lstrip()
    for file in report['files']:
        reports[Path(file['path']).name] = {t['id']: t['crit'] for t in file.get('traits', [])}
for path, yes, no in cases:
    traits = reports[path.name]
    assert yes <= traits.keys(), (path.name, 'missing', yes-traits.keys())
    assert not no & traits.keys(), (path.name, 'unexpected', no & traits.keys())
    for trait in (HIDE, SELF):
        if trait in yes:
            assert traits[trait] == 5, (path.name, trait, traits[trait])
print(f'PASS {len(cases)} encoded-effect controls')
