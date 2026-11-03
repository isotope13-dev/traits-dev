#!/usr/bin/env python3
"""Check migrated Android settings and sudo evidence and their boundaries."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = os.environ.get('CLEAVE', str(ROOT.parent / 'cleave/target/release/cleave'))
SETTINGS = 'micro-behaviors/os/application/desktop-settings::android-source-accessibility-settings-enable'
SUDO = 'micro-behaviors/os/privilege/elevation::sudo-stdin-password'
NONINTERACTIVE = 'micro-behaviors/os/privilege/elevation::sudo-no-prompt-command-text'
USER = 'micro-behaviors/process/create/command::sudo-user-command'
RUNAS = 'micro-behaviors/process/config/launch::runas-verb'
ARGV = 'micro-behaviors/process/config/launch::python-sudo-argv-list'
RUNAS_CALL = 'micro-behaviors/os/privilege/elevation::shellexecute-runas-call'
HIDDEN = 'micro-behaviors/process/argument/visibility::shellexecute-hidden-showcmd'
CASES = {
    'settings.java': 'class X { String a = "settings put secure enabled_accessibility_services x"; String b = "settings put secure accessibility_enabled 1"; }\n',
    'unrelated.java': 'class X { String a = "settings get secure accessibility_enabled"; }\n',
    'sudo.sh': '#!/bin/sh\nprintf "%s\\n" "$pw" | sudo -S id\n',
    'ordinary.sh': '#!/bin/sh\nsudo pacman -S package\n',
    'no-prompt.sh': '#!/bin/sh\nsudo -n id\n',
    'target-option.sh': '#!/bin/sh\nsudo lsof -n\n',
    'other-user.sh': '#!/bin/sh\nsudo -u builder makepkg\n',
    'runas.ps1': 'Start-Process powershell -Verb RunAs\n',
    'argv.py': 'args = ["sudo"]\n',
    'elevated.vbs': 'obj.ShellExecute("cmd.exe", "", "", "runas", 0)\n',
    'visible.vbs': 'obj.ShellExecute("cmd.exe", "", "", "open", 1)\n',
}
with tempfile.TemporaryDirectory(prefix='privilege-subject-') as directory:
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
    assert SETTINGS in found['settings.java'] and SETTINGS not in found['unrelated.java'], found
    assert SUDO in found['sudo.sh'] and SUDO not in found['ordinary.sh'], found
    assert NONINTERACTIVE in found['no-prompt.sh'] and NONINTERACTIVE not in found['target-option.sh'], found
    assert USER in found['other-user.sh'], found
    assert RUNAS in found['runas.ps1'] and ARGV in found['argv.py'], found
    # Scan output can omit redundant findings; inspect each rule directly.
    for name, expected in [('elevated.vbs', 'MATCHED'), ('visible.vbs', 'NOT MATCHED')]:
        trace = subprocess.run(
            [CLEAVE, '--traits-dir', str(ROOT), 'test-rules', '--rules',
             ','.join((RUNAS_CALL, HIDDEN)), str(Path(directory) / name)],
            text=True, capture_output=True, check=True,
        ).stdout
        for rule in (RUNAS_CALL, HIDDEN):
            assert f'{expected} {rule}' in trace, trace
print('Privilege subjects: Android settings and sudo stdin boundaries passed')
