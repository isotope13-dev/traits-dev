"""Static-only controls; no fixture or specimen is imported or executed."""
import json, os, subprocess
from pathlib import Path
root = Path(__file__).resolve().parent
repo = root.parent.parent
env = os.environ.copy()
for key in ['SCAN_HOPPER', 'SCAN_REGISTRY_MAP', 'SCAN_LLM', 'CLEAVE_VALIDATE']:
    env.pop(key, None)
env['CLEAVE_TRAITS_DIR'] = str(repo)
host = 'micro-behaviors/process/interpreter/powershell/host::python-created-powershell-script-invocation'
agent = 'objectives/command-and-control/remote-command/dispatch::python-agent-powershell-tasking'
clip = 'objectives/collection/clipboard/monitor::keylogger-clipboard-file-tracing'
daily = 'micro-behaviors/os/autorun/task-trigger::schtasks-daily-trigger-option'
idle = 'micro-behaviors/os/autorun/task-trigger::schtasks-idle-trigger-option'
task = 'objectives/persistence/system/scheduled-task::compressed-profile-recurring-task-registration'
history = 'objectives/collection/activity/browser::credential-harvester-history-export'
cases = {
    'history-format.ps1': (set(), {history}),
    'host.py': ({host}, {agent}),
    'host-async.py': ({host}, {agent}),
    'host-different.py': (set(), {host, agent}),
    'host-uninvoked.py': (set(), {host, agent}),
    'host-token.py': (set(), {host, agent}),
    'host-reassigned.py': (set(), {host, agent}),
    'ordinary-task.ps1': ({daily, idle}, {task}),
    'task-prefix.ps1': (set(), {daily, idle, task}),
    'clipboard-keylogger.exe': ({clip}, set()),
    'clipboard-manager.exe': (set(), {clip}),
    'keylogger-no-clipboard.exe': (set(), {clip}),
}
command = ['atomscan', '--no-update', '--analyze=local', '--follow=none', '--mode=slow', '-f', 'json']
r = subprocess.run(command + [str(root / p) for p in cases], env=env, capture_output=True, text=True)
reports = [json.loads(line) for line in r.stdout.splitlines() if line.strip()]
assert len(reports) == len(cases), (len(reports), r.stderr)
for report in reports:
    name = Path(report['raw']['files'][0]['path']).name
    ids = {t['id'] for f in report['raw']['files'] for t in f.get('traits', [])}
    present, absent = cases[name]
    assert present <= ids and not absent & ids, (name, present - ids, absent & ids)
    print('PASS', name)
