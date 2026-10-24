"""Static regression controls; specimens are parsed, never executed.
Usage: python3 check.py SAMPLE_ROOT SCRATCH
"""
from pathlib import Path
import json, os, subprocess, sys
import dnfile

ROOT = Path(__file__).resolve().parents[3]
SAMPLES, OUT = map(Path, sys.argv[1:3])
OUT.mkdir(parents=True, exist_ok=True)
PE = SAMPLES / '7b3aa2c3251b/1-7dfaef.pe'
PS = SAMPLES / '09674b1689d8/register_remote_appx_oauth.ps1'
TGZ = SAMPLES / '2b144e342f2a/ltidisafe-1.7.1.tgz'
SHELL = 'objectives/command-and-control/remote-command/shell::managed-infection-task-command-output'
FILES = 'objectives/exfiltration/stealer/file::managed-infection-document-disk-upload'
REPORT = 'objectives/exfiltration/stealer/system-info/identity::managed-infection-domain-report-upload'
OAUTH = 'objectives/exfiltration/stealer/token::winrt-first-party-oob-response-forwarding'
APPX = 'objectives/exfiltration/stealer/token::sideloaded-appx-oauth-response-forwarding'
NAME = 'micro-behaviors/data/serialize/schema-object::machinename-label'
OLDNAME = 'objectives/discovery/system/fingerprint/info::machinename-label'
GROUP = 'metadata/permission/host::utility-extension-broad-control'
NEW_NAMES = 'metadata/package/name/vocabulary::'

cases = [(PE, {SHELL: True, FILES: True, REPORT: True, NAME: True, OLDNAME: False}),
         (PS, {OAUTH: True, APPX: True}), (TGZ, {})]
raw = PE.read_bytes()
def add(name, content, checks):
    p = OUT / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(content if isinstance(content, bytes) else content.encode())
    cases.append((p, checks))

def erase(token, data=raw):
    assert token in data, token
    return data.replace(token, b'Z' * len(token))

# Semantic roles must remain separate. Generic shell, file and host APIs alone
# are insufficient; a task getter or upload sink removed breaks its outcome.
add('no-infection-field.exe', erase('INFECTIONTYPE'.encode('utf-16le')),
    {SHELL: False, FILES: False, REPORT: False})
add('no-task-args.exe', erase(b'get_Args'), {SHELL: False, FILES: True})
add('no-output-sink.exe', erase('/c {0} > {1}'.encode('utf-16le')),
    {SHELL: False, FILES: True})
add('no-disk-event.exe', erase("TargetInstance ISA 'Win32_LogicalDisk'".encode('utf-16le')),
    {SHELL: True, FILES: False})
add('no-file-upload.exe', erase(b'UploadFileTaskAsync'),
    {SHELL: False, FILES: False, REPORT: True})
# Renaming namespace, C2, campaign and task-status text keeps behavior coverage.
renamed = raw
for token in [b'LSASS', 'msoftupdates'.encode('utf-16le'),
              'USBJOBSTARTED'.encode('utf-16le'),
              'FileNotCreatedAgainstCommand'.encode('utf-16le')]:
    renamed = erase(token, renamed)
add('renamed-implant.exe', renamed, {SHELL: True, FILES: True, REPORT: True})
# Root-heap binding rejects evidence moved into overlay or a benign dependency.
field = 'INFECTIONTYPE'.encode('utf-16le')
add('field-only-in-overlay.exe', erase(field) + field,
    {SHELL: False, FILES: False, REPORT: False})
p = dnfile.dnPE(str(PE))
cecil = next(r.data for r in p.net.resources if str(r.name).endswith('Mono.Cecil.dll'))
add('Mono.Cecil.dll', cecil, {SHELL: False, FILES: False, REPORT: False})
add('Cecil-with-implant-overlay.dll', cecil + raw,
    {SHELL: False, FILES: False, REPORT: False})

ps = PS.read_text()
add('renamed.ps1', ps.replace('sync-cache.example', 'other.example').replace('RemoteSupport', 'HelpDesk'),
    {OAUTH: True, APPX: True})
add('broker-read-and-unrelated-post.ps1', ps.replace(
    'body: "callback=" + encodeURIComponent(result.responseData)',
    'body: "status=ok"\n    // read separately: result.responseData'),
    {OAUTH: False, APPX: False})
add('own-oauth-client.ps1', ps.replace('d3590ed6-52b3-4102-aeff-aad2292ab01c',
    '11111111-1111-1111-1111-111111111111'), {OAUTH: False, APPX: False})
add('no-registration.ps1', ps[:ps.index('Add-AppxPackage')], {OAUTH: True, APPX: False})
add('excluded-remote-rule.ps1', ps.replace('Type="include"', 'Type="exclude"'),
    {OAUTH: True, APPX: False})
add('split-uri-rules.ps1', ps.replace('Type="include" WindowsRuntimeAccess="all"',
    'Type="include" /><uap:Rule Match="https://local.example/*" Type="exclude" WindowsRuntimeAccess="all"'),
    {OAUTH: True, APPX: False})
add('report-label.py', 'print("MachineName: workstation")\n', {NAME: True, OLDNAME: False})
# Existing host-permission consumers must keep their name roles after relocation.
base = {'manifest_version': 3, 'name': 'AI Chat PDF', 'version': '1.0',
        'host_permissions': ['<all_urls>'], 'permissions': ['debugger']}
add('utility/manifest.json', json.dumps(base),
    {NEW_NAMES+'ai-chat-pdf-name': True, GROUP: True})
base['name'] = 'Calendar'
add('calendar/manifest.json', json.dumps(base),
    {NEW_NAMES+'ai-chat-pdf-name': False, GROUP: False})

cmd = [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT), '--format', 'json']
result = subprocess.run(cmd + [str(p) for p, _ in cases], text=True,
                        capture_output=True, check=True)
(OUT / 'scan.json').write_text(result.stdout)
(OUT / 'stderr.txt').write_text(result.stderr)
assert not result.stderr.strip(), result.stderr
reports = {}; data = result.stdout.strip(); decoder = json.JSONDecoder()
while data:
    d, end = decoder.raw_decode(data); data = data[end:].strip()
    for f in d['files']:
        reports[f['path']] = {t['id']: t for t in f['traits']}
checks = []
for path, expected in cases:
    actual = reports[str(path)]
    for rule, want in expected.items():
        assert (rule in actual) == want, (path.name, rule, want)
    checks.append({'path': path.name, 'checks': expected, 'passed': True})
(OUT / 'checks.json').write_text(json.dumps(checks, indent=2)+'\n')
print(f'PASS: {len(cases)} static artifact/control cases')
