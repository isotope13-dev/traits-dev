#!/usr/bin/env python3
"""Static controls for offset syntax and curl POST defaults. Executes no sample."""
import json
import os
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
source, scratch = map(Path, sys.argv[1:])
scratch.mkdir(parents=True, exist_ok=True)
s = source.read_text()
key = int(re.search(r'\$key=(\d+)', s)[1])
a = list(map(int, re.search(r'\$codes=@\((.*?)\)', s, re.S)[1].split(',')))
decoded = ''.join(chr(n+key) for n in a)
HOSTILE = 'objectives/execution/payload/file-exec::offset-passworded-archive-hidden-launch'
CONSOLE = 'objectives/evasion/process/hidden/console::offset-archive-console-control'
CLEANUP = 'objectives/evasion/indicator-removal/cleanup::offset-archive-environment-path-cleanup'
POST = 'micro-behaviors/communications/http/post::http-curl-post-request'
PREFIX = 'metadata/lang/encoding::negative-offset-'
tokens = json.loads((Path(__file__).parent/'tokens.json').read_text())
cases = []

def wrap(program, offset=704123, evaluate=True):
    return ("$env:__ST=$MyInvocation.MyCommand.Path\n"
            f"$key={offset}\n$codes=@("+','.join(str(ord(c)-offset) for c in program)+")\n"
            "$program='';for($index=0;$index -lt $codes.Length;$index++)"
            "{$program+=[char]([int64]$codes[$index]+$key)}\n"+
            ("[scriptblock]::Create($program).Invoke()\n" if evaluate else "Write-Output $program\n"))

def add(name, text, yes=(), no=()):
    path = scratch/name
    path.write_text(text)
    cases.append((path, set(yes), set(no)))

high = (HOSTILE, CONSOLE, CLEANUP)
for k in (17234, 234567, 9182734):
    add(f'rekey-{k}.ps1', wrap(decoded, k), high)
add('renamed-variables.ps1', wrap(decoded.replace('$dir', '$stageRoot').replace('$tool', '$extractor').replace('$password', '$secret')),
    high)
add('unused-source.ps1', wrap(decoded, evaluate=False), no=high)
add('hello.ps1', wrap("Write-Output 'Hello world'"), no=high)
add('visible.ps1', wrap(decoded.replace('-WindowStyle Hidden', '-WindowStyle Normal')), no=high)
add('no-executable-selection.ps1', wrap(decoded.replace("-Filter '*.exe'", "-Filter '*.log'")), no=high)
add('no-password-argument.ps1', wrap(decoded.replace("('-p'+$", "('-a'+$")), no=high)
add('no-console-api.ps1', wrap(decoded.replace('::ShowWindow($', '::TestWindow($')), (HOSTILE,CLEANUP), (CONSOLE,))
add('no-removal.ps1', wrap(decoded.replace('Remove-Item -LiteralPath $env:', 'Get-Item -LiteralPath $env:')), (HOSTILE,CONSOLE), (CLEANUP,))
add('no-extract-operation.ps1', wrap(decoded.replace("-ArgumentList @('x',", "-ArgumentList @('l',")), no=high)
# A near miss differs only in the high digits of one encoded magnitude.
# Final-digit-only comparisons would falsely retain the HTTPS token.
wrong = wrap(decoded)
encoded_token = ','.join(str(ord(c)-key) for c in tokens['https-downloadfile-call'])
parts = encoded_token.split(','); parts[3] = str(int(parts[3])-1000)
add('corrupt-high-digits.ps1', wrong.replace(encoded_token, ','.join(parts)), no=(HOSTILE,PREFIX+'https-downloadfile-call'))
# Formerly default curl POST was missed, even though the form was transmitted.
add('default-post.sh', "#!/bin/sh\ncurl --data-urlencode 'name=value' https://example.org/form\n", (POST,))
for opt in ('-G','--get','-I','-X GET','--request PUT','-X CUSTOM'):
    add('curl-'+opt.replace(' ','-').replace('--','')+'.sh',
        f"#!/bin/sh\ncurl {opt} --data-urlencode 'name=value' https://example.org/form\n", no=(POST,))
add('explicit-post.sh', "#!/bin/sh\ncurl -X POST --data 'name=value' https://example.org/form\n", (POST,))
run = subprocess.run([os.environ.get('CLEAVE','cleave'), '--traits-dir',str(ROOT),'--format','json',
                      *[str(p) for p,_,_ in cases]], capture_output=True, text=True)
assert run.returncode == 0, run.stderr
reports={}
remaining=run.stdout.lstrip()
while remaining:
    report,end=json.JSONDecoder().raw_decode(remaining)
    remaining=remaining[end:].lstrip()
    for f in report['files']:
        reports[Path(f['path']).name]={t['id']:t['crit'] for t in f.get('traits',[])}
for p,yes,no in cases:
    traits=reports[p.name]
    assert yes <= traits.keys(), (p.name,'missing',yes-traits.keys())
    assert not no & traits.keys(), (p.name,'unexpected',no&traits.keys())
    if HOSTILE in yes: assert traits[HOSTILE]==5, (p.name,traits[HOSTILE])
print(f'PASS {len(cases)} offset/curl controls')
