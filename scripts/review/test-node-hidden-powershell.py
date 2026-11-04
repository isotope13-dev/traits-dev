#!/usr/bin/env python3
"""Bind hidden-window and policy-bypass switches to one PowerShell call."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--cleave', default='cleave')
args = parser.parse_args()
source = '''const cp = require('child_process');
cp.spawn('powershell.exe', [
  '-NoLogo', '-NoProfile', '-NonInteractive',
  '-ExecutionPolicy', 'Bypass',
  '-WindowStyle', 'Hidden', '-File', path
]);
'''
cases = {'launch.js': source,
         'reverse.js': "cp.execFile('powershell', ['-WindowStyle', 'Hidden', '-EP', 'Bypass']);\n",
         'direct.js': "spawn('powershell.exe', ['-EP', 'Bypass', '-WindowStyle', 'Hidden']);\n",
         'bundled.js': "(0,x.spawn)('powershell.exe',['-ExecutionPolicy','Bypass','-Command','-'],{windowsHide:!0});\n",
         'boolean.js': "cp.spawn('powershell.exe',['-EP','Bypass'],{windowsHide:true});\n",
         'other-program.js': source.replace('powershell.exe', 'notepad.exe'),
         'no-bypass.js': source.replace('Bypass', 'RemoteSigned'),
         'visible.js': "(0,x.spawn)('powershell.exe',['-EP','Bypass'],{windowsHide:!1});\n",
         'split.js': "cp.spawn('powershell.exe', ['-ExecutionPolicy', 'Bypass']);\n"
                     "cp.spawn('other.exe', ['-WindowStyle', 'Hidden']);\n"}
with tempfile.TemporaryDirectory(prefix='node-hidden-powershell-') as temp:
    root = Path(temp)
    for name, body in cases.items():
        (root / name).write_text(body)
    p = subprocess.run([args.cleave, '--traits-dir', str(repo), '--min-crit', 'component',
                        '--format=json', *(str(root / n) for n in cases)],
                       check=True, capture_output=True, text=True)
    found = {Path(f['path']).name: {t['id'] for t in f.get('traits', [])}
             for line in p.stdout.splitlines() if line for f in json.loads(line)['files']}
    trait = 'micro-behaviors/process/create/hidden::node-hidden-policy-bypass-powershell-launch'
    assert all(trait in found[n] for n in ('launch.js', 'reverse.js', 'direct.js', 'bundled.js', 'boolean.js'))
    assert all(trait not in found[n] for n in ('other-program.js', 'no-bypass.js', 'visible.js', 'split.js'))
    print('Hidden PowerShell Bypass findings bind both switches to one call.')
