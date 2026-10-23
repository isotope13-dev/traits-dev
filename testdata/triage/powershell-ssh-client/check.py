"""Check parsed SSH commands without executing any PowerShell or SSH."""
import argparse
import json
import os
from pathlib import Path
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--scratch', type=Path, required=True)
args = parser.parse_args()
root = Path(__file__).resolve().parents[3]
directory = args.scratch / 'powershell-ssh-client-controls'
directory.mkdir(parents=True, exist_ok=True)
trait = 'micro-behaviors/communications/ssh/client::powershell-ssh-client-command'
cases = {
    'pipe.ps1': ('$configuration | & ssh operator@host.example', True),
    'direct.ps1': ('ssh host.example hostname', True),
    'exe.ps1': ('& ssh.exe host.example', True),
    'single-quote.ps1': ("& 'ssh.exe' host.example", True),
    'double-quote.ps1': ('& "ssh" host.example', True),
    'case.ps1': ('& SSH.EXE host.example', True),
    'comment.ps1': ('# & ssh operator@host.example', False),
    'string.ps1': ("$example = '& ssh operator@host.example'", False),
    'here-string.ps1': ("$example = @'\n& ssh host.example\n'@\n", False),
    'argument.ps1': ('Write-Output ssh host.example', False),
    'quoted-argument.ps1': ("Write-Output '& ssh host.example'", False),
    'other-tool.ps1': ('& ssh-keygen -t ed25519', False),
    'variable.ps1': ('$tool = "ssh"; & $tool host.example', False),
    'declaration.ps1': ('function ssh { Write-Output example }', False),
}
for name, (content, _) in cases.items():
    (directory / name).write_text(content + '\n')
env = os.environ.copy()
env.pop('CLEAVE_VALIDATE', None)
result = subprocess.run(
    [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(root),
     '--format', 'jsonl', *[str(directory / name) for name in cases]],
    check=True, text=True, capture_output=True, env=env,
)
reports = {}
for line in result.stdout.splitlines():
    for file in json.loads(line)['files']:
        reports[Path(file['path']).name] = file
for name, (_, expected) in cases.items():
    matches = [t for t in reports[name].get('traits', []) if t['id'] == trait]
    assert bool(matches) == expected, (name, matches)
    if expected:
        assert matches[0]['crit'] == 3, (name, matches)
(directory / 'reports.jsonl').write_text(result.stdout)
print(f'PASS: {len(cases)} SSH command, quoting, comment and non-command controls')
