#!/usr/bin/env python3
"""Check the parent PID is an argument to the inode lookup helper."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[2]
trait = 'micro-behaviors/fs/file/stat::parent-process-inode-helper-call'
cases = {
    'parent': ('void f(){auto n = utils::get_inode_of_process(getppid());}', True),
    'self': ('void f(){auto n = utils::get_inode_of_process(getpid());}', False),
    'unrelated': ('void f(){auto p = getppid(); auto n = utils::get_inode_of_process(pid);}', False),
    'other-helper': ('void f(){auto n = utils::get_process_info(getppid());}', False),
    'comment': ('void f(){/* utils::get_inode_of_process(getppid()); */}', False),
}
with tempfile.TemporaryDirectory(prefix='parent-inode-') as tmp:
    paths = []
    for name, (content, _) in cases.items():
        path = Path(tmp) / (name + '.cpp')
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
print('Parent process inode helper boundaries passed.')
