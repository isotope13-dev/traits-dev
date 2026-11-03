#!/usr/bin/env python3
"""Check service stop commands specifically in VM startup metadata."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[2]
prefix = 'micro-behaviors/os/service/stop::cloud-startup-'
def workflow(command, field='startup-script'):
    return {'Steps': {'run': {'CreateInstances': [{'metadata': {field: command}}]}}}

cases = {
    'service': (workflow('service sshguard stop; logger booted'), True),
    'systemctl': (workflow('sudo systemctl stop fail2ban'), True),
    'wrong-service': (workflow('service ssh stop'), False),
    'wrong-operation': (workflow('service sshguard start'), False),
    'wrong-field': (workflow('service sshguard stop', 'description'), False),
    'comment': (workflow('# service sshguard stop'), False),
}
with tempfile.TemporaryDirectory(prefix='cloud-login-guard-') as tmp:
    paths = []
    for name, (data, _) in cases.items():
        path = Path(tmp) / (name + '.json')
        path.write_text(json.dumps(data))
        paths.append(str(path))
    env = os.environ.copy()
    env['CLEAVE_SKIP_CACHE'] = '1'
    result = subprocess.run([str((repo / '../cleave/target/release/cleave').resolve()), '--traits-dir', str(repo), '--format=json', *paths], check=True, capture_output=True, text=True, env=env)
    reports = [json.loads(line)['files'][0] for line in result.stdout.split('\n') if line]
    assert len(reports) == len(cases)
    for report in reports:
        name = Path(report['path']).stem
        found = any(t['id'].startswith(prefix) for t in report.get('traits', []))
        assert found == cases[name][1], (name, found, cases[name][1])
print('Cloud startup login-guard service boundaries passed.')
