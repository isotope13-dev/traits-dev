#!/usr/bin/env python3
"""Require independent LuaJIT CLI strings for the Mach-O runtime identity."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--cleave', default='cleave')
parser.add_argument('--clang', default='clang')
args = parser.parse_args()
markers = ['LuaJIT 2.1.0-beta3', 'luaJIT_BC_%s', 'Perform LuaJIT control command.']
with tempfile.TemporaryDirectory(prefix='macho-luajit-') as temp:
    root = Path(temp)
    binaries = []
    for name, values in [('complete', markers), ('no-help', markers[:2]),
                         ('no-bytecode', [markers[0], markers[2]])]:
        src = root / (name + '.c')
        src.write_text('\n'.join('__attribute__((used,section("__TEXT,__cstring,cstring_literals"))) '
                                  f'static const char s{i}[] = {json.dumps(value)};'
                                  for i, value in enumerate(values)))
        obj = root / (name + '.o')
        subprocess.run([args.clang, '-target', 'x86_64-apple-darwin', '-c', str(src), '-o', str(obj)],
                       check=True, capture_output=True)
        binaries.append(obj)
    p = subprocess.run([args.cleave, '--traits-dir', str(repo), '--min-crit', 'component',
                        '--format=json', *(str(x) for x in binaries)],
                       check=True, capture_output=True, text=True)
    found = {Path(f['path']).name: {t['id'] for t in f.get('traits', [])}
             for line in p.stdout.splitlines() if line for f in json.loads(line)['files']}
    identity = 'well-known/lib/runtime/scripted/luajit::macho-command-line-interpreter'
    assert identity in found['complete.o']
    assert identity not in found['no-help.o'] and identity not in found['no-bytecode.o']
    print('Mach-O LuaJIT CLI identity requires banner, bytecode marker and help.')
