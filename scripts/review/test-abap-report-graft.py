#!/usr/bin/env python3
"""Check ABAP report-graft evidence and commented writer handling."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[2]
prefix = 'objectives/impact/infect/script/inject::abap-report-source-graft-'
source = '''REPORT demo.
SELECT NAME INTO target FROM TRDIR.
READ REPORT target INTO target_lines. READ REPORT SY-REPID INTO self_lines.
LOOP AT target_lines INTO row.
ENDLOOP.
INSERT LINES OF self_lines FROM 1 INTO target_lines INDEX pos.
*INSERT REPORT target FROM target_lines.
'''
cases = {
    'disabled': (source, 'disabled-writer'),
    'active': (source.replace('*INSERT REPORT', 'INSERT REPORT'), 'active-writer'),
    'other-names': (source.replace('target_lines', 'work').replace('self_lines', 'mine'), 'disabled-writer'),
    'no-directory': (source.replace('FROM TRDIR', 'FROM other_table'), None),
    'no-self-read': (source.replace('SY-REPID', 'other'), None),
    'one-read': (source.replace('READ REPORT target INTO target_lines. ', ''), None),
    'no-graft': (source.replace('INSERT LINES OF', 'APPEND LINES OF'), None),
    'no-writer': (source.replace('*INSERT REPORT target FROM target_lines.', ''), None),
}
with tempfile.TemporaryDirectory(prefix='abap-report-graft-') as tmp:
    paths = []
    for name, (content, _) in cases.items():
        path = Path(tmp) / (name + '.txt')
        path.write_text(content)
        paths.append(str(path))
    env = os.environ.copy()
    env['CLEAVE_SKIP_CACHE'] = '1'
    result = subprocess.run([str((repo / '../cleave/target/release/cleave').resolve()), '--traits-dir', str(repo), '--format=json', *paths], check=True, capture_output=True, text=True, env=env)
    reports = [json.loads(line)['files'][0] for line in result.stdout.split('\n') if line]
    assert len(reports) == len(cases)
    for report in reports:
        name = Path(report['path']).stem
        found = {t['id'].removeprefix(prefix) for t in report.get('traits', []) if t['id'].startswith(prefix)}
        expected = set() if cases[name][1] is None else {cases[name][1]}
        assert found == expected, (name, found, expected)
print('ABAP report graft boundaries passed.')
