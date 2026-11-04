#!/usr/bin/env python3
"""Distinguish a ShellExecute member reference from invocation text."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--cleave', default='../cleave/target/release/cleave')
args = parser.parse_args()
with tempfile.TemporaryDirectory(prefix='shell-handler-taxonomy-') as tmp:
    root = Path(tmp)
    cases = {
        'member.js': 'var f = application.ShellExecute;\n',
        'call.js': 'application.ShellExecute("example.txt");\n',
        'call.vbs': 'Set app = CreateObject("Shell.Application")\napp.ShellExecute "example.txt"\n',
    }
    for name, text in cases.items():
        (root / name).write_text(text)
    result = subprocess.run(
        [str((repo / args.cleave).resolve()), '--traits-dir', str(repo), '--format=json',
         *(str(root / name) for name in cases)], check=True, capture_output=True, text=True,
    )
    reports = [json.loads(line)['files'][0] for line in result.stdout.splitlines() if line]
    ids = {Path(r['path']).name: {t['id'] for t in r.get('traits', [])} for r in reports}
    assert set(ids) == set(cases), ids.keys()
    ref = 'micro-behaviors/os/handler/open::shellexecute-method-reference'
    call = 'metadata/lang/source/syntax/call/member::shellexecute-method-invocation-text'
    assert ref in ids['member.js'] and call not in ids['member.js']
    assert ref in ids['call.js'] and call in ids['call.js']
    assert ref in ids['call.vbs'] and call in ids['call.vbs']
    print('ShellExecute member references and invocation text are distinguished.')
