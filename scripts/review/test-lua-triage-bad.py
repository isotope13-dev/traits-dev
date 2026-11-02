#!/usr/bin/env python3
"""Static controls for Lua triage; never execute a fixture or contact its URLs."""
import argparse
import json
import lzma
from pathlib import Path
import re
import subprocess
import tempfile
import zipfile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cleave', default='../cleave/target/release/cleave')
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[2]
    fixture = 'generated/taxonomy/lua-triage-bad-20261102'
    data = {}
    for category in ['hostile', 'notable']:
        for p in (repo / 'testdata' / category / fixture).iterdir():
            if p.suffix == '.xz':
                data[p.stem] = lzma.decompress(p.read_bytes())
            else:
                data[p.name] = p.read_bytes()
    cases = dict(data)
    minimum = {n: 3 for n in ['ransom.lua', 'solaris.lua', 'dns-ssh.lua', 'http-phish.lua',
                              'worm.vbs', 'encrypted-launcher.js', 'virtualized-runtime.lua']}
    minimum.update({'Jamfile.lua': 2})
    benign = {'inert-config.lua', 'vm-guest-config.lua', 'language-spec.lua'}
    require, forbid = {}, {}
    ransom = 'objectives/impact/ransom/encrypt/bulk-encryption::lua-ransom-file-rewrite'
    archive = 'objectives/exfiltration/http/archive::lua-system-config-archive-upload'
    audit = 'objectives/evasion/security-bypass/disable-service::lua-disables-auditing-and-tpm'
    log = 'objectives/evasion/indicator-removal/log-removal::lua-unix-log-truncate'
    cron = 'objectives/persistence/system/cron/schedule::lua-covert-scheduled-fetch-shell'
    dns = 'objectives/exfiltration/dns/query::lua-sequenced-data-dns-queries'
    ssh = 'objectives/lateral-movement/brute-force/raw-ssh::lua-password-ssh-loop'
    key = 'objectives/persistence/login/ssh-authorized-keys::lua-credential-loop-installs-ssh-key'
    upload = 'objectives/exfiltration/stealer/credential/raw-file::lua-secret-file-http-upload'
    hidden = 'objectives/execution/payload/file-exec/command/fetch::lua-concealed-curl-batch-stage'
    require.update({'ransom.lua': {ransom, archive}, 'solaris.lua': {audit, log, cron},
                    'dns-ssh.lua': {dns, ssh, key}, 'http-phish.lua': {upload}})

    def add(name, content, *, good=False, count=None, yes=(), no=()):
        cases[name] = content.encode() if isinstance(content, str) else content
        if good:
            benign.add(name)
        if count is not None:
            minimum[name] = count
        if yes:
            require[name] = set(yes)
        if no:
            forbid[name] = set(no)

    # Future variants change domains, variable/function names, field names,
    # whitespace, shell spelling and safety gates while preserving behavior.
    for name in ['ransom.lua', 'solaris.lua', 'dns-ssh.lua', 'http-phish.lua']:
        text = data[name].decode().replace('review.example.invalid', 'staging.example.net')
        for old, new in [('C2_HOST', 'endpoint'), ('STAGE_DIR', 'workspace'),
                         ('filepath', 'location'), ('content', 'buffer'),
                         ('run', 'capture_command'), ('_dns_exfil', 'send_chunks')]:
            text = re.sub(r'\b' + re.escape(old) + r'\b', new, text)
        variant = 'renamed-' + name
        add(variant, text, count=3)
    text = data['solaris.lua'].decode()
    add('ungated-solaris.lua', text[text.index('-- Configuration'):], count=3)
    text = data['ransom.lua'].decode()
    start = text.index('local function _safety_gate()')
    end = text.index('local function _detect_sandbox()', start)
    text = text[:start] + text[end:]
    text = re.sub(r'(?m)^\s*_safety_gate\(\)\s*$', '', text)
    add('ungated-ransom.lua', text, count=3)
    text = data['dns-ssh.lua'].decode()
    text = text.replace('cred.pass', 'cred.secret').replace('cred.user', 'cred.login')
    text = re.sub(r'\bpass\s*=', 'secret=', text)
    text = re.sub(r'\buser\s*=', 'login=', text)
    add('renamed-credential-fields.lua', text, yes={ssh, key, dns}, count=3)
    text = data['dns-ssh.lua'].decode()
    text = re.sub(r'(?m)^\s*os.execute\(string.format\(\x27nslookup[^\n]+\n', '', text)
    text = text.replace('%02x', '%02X').replace('%03d', '%04d').replace('#encoded, 60', '#encoded, 50')
    add('dig-uppercase-hex.lua', text, yes={dns})
    add('no-dns-transfer.lua', data['dns-ssh.lua'].decode().replace('nslookup -type=txt', 'echo').replace('dig +short TXT', 'echo'), no={dns})
    add('logged-solaris.lua', data['solaris.lua'].decode().replace('    run(', '    print('), no={audit, log, cron})
    add('no-ransom-replacement.lua', data['ransom.lua'].decode().replace('io.open(filepath, "wb")', 'io.open("preview.bin", "wb")'), no={ransom, archive})
    add('ordinary-backup.lua', '''local archive="/tmp/backup.tar.gz"
os.execute("tar czf "..archive.." /etc/ 2>/dev/null")
os.execute("curl -X POST -F file=@/tmp/backup.tar.gz https://backup.example.invalid/upload")
''', good=True)
    add('unrelated-log-and-output.lua', 'local input="/var/log/syslog"\nlocal out=io.open("report.txt","w")\nreturn input,out\n', good=True)
    add('inert-route.lua', 'return {route="/api/v1/exfil", methods={"GET","POST"}}\n', good=True)
    add('key-name-map.lua', 'return {"id_rsa","id_ed25519","authorized_keys","/.netrc","/.ssh/id_rsa"}\n', good=True)
    add('hostname-helper.lua', 'local socket=require("socket")\nlocal hostname=socket.dns.gethostname()\nreturn hostname\n', good=True)
    add('report-upload.lua', '''local http=require("socket.http")
local f=io.open("report.txt","r")
local text=f:read("*a")
http.request("https://reports.example.invalid",text)
''', good=True)
    add('aes-data-only.js', '''const fs=require('fs'),crypto=require('crypto');
const d=crypto.createDecipheriv('aes-256-cbc',key,iv);
fs.writeFileSync('report.bin',d.update(fs.readFileSync('data.bin')));
''', good=True)
    add('run-key-installer.js', '''const {execSync}=require('child_process');
execSync('reg add "HKCU\\\\Software\\\\Microsoft\\\\Windows\\\\CurrentVersion\\\\Run" /v App /d app.exe');
''', good=True)
    add('plain-task-config.lua', '''return {name="WindowsDefenderScheduledScan",command="schtasks /create /sc daily",paths={"C:/data"}}
''', good=True)
    add('quoted-solaris.lua', 'return [====[' + data['solaris.lua'].decode() + ']====]\n', good=True)
    add('quoted-http-program.lua', 'return [====[' + data['http-phish.lua'].decode() + ']====]\n', good=True)
    add('commented-solaris.lua', '--[====[' + data['solaris.lua'].decode() + ']====]\nreturn {}\n', good=True)
    hook = data['Jamfile.lua'].decode()
    add('renamed-project.lua', hook, count=1, yes={hidden})
    add('hook-without-hide.lua', hook.replace('ffi.C.ShowWindow(hWnd, SW_HIDE)', 'print(hWnd, SW_HIDE)'), no={hidden})
    add('hook-renamed-hide-variable.lua', hook.replace('SW_HIDE', 'display_mode'), yes={hidden}, count=1)
    add('ordinary-data-fetch.lua', 'os.execute("curl -o report.csv https://reports.example.invalid/report.csv")\n', good=True)
    add('logged-stage-command.lua', hook.replace('os.execute(', 'print('), good=True)
    add('quoted-hook.lua', 'return [====[' + hook + ']====]\n', good=True)
    spec = data['language-spec.lua'].decode()
    add('renamed-language-spec.lua', spec.replace('createProcess', 'launch').replace('user-data.lua', 'settings-extra.lua'), good=True, yes={'micro-behaviors/process/deploy/interpreter-command::lua-module-native-interpreter-helper'})
    add('no-native-spec-launch.lua', spec.replace('ffi.C.CreateProcessW(', 'log_only('), good=True)

    with tempfile.TemporaryDirectory(prefix='lua-bad-controls-') as directory:
        work = Path(directory)
        for name, content in cases.items():
            (work/name).write_bytes(content)
        # Archive scope must be retained; neither a filename nor the container
        # signature provides the verdict for these embedded members.
        with zipfile.ZipFile(work/'editor-bundle.zip', 'w', zipfile.ZIP_DEFLATED) as out:
            out.writestr('spec/new-language.lua', data['language-spec.lua'])
            out.writestr('cfg/user-data.lua', data['virtualized-runtime.lua'])
        minimum['editor-bundle.zip'] = 3
        cases['editor-bundle.zip'] = b''
        result = subprocess.run([str((repo/args.cleave).resolve()), '--traits-dir', str(repo),
                                 '--all-files', '--format=json', str(work)],
                                check=True, capture_output=True, text=True)
        assert 'skipped trait file' not in result.stderr, result.stderr
        reports = [json.loads(line) for line in result.stdout.split('\n') if line.strip()]
        roots = {Path(report['files'][0]['path']).name: report['files'][0] for report in reports}
        assert set(cases) <= roots.keys(), set(cases)-roots.keys()
        for name in cases:
            traits = roots[name].get('traits', [])
            ids = {t['id'] for t in traits}
            elevated = {t['id'] for t in traits if t['crit'] >= 4}
            hostile = {t['id'] for t in traits if t['crit'] >= 5}
            if name in benign:
                assert not elevated, (name, elevated)
            if name in minimum:
                assert len(hostile) >= minimum[name], (name, hostile)
            assert require.get(name, set()) <= ids, (name, require.get(name,set())-ids)
            assert not forbid.get(name, set()) & ids, (name, forbid.get(name,set()) & ids)
            print('PASS', name)
        assert roots['worm.vbs']['type'] == 'vbs'
        assert roots['language-spec.lua']['type'] == 'lua'
    print(f'{len(cases)} Lua bad-triage controls passed')


if __name__ == '__main__':
    main()
