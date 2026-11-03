#!/usr/bin/env python3
"""Check that the symlink target and protected directory are bound."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[2]
trait = 'objectives/execution/exploit/symlink::protected-symlink-target-privileged-test'
source = '''#!/bin/sh
$sudo chmod 700 $tmp || exit
$sudo -u $user ln -s $tmp/probe $log/notices >>$out
$sudo $program root 2>&1 | filter
if $sudo test -f $tmp/probe; then
  $sudo cat $tmp/probe
fi
'''
cases = {
    'complete': (source, True),
    'other-directory': (source.replace('chmod 700 $tmp', 'chmod 700 $other'), False),
    'other-target': (source.replace('test -f $tmp/probe', 'test -f $tmp/other'), False),
    'ordinary-directory': (source.replace('chmod 700', 'chmod 755'), False),
    'no-privileged-program': (source.replace('$sudo $program root', '$program root'), False),
    'no-symbolic-link': (source.replace('ln -s', 'ln -f'), False),
    'renamed-target': (source.replace('/probe', '/result'), True),
}
with tempfile.TemporaryDirectory(prefix='protected-symlink-') as tmp:
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
print('Protected symlink target pattern boundaries passed.')
