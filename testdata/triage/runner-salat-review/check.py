"""Focused static controls. No fixture is executed."""
from pathlib import Path
import json, os, subprocess
ROOT = Path(__file__).resolve().parents[3]
BASE = Path(__file__).resolve().parent
r = subprocess.run([os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
                    '--format', 'json', str(BASE)],
                   env=dict(os.environ, CLEAVE_VALIDATE='0'),
                   text=True, capture_output=True)
if r.returncode not in (0, 1):
    raise RuntimeError(r.stderr)
files, s, dec = [], r.stdout, json.JSONDecoder()
while s.strip():
    report, n = dec.raw_decode(s.lstrip())
    files.extend(report['files'])
    s = s.lstrip()[n:]
by_name = {Path(f['path']).name: f for f in files}
def ids(name):
    return {t['id'] for t in by_name[name].get('traits', [])}
def hostile(name):
    return {t['id'] for t in by_name[name].get('traits', []) if t['crit'] == 5}
exfil = 'objectives/exfiltration/stealer/dev-secret::runner-secret-filter-issue-post'
release = 'micro-behaviors/communications/http/client/service::shell-curl-github-release-api-reference'
assert exfil in hostile('renamed-secret-pipeline.sh')
assert release in ids('release-metadata.sh')
assert release not in ids('gist-metadata.sh')
for name in ('bootstrap-python.sh', 'gist-metadata.sh', 'release-metadata.sh', 'comment-pipeline.sh', 'token-api.c', 'registry.go'):
    assert not hostile(name), (name, hostile(name))
assert 'micro-behaviors/os/privilege/token::open-process-token' in ids('token-api.c')
assert 'micro-behaviors/os/privilege/token::duplicate-token-ex' in ids('token-api.c')
assert 'micro-behaviors/os/registry/manipulate::go-registry-set-string-value-call' in ids('registry.go')
assert not any('sudo-python' in i for i in ids('comment-pipeline.sh'))
print('PASS: renamed member, bootstrap, comment, Gist, release controls')
