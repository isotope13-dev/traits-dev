#!/usr/bin/env python3
"""Check root-shell and obfuscated shortcut detection boundaries."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile

repo = Path(__file__).resolve().parents[2]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--cleave', default='../cleave/target/release/cleave')
args = parser.parse_args()

shortcut = 'objectives/persistence/login/startup/shortcut::windows-shortcut-obfuscated-argument-inject'
root_shell = 'objectives/privilege-escalation/elevation-control/setuid/shell::compiled-root-shell-history-suppression'
ssh_log = 'objectives/credential-access/capture/input::ssh-client-plaintext-password-logging'
php_template = 'objectives/command-and-control/backdoor/webshell/embedded::phpsploit-header-eval-backdoor-template'
shell_source_id = 'micro-behaviors/process/interpreter/eval/source::shell-source-command'
shortcut_source = '''import os
for root, dirs, files in os.walk("."):
    s = shell.CreateShortcut(root)
    target = s.TargetPath
    s.Arguments = ''.join(map(getattr(__builtins__, 'chr'), [65]))
    a = ''.join(map(getattr(__builtins__, 'chr'), [66]))
    b = ''.join(map(getattr(__builtins__, 'chr'), [67]))
    s.Save()
'''
shell_source = '''#!/bin/sh
unset HISTFILE
cat > helper.c <<'SRC'
int main(void) { setuid(0); execl("/bin/sh", "sh", 0); }
SRC
gcc helper.c -o helper
chmod u+s helper
'''
ssh_source = '''void authenticate(void) {
  password = read_passphrase(prompt, 0);
  fprintf(log, "%s:%s", authctxt->server_user, password);
  packet_put_cstring(password);
}
'''
php_source = '''#!/bin/sh
cat > /tmp/config <<'END'
source /example
set BACKDOOR "@eval($_SERVER['HTTP_TOKEN'])"
exploit --get-backdoor
END
'''
samples = {
    'shortcut.py': (shortcut_source, {shortcut}),
    'no-shortcut.py': (shortcut_source.replace('CreateShortcut(', 'Open('), set()),
    'no-obfuscation.py': (shortcut_source.replace('join(map(getattr(__builtins__', 'join(map(getattr(other', 3), set()),
    'root.sh': (shell_source, {root_shell}),
    'fixed-command.sh': (shell_source.replace('"sh", 0', '"sh", "-c", "id", 0'), set()),
    'ssh-log.c': (ssh_source, {ssh_log}),
    'ssh-redacted.c': (ssh_source.replace('server_user, password', 'server_user, redacted'), set()),
    'php-template.sh': (php_source, {php_template}),
    'php-template-no-generator.sh': (php_source.replace('exploit --get-backdoor', 'help'), set()),
    'real-source.sh': ('#!/bin/sh\nsource /etc/profile\n', {shell_source_id}),
}
with tempfile.TemporaryDirectory(prefix='shell-bad-review-') as tmp:
    paths = []
    for name, (content, _) in samples.items():
        path = Path(tmp) / name
        path.write_text(content)
        paths.append(str(path))
    result = subprocess.run(
        [str((repo / args.cleave).resolve()), '--traits-dir', str(repo), '--format=json', *paths],
        check=True, capture_output=True, text=True,
    )
    reports = [json.loads(line)['files'][0] for line in result.stdout.splitlines() if line]
    for report in reports:
        name = Path(report['path']).name
        actual = {t['id'] for t in report.get('traits', [])} & {shortcut, root_shell, ssh_log, php_template, shell_source_id}
        expected = samples[name][1]
        assert actual == expected, (name, actual, expected)
    assert len(reports) == len(samples)
print('Shortcut modification and root-shell boundaries passed.')
