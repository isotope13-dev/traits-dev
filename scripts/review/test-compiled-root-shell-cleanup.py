#!/usr/bin/env python3
"""Check that cleanup binds the compiled source and privileged output."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[2]
trait = 'objectives/evasion/indicator-removal/cleanup::compiled-root-shell-source-removal'
source = '''#!/bin/sh
code=$(cat <<EOF
int main() { setuid(0); execl("/bin/sh", "sh", 0); }
EOF
)
build() {
  echo "$code" > ./.helper.c
  gcc -o ./.helper ./.helper.c
  chown root:root ./.helper
  chmod u+s ./.helper
  rm ./.helper.c
}
'''
cases = {
    'complete': (source, True),
    'other-source': (source.replace('rm ./.helper.c', 'rm ./.other.c'), False),
    'other-owner': (source.replace('chown root:root ./.helper', 'chown root:root ./.other'), False),
    'other-mode': (source.replace('chmod u+s ./.helper', 'chmod u+s ./.other'), False),
    'ordinary-build': (source.replace('setuid(0);', ''), False),
    'no-removal': (source.replace('rm ./.helper.c', ':'), False),
    'other-compiler': (source.replace('gcc ', 'clang '), True),
}
with tempfile.TemporaryDirectory(prefix='compiled-root-cleanup-') as tmp:
    paths = []
    for name, (content, _) in cases.items():
        path = Path(tmp) / (name + '.sh')
        path.write_text(content)
        paths.append(str(path))
    env = os.environ.copy()
    env['CLEAVE_SKIP_CACHE'] = '1'
    result = subprocess.run([str((repo / '../cleave/target/release/cleave').resolve()), '--traits-dir', str(repo), '--format=json', *paths], check=True, capture_output=True, text=True, env=env)
    reports = [json.loads(line)['files'][0] for line in result.stdout.split('\n') if line]
    assert len(reports) == len(cases)
    for report in reports:
        name = Path(report['path']).stem
        found = trait in {t['id'] for t in report.get('traits', [])}
        assert found == cases[name][1], (name, found, cases[name][1])
print('Compiled setuid shell source cleanup boundaries passed.')
