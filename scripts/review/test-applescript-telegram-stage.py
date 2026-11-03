#!/usr/bin/env python3
"""Check evidence requirements for the Telegram fallback stage."""
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
    'no-interpreter-pipe': source.replace('| osascript', '| cat'),
    'no-telegram': source.replace('t.me/', 'example.invalid/'),
    'no-curl': source.replace('curl', 'printf'),
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
            match = any(t['id'].endswith('::telegram-fallback-curl-osascript-stage') for t in f.get('traits', []))
            assert match == f['path'].endswith('/positive.applescript'), f['path']
print('Telegram fallback stage rejects three negative controls')
