#!/usr/bin/env python3
"""Check package and source evidence for an install-time remote eval."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from zipfile import ZipFile, ZIP_DEFLATED
root = Path(__file__).resolve().parents[2]
cleave = os.environ.get('CLEAVE', str(root.parent / 'cleave/target/release/cleave'))
package = Path(sys.argv[1])
manifest = (package / 'package.json').read_text()
entry = (package / 'src/index.js').read_text()
helper = (package / 'src/utils.js').read_text()
cases = {
    'positive': (manifest, entry, helper),
    'no-install-hook': (manifest.replace('"postinstall"', '"otherhook"'), entry, helper),
    'no-paste-origin': (manifest.replace('pastebin.com', 'example.org'), entry, helper),
    'no-https': (manifest, entry.replace('https.get', 'https.noop'), helper),
    'no-buffering': (manifest, entry.replace('str += src', 'str = src'), helper),
    'no-eval': (manifest, entry.replace('eval(str)', 'String(str)'), helper),
    'no-decoding': (manifest, entry, helper.replace("'base64'", "'utf-8'")),
}
with tempfile.TemporaryDirectory() as directory:
    paths = []
    for name, files in cases.items():
        assert name == 'positive' or files != cases['positive'], name
        path = Path(directory) / (name + '.zip')
        with ZipFile(path, 'w', ZIP_DEFLATED) as z:
            for filename, data in zip(('package.json', 'src/index.js', 'src/utils.js'), files):
                z.writestr(filename, data)
        paths.append(str(path))
    result = subprocess.run([cleave, '--traits-dir', str(root), '--json', *paths],
                            capture_output=True, text=True, check=True,
                            env={**os.environ, 'CLEAVE_SKIP_CACHE': '1', 'RAYON_NUM_THREADS': '2'})
    rows = [json.loads(line) for line in result.stdout.split('\n') if line]
    assert len(rows) == len(paths)
    for row in rows:
        f = row['files'][0]
        match = any(t['id'].endswith('::npm-install-pastebin-response-eval-clues') for t in f.get('traits', []))
        assert match == f['path'].endswith('/positive.zip'), f['path']
print('npm install remote-eval rule rejects six missing-evidence controls')
