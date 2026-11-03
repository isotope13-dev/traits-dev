#!/usr/bin/env python3
"""Check process-creation and event subjects after the WMI migration."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = os.environ.get('CLEAVE', str(ROOT.parent / 'cleave/target/release/cleave'))
CREATE = 'micro-behaviors/process/create/wmi::wmi-process-create-call'
EVENT = 'micro-behaviors/os/wmi/event::wmi-notification-query-call'
STOP = 'micro-behaviors/os/service/stop::stop-service-wmi'
TERMINATE = 'micro-behaviors/process/terminate/kill::terminate-process-wmi'
CASES = {
    'create.vbs': 'Set obj = svc.Get("Win32_Process").Create("calc.exe")\n',
    'other.vbs': 'Set obj = svc.Get("Win32_Service").Create("calc.exe")\n',
    'event.js': 'var e = service.ExecNotificationQuery("SELECT * FROM X");\n',
    'query.js': 'var e = service.ExecQuery("SELECT * FROM X");\n',
    'stop.ps1': '$s = Get-WmiObject Win32_Service\n$s.StopService()\n',
    'terminate.ps1': '$p = Get-WmiObject Win32_Process\n$p.Terminate()\n',
    'query.ps1': '$p = Get-WmiObject Win32_Process\n$p.Name\n',
}
with tempfile.TemporaryDirectory(prefix='wmi-subjects-') as directory:
    paths = []
    for name, content in CASES.items():
        path = Path(directory) / name
        path.write_text(content)
        paths.append(str(path))
    result = subprocess.run([CLEAVE, '--traits-dir', str(ROOT), '--format', 'jsonl', 'analyze', *paths], text=True, capture_output=True, check=True)
    found = {}
    for line in result.stdout.splitlines():
        for item in json.loads(line).get('files', []):
            found[Path(item['path']).name] = {trait['id'] for trait in item.get('traits', [])}
    assert CREATE in found['create.vbs'] and CREATE not in found['other.vbs'], found
    assert EVENT in found['event.js'] and EVENT not in found['query.js'], found
    assert STOP in found['stop.ps1'], found
    assert TERMINATE in found['terminate.ps1'] and TERMINATE not in found['query.ps1'], found
print('WMI subjects: process creation and notification boundaries passed')
