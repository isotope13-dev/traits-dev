"""Static scans only: never execute the fixture commands or connect functions."""
import json
import os
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
MB = 'micro-behaviors/'
REC = 'objectives/impact/degrade/system/recovery::'
CASES = {
    'ordinary-query.py': {MB+'communications/grpc::query-result-upload-method'},
    'source-observations.py': {
        'metadata/lang/source/declaration::python-overwrite-file-function',
        'metadata/lang/source/syntax/call/arguments::python-host-variable-create-connection',
        'metadata/package/documentation/security-advisory::cve-reference',
    },
    'tls-client.py': {
        MB+'communications/tls/initialize::python-ssl-context-wrap-socket',
        MB+'communications/tls/initialize::python-wrap-socket-server-hostname',
    },
    'tls-client.js': {MB+'communications/socket/connect::node-tls-connect'},
    'recovery-on.bat': {'metadata/lang/source/syntax/command::windows-wmic-command'},
    'recovery-off.bat': {
        REC+'comprehensive-recovery-inhibition', REC+'wmic-shadowcopy',
        REC+'bcdedit-recovery', REC+'bcdedit-ignore-failures',
    },
    'nul-only.py': {MB+'data/string/assembly::append-nul-prefixed-string'},
}
command = [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT), '--json']
result = subprocess.run(command + [str(HERE/name) for name in CASES],
                        capture_output=True, text=True, check=True)
seen = set()
for line in result.stdout.splitlines():
    for report in json.loads(line).get('files', []):
        name = Path(report['path']).name
        if name not in CASES:
            continue
        seen.add(name)
        traits = {t['id'] for t in report.get('traits', [])}
        assert CASES[name] <= traits, (name, CASES[name] - traits)
        if name != 'recovery-off.bat':
            assert not [t for t in report.get('traits', []) if t['crit'] >= 4], name
        if name == 'source-observations.py':
            assert not any(t.startswith(MB+'communications/socket/connect::') for t in traits)
assert seen == set(CASES), seen
print('Passed seven static positive and near-miss controls')
