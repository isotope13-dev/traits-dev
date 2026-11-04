#!/usr/bin/env python3
"""Check VS Code active-filename shell construction with linked variables."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--cleave', default='cleave')
args = parser.parse_args()
source = '''function activate() {
  var filename = vscode.window.activeTextEditor.document.fileName;
  var exec = require('child_process').exec;
  exec('autopep8 ' + filename, callback);
}
'''
cases = {'unsafe.js': source,
         'other-argument.js': source.replace("'autopep8 ' + filename", "'autopep8 ' + other"),
         'argument-array.js': source.replace("require('child_process').exec", "require('child_process').execFile")
                                    .replace("'autopep8 ' + filename", "'autopep8', [filename]"),
         'escaped.js': source.replace("'autopep8 ' + filename", "'autopep8 ' + shellEscape(filename)"),
         'other-source.js': source.replace('vscode.window.activeTextEditor.document.fileName', 'settings.name')}
with tempfile.TemporaryDirectory(prefix='vscode-filename-shell-') as temp:
    root = Path(temp)
    for name, body in cases.items():
        (root / name).write_text(body)
    p = subprocess.run([args.cleave, '--traits-dir', str(repo), '--min-crit', 'component',
                        '--format=json', *(str(root / n) for n in cases)],
                       check=True, capture_output=True, text=True)
    found = {Path(f['path']).name: {t['id'] for t in f.get('traits', [])}
             for line in p.stdout.splitlines() if line for f in json.loads(line)['files']}
    trait = 'micro-behaviors/process/create/shell/variable-command::vscode-active-filename-concatenated-to-exec'
    assert trait in found['unsafe.js']
    assert all(trait not in found[n] for n in cases if n != 'unsafe.js')
    print('VS Code filename shell finding requires the linked unescaped command.')
