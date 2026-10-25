#!/usr/bin/env python3
"""Parse controls and original scripts; never import or execute specimen code."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
SAMPLE_ROOT = Path('/usr/local/var/cyclotron/tmp.noindex/cyclotron-90084b2c/samples')
parser = argparse.ArgumentParser()
parser.add_argument('--samples', type=Path, default=SAMPLE_ROOT)
args = parser.parse_args()
paths = [args.samples / p for p in [
    '947a98165211/memos_trojan_init.py',
    'fc266418e962/chosen-brick-techniques.ps1',
    '0377259b2d46/telegram_polled_backdoor.py',
]]
expected = ['947a98165211c8da292338fa3300387ca6ee87b4b7a31cd36576b4a71cf9939b',
            'fc266418e9621d5d0739e8f100d58f94fbdb6995935239e5778b6ddcaffc5ee6',
            '0377259b2d46e8d3eb0c419c0ead4c1279653e3885f32a2fb8d9a2756825cdfd']
for p, digest in zip(paths, expected):
    assert hashlib.sha256(p.read_bytes()).hexdigest() == digest, p
memos, ps, bot = [p.read_text() for p in paths]
P = 'objectives/command-and-control/remote-command/'
signed = P + 'tasking::signed-c2-task-fetch-verify-execute'
loop = P + 'tasking::http-json-verified-command-task-loop'
files = 'objectives/credential-access/files/secret-sweep::python-developer-key-file-content-collection'
shell = P + 'shell::ptb-message-text-shell'
program = P + 'tasking::telegram-message-direct-program-launch'
document = P + 'tasking::telegram-document-write-launch-task'
run = 'micro-behaviors/os/registry/write::powershell-assigned-run-key-property'
persist = 'objectives/persistence/login/registry/run-key::run-key-persistence-ps'
namespace = 'micro-behaviors/os/env/enumeration::python-environ-items-namespace-prefix-filter'
verify = 'micro-behaviors/crypto/verify::public-key-verify-call'
mutex = 'micro-behaviors/process/sync/mutex::new-object-mutex'
ps_task = P + 'tasking::telegram-document-task-launch-loop'
cases = [(paths[0], [signed, loop, files], []),
         (paths[1], [persist, run, mutex, ps_task], []),
         (paths[2], [shell, program, document], [])]
fixtures = [
    ('renamed-implant.py', memos.replace('skyleen.fr', 'tasks.example.org').replace('sckit-', 'helper-'), [signed, files], []),
    ('unverified-command.py', memos.replace('subprocess.run(payload.decode()', 'subprocess.run(other.decode()'), [], [signed, loop]),
    ('different-key.py', memos.replace('verifier.verify(', 'unrelated.verify('), [], [signed, loop]),
    ('different-opened-path.py', memos.replace('with open(path,', 'with open(other,'), [], [signed, files]),
    ('task-controller-only.py', memos[memos.index('def _run_signed_tasks():'):memos.index('_launch_implant()  #')], [loop], [signed, files]),
    ('constant-shell.py', bot.replace('os.popen(message[2:])', 'os.popen("echo status")'), [], [shell, document]),
    ('unregistered-shell.py', bot.replace('~filters.COMMAND, analyze_command', '~filters.COMMAND, harmless'), [], [shell, document]),
    ('fixed-program.py', bot.replace('subprocess.Popen(message[9:])', 'subprocess.Popen("status.exe")'), [shell, document], [program]),
    ('different-launch-path.py', bot.replace('subprocess.Popen([destination])', 'subprocess.Popen([other])'), [shell], [document]),
    ('different-response.py', bot.replace('payload.write(content)', 'payload.write(b"local")').replace('payload.write(response.content)', 'payload.write(b"local")'), [shell], [document]),
    ('different-writer.py', bot.replace('payload.write(', 'unrelated.write('), [shell], [document]),
    ('download-only.py', bot.replace('subprocess.Popen([destination])', 'print(destination)'), [shell], [document]),
    ('reassigned-run-key.ps1', ps.replace('New-ItemProperty -Path $runKey', "$runKey = 'HKCU:\\Software\\Example'\nNew-ItemProperty -Path $runKey"), [], [run, persist]),
    ('immediate-run-key.ps1', "$r='HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Run'\nNew-ItemProperty -Path $r -Name Example -Value 'app.exe'\n", [run], [persist]),
    ('literal-namespace.py', 'import os\nx={k:v for k,v in os.environ.items() if k.startswith("EXAMPLE_")}\n', [namespace], []),
    ('literal-secret-prefix.py', 'import os\nx={k:v for k,v in os.environ.items() if k.startswith("SECRET_")}\n', [], [namespace]),
    ('tuple-secret-prefix.py', memos, [], [namespace]),
    ('notification-bot.py', 'import requests, os\nBOT_TOKEN="7834567890:AbCdEfGhIjKlMnOpQrStUvWxYz_0123456789"\nAPI=f"https://api.telegram.org/bot{BOT_TOKEN}"\nupdates=requests.get(f"{API}/getUpdates").json()\nprint(os.popen("echo health").read())\n', [], [shell, program, document]),
]
for p, yes, no in [
    ('testdata/taxonomy/registry-sample-triage/rsa.py', [verify], []),
    ('testdata/hostile/telegram-desktop-lockdown.py', ['objectives/command-and-control/channel/messaging::python-telegram-desktop-lockdown-rat'], []),
    ('testdata/benign/user-configured-telegram-bot-controls.py', [], [shell, program, document]),
    ('testdata/taxonomy/python-execution-templates/telegram.py', [], [shell, program, document]),
    ('testdata/triage/acquit-registry-loader-review/telegram-concealed-task.ps1', [ps_task], []),
    ('testdata/triage/acquit-registry-loader-review/telegram-visible-launch.ps1', [], [ps_task]),
    ('testdata/triage/acquit-registry-loader-review/telegram-different-launch-path.ps1', [], [ps_task]),
    ('testdata/triage/acquit-registry-loader-review/telegram-document-download-only.ps1', [], [ps_task]),
]:
    cases.append((ROOT / p, yes, no))
with tempfile.TemporaryDirectory(prefix='acquit-static-') as tmp:
    for name, source, yes, no in fixtures:
        path = Path(tmp) / name
        path.write_text(source)
        cases.append((path, yes, no))
    # Verify neutral relocation match preservation on source and the RSA fixture.
    for name, source, yes, no in [
        ('native-secret-names.c', 'char *names[]={"APP_PASSWORD","APP_SECRET_KEY","APP_API_KEY"};\n', [
            'micro-behaviors/os/security/auth/secret::native-password-like-identifier',
            'micro-behaviors/os/security/auth/secret::native-secret-like-identifier',
            'micro-behaviors/os/security/auth/secret::native-api-key-like-identifier',
            'micro-behaviors/os/security/auth/secret::native-credential-like-identifiers'], []),
        ('native-api-constants.c', 'char *names[]={"ERROR_WRONG_PASSWORD","SSL_SECRET_KEY","GL_API_KEY"};\n', [], [
            'micro-behaviors/os/security/auth/secret::native-password-like-identifier',
            'micro-behaviors/os/security/auth/secret::native-secret-like-identifier',
            'micro-behaviors/os/security/auth/secret::native-api-key-like-identifier']),
    ]:
        path = Path(tmp) / name
        path.write_text(source)
        cases.append((path, yes, no))
    result = subprocess.run(['cleave', '--traits-dir', str(ROOT), '--format', 'jsonl', *[str(x[0]) for x in cases]],
                            cwd=ROOT, capture_output=True, text=True, timeout=600, check=False)
    assert result.returncode == 0, result.stderr
    assert not result.stderr.strip(), result.stderr
    reports = {f['path']: f for line in result.stdout.splitlines() for f in json.loads(line)['files']}
    for path, yes, no in cases:
        ids = {t['id'] for t in reports[str(path)]['traits']}
        assert set(yes) <= ids and not set(no) & ids, (path.name, 'missing', set(yes)-ids, 'unexpected', set(no)&ids)
        print('PASS', path.name, flush=True)
print(f'{len(cases)} static regression controls passed')
