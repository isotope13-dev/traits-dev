#!/usr/bin/env python3
"""Check CMS contact/log EXEC distribution patterns and boundaries."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[2]
trait = 'objectives/lateral-movement/worm/file-copy::cms-contact-netlog-exec-distribution'
source = '''/* REXX */
say 'hello'
pull userid
"EXECIO * DISKR " userid " NAMES A (FIFO"
do while queued() > 0
  pull name node
  "SF SAMPLE EXEC A " name " AT " node " (ack"
end
"EXECIO * DISKR " userid " NETLOG A (FIFO"
do while queued() > 0
  pull name node
end
'''
cases = {
    'complete': (source, True),
    'alternate-name': (source.replace('SAMPLE EXEC', 'WORKER EXEC'), True),
    'no-address-book': (source.replace(' NAMES A', ' NOTES A'), False),
    'no-network-log': (source.replace(' NETLOG A', ' OTHER A'), False),
    'no-exec-transfer': (source.replace('SAMPLE EXEC', 'SAMPLE DATA'), False),
    'no-destination': (source.replace(' AT ', ' ON '), False),
    'cross-line': (source.replace(' AT ', '\nAT '), False),
    'no-queue-loop': (source.replace('do while queued() > 0', 'do 1'), False),
}
with tempfile.TemporaryDirectory(prefix='cms-exec-distribution-') as tmp:
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
        found = trait in {t['id'] for t in report.get('traits', [])}
        assert found == cases[name][1], (name, found, cases[name][1])
print('CMS EXEC distribution pattern boundaries passed.')
