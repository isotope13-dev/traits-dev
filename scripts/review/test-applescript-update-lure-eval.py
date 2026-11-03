#!/usr/bin/env python3
"""Check the meeting-update lure and remote script facts independently."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
root = Path(__file__).resolve().parents[2]
cleave = os.environ.get('CLEAVE', str(root.parent / 'cleave/target/release/cleave'))
source = Path(sys.argv[1]).read_text()
cases = {
    'positive': source,
    'no-fetch': source.replace('do shell script "curl ', 'do shell script "printf '),
    'no-evaluation': source.replace('run script cont', 'return cont'),
    'no-update-lure': source.replace('softwareupdate', 'softwareupdatx'),
}
with tempfile.TemporaryDirectory() as directory:
    paths = []
    for name, data in cases.items():
        assert name == 'positive' or data != source, name
        path = Path(directory) / (name + '.applescript')
        path.write_text(data)
        paths.append(str(path))
    result = subprocess.run([cleave, '--traits-dir', str(root), '--json', *paths],
                            capture_output=True, text=True, check=True,
                            env={**os.environ, 'CLEAVE_SKIP_CACHE': '1'})
    for line in result.stdout.split('\n'):
        if line:
            f = json.loads(line)['files'][0]
            match = any(t['id'].endswith('::meeting-update-curl-output-script-eval-clues') for t in f.get('traits', []))
            assert match == f['path'].endswith('/positive.applescript'), f['path']
print('Meeting lure and evaluation rule rejects three controls')
