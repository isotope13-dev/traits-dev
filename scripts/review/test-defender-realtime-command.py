#!/usr/bin/env python3
"""Check direct Defender real-time disable command observations."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[2]
trait = 'micro-behaviors/os/security/defender::powershell-realtime-disable-command'
cases = {
    'disable': ('Set-MpPreference -DisableRealtimeMonitoring $true\n', True),
    'option': ('Set-MpPreference -Force -DisableRealtimeMonitoring $true\n', True),
    'reenable': ('Set-MpPreference -DisableRealtimeMonitoring $false\n', False),
    'comment': ('# Set-MpPreference -DisableRealtimeMonitoring $true\n', False),
    'other-setting': ('Set-MpPreference -DisableBehaviorMonitoring $true\n', False),
}
with tempfile.TemporaryDirectory(prefix='defender-command-') as tmp:
    paths = []
    for name, (content, _) in cases.items():
        path = Path(tmp) / (name + '.ps1')
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
print('Defender real-time command boundaries passed.')
