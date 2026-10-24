#!/usr/bin/env python3
"""Check staged-secret rules against source and near misses without execution."""
import argparse
import json
from pathlib import Path
import subprocess

p = argparse.ArgumentParser()
p.add_argument('--evidence', type=Path, required=True)
p.add_argument('--fixtures', type=Path, required=True)
p.add_argument('--report', type=Path, required=True)
p.add_argument('--cleave', default='cleave')
a = p.parse_args()
root = Path(__file__).resolve().parents[2]
write = 'micro-behaviors/fs/write/credential::shell-credential-labeled-variable-write'
encode = 'micro-behaviors/data/encode/base64::shell-base64-output-file'
dump = 'micro-behaviors/fs/write/credential::shell-multiple-credential-variable-writes'
upload = 'objectives/exfiltration/stealer/env::shell-credential-dump-encoded-file-upload'
new = {write, encode, dump, upload}
callback = 'micro-behaviors/communications/http/url/endpoint::webhook-site-uuid-path'
old_callback = 'objectives/supply-chain/recon-exfil/secrets::webhook-site-token'
source = (a.evidence / 'suspicious/oct10-cache.yml').read_text().split('        run: |\n', 1)[1]
source = '\n'.join(line[10:] for line in source.splitlines()) + '\n'
cases = {}


def case(name, text, required=(), forbidden=()):
    path = a.fixtures / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    cases[name] = (set(required), set(forbidden))


case('original-step.sh', source, new)
case('renamed-step.sh', source.replace('/tmp/c.env', '$RUNNER_TEMP/bundle')
     .replace('/tmp/c.b64', '$RUNNER_TEMP/packed').replace('${S', '${ALIAS')
     .replace('webhook.site/65a42464-3cfa-4b02-a18c-17a6d7b86f37', 'collector.invalid/submit'), new)
case('bsd-base64.sh', source.replace('base64 -w0', 'base64'), new)
case('printf.sh', source.replace('echo ', "printf '%s\\n' "), new)
workflow = (a.evidence / 'suspicious/oct10-cache.yml').read_text()
case('windows-bash.yml', workflow.replace('ubuntu-latest', 'windows-latest')
     .replace('        run: |', '        shell: bash\n        run: |'), new)
minimal_workflow = 'name: callback\non: [push]\njobs:\n  test:\n    runs-on: ubuntu-latest\n    steps:\n      - run: curl https://webhook.site/'
case('collector-path.yml', minimal_workflow + '65a42464-3cfa-4b02-a18c-17a6d7b86f37\n', {callback}, {old_callback, dump, upload})
case('short-collector-path.yml', minimal_workflow + 'abcdefghijkl\n', forbidden={callback, old_callback, dump, upload})
case('single-write.sh', '\n'.join([source.splitlines()[0]] + source.splitlines()[6:]) + '\n',
     {write, encode}, {dump, upload})
case('comments.sh', '\n'.join('# ' + line for line in source.splitlines()) + '\n', forbidden=new)
case('quoted.sh', "cat <<'DOCUMENTATION'\n" + source + 'DOCUMENTATION\n', forbidden=new)
literal = source
for i in range(1, 7):
    literal = literal.replace('${S' + str(i) + '}', 'redacted')
case('no-expansion.sh', literal, {encode}, {write, dump, upload})
case('stdout-only.sh', '\n'.join(line.split(' >')[0] if line.startswith('echo ') else line
                                 for line in source.splitlines()) + '\n', {encode}, {write, dump, upload})
case('null-output.sh', '\n'.join(line.split(' >')[0] + ' > /dev/null' if line.startswith('echo ')
                                 else line for line in source.splitlines()) + '\n',
     {encode}, {write, dump, upload})
case('decode.sh', source.replace('base64 -w0', 'base64 -d'), {write, dump}, {encode, upload})
case('no-upload.sh', '\n'.join(line for line in source.splitlines()
                               if not line.startswith('curl ')) + '\n', {write, encode, dump}, {upload})
case('auth-only.sh', source.replace('--data-binary @/tmp/c.b64', '--oauth2-bearer "$S1"'),
     {write, encode, dump}, {upload})

a.report.parent.mkdir(parents=True, exist_ok=True)
subprocess.run([a.cleave, '--traits-dir', str(root), 'analyze', '--format', 'json',
                '-o', str(a.report), str(a.fixtures)], check=True)
# Directory output may concatenate JSON documents without separators.
remaining = a.report.read_text()
decoder = json.JSONDecoder()
found = {}
while remaining.strip():
    report, end = decoder.raw_decode(remaining.lstrip())
    remaining = remaining.lstrip()[end:]
    for f in report.get('files', [report]):
        found.setdefault(Path(f['path']).name, set()).update(t['id'] for t in f.get('traits', []))
for name, (required, forbidden) in cases.items():
    actual = found.get(name, set())
    assert required <= actual, (name, 'missing', sorted(required - actual))
    assert not forbidden & actual, (name, 'unexpected', sorted(forbidden & actual))
print(f'{len(cases)} staged-credential controls passed')
