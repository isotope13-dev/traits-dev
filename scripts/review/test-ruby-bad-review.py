#!/usr/bin/env python3
"""Static Ruby edge-case regressions; no sample code is executed."""
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
H = ROOT / 'testdata/hostile/generated/ruby-bad-review'
S = ROOT / 'testdata/suspicious/generated/ruby-bad-review'
N = ROOT / 'testdata/notable/generated/ruby-bad-review'
SHELL = 'objectives/command-and-control/reverse-shell/fd-redirect::ruby-syscall-stdio-reverse-shell'
DOWNLOAD = 'objectives/execution/payload/file-exec/detached::ruby-hidden-temp-download-launch'
INSTALL = 'objectives/supply-chain/install-hook/extconf::extconf-hidden-temp-download-launch'
KEY = 'objectives/credential-access/ssh/key::ruby-home-private-key-post-collector'
AWS = 'objectives/credential-access/cloud/account::ruby-home-aws-credential-post-collector'
COOKIE = 'objectives/command-and-control/backdoor/webshell/client::ruby-cookie-command-shell-client'
LDAP = 'objectives/execution/exploit/buffer-overflow::ruby-ldap-rewrite-buffer-overflow'
POPEN = 'objectives/command-and-control/remote-command/dispatch/command::ruby-tcp-popen-command-shell'
FLOW = 'objectives/command-and-control/dropper/delivery/fetch-exec::ruby-temporary-executable-http-dropper'
SHADOW = 'objectives/exfiltration/stealer/credential/value/password::ruby-shadow-encoded-http-exporter'
RANSOM = 'objectives/impact/ransom/encrypt/filesystem::ruby-ransom-bulk-rename-encryption'
CALLBACK = 'objectives/supply-chain/install-hook/extconf::extconf-host-profile-shell-callback'
CLIP = 'objectives/impact/crypto-manipulation/clipboard::vbs-htmlfile-clipboard-clipper'
CLIP_RUN = 'objectives/persistence/login/registry/autostart::vbs-wallet-clipper-run-persistence'
CLIP_REMOVE = 'objectives/evasion/self-delete/process::vbs-wallet-clipper-source-removal'


def objects(text):
    decoder = json.JSONDecoder()
    offset = 0
    while offset < len(text):
        while offset < len(text) and text[offset].isspace():
            offset += 1
        if offset == len(text):
            return
        value, offset = decoder.raw_decode(text, offset)
        yield value


def main():
    cases = {}

    def add(name, path, required=(), forbidden=(), transform=lambda s: s, severity=None):
        cases[name] = (path.name, transform(path.read_text()), set(required), set(forbidden), severity)

    for name, required in {
        'syscall-shell': [SHELL], 'hidden-download': [DOWNLOAD],
        'native-loader': [DOWNLOAD, INSTALL], 'native-credential-hook': [KEY, AWS],
        'session-store': [KEY, AWS], 'cookie-client': [COOKIE], 'ldap-overflow': [LDAP],
        'socket-popen': [POPEN], 'credential-message': [SHADOW],
        'trojan-downloader': [FLOW], 'native-ransom': [RANSOM],
        'host-callback': [CALLBACK], 'wallet-clipper': [CLIP, CLIP_RUN, CLIP_REMOVE],
    }.items():
        path = next((H / name).iterdir())
        add(name, path, required)
    syscall = H / 'syscall-shell/sample.rb'
    add('renamed-socket', syscall, [SHELL], transform=lambda s: re.sub(r'\bs\b', 'channel', re.sub(r'\bfd\b', 'descriptor', s)))
    add('different-dup-source', syscall, forbidden=[SHELL], transform=lambda s: s.replace('s.fileno', 'other.fileno'))
    add('different-dup-destination', syscall, forbidden=[SHELL], transform=lambda s: s.replace('s.fileno, fd', 's.fileno, 9'))
    add('quoted-loader', H / 'hidden-download/sample.rb', forbidden=[DOWNLOAD], transform=lambda s: "puts <<'EXAMPLE'\n" + s + '\nEXAMPLE\n')
    key = H / 'native-credential-hook/extconf.rb'
    add('renamed-secret-helpers', key, [KEY, AWS], transform=lambda s: re.sub(r'\b_r\b', 'read_profile_file', s))
    add('unused-secret-reader', key, forbidden=[KEY, AWS], transform=lambda s: s.replace('def _r(p)', 'def unused_reader(p)'))
    add('different-sent-request', key, forbidden=[KEY, AWS], transform=lambda s: s.replace('_http.request(_req)', '_http.request(other_request)'))
    add('quoted-cookie-module', H / 'cookie-client/sample.rb', forbidden=[COOKIE], transform=lambda s: "puts <<'EXAMPLE'\n" + s + '\nEXAMPLE\n')
    add('ordinary-ldap-request', H / 'ldap-overflow/sample.rb', forbidden=[LDAP], transform=lambda s: s.replace('/ldap://localhost/%3fA%3fA%3fCCCCCCCCCC%3fC%3f%90', '/directory/search'))
    add('different-downloaded-file', H / 'trojan-downloader/sample.rb', forbidden=[FLOW], transform=lambda s: s.replace("system('/tmp/autosymbiontic')", "system('/tmp/other')"))
    add('different-secret-message', H / 'credential-message/sample.rb', forbidden=[SHADOW], transform=lambda s: s.replace('users: user_data,', 'users: ordinary_stats,'))
    direct_key = ROOT / 'testdata/hostile/samples/ruby-ssh-key-read-exfil.rb'
    direct_key_id = 'objectives/exfiltration/stealer/credential/value/key::ruby-private-key-content-http-export'
    add('direct-key-export', direct_key, [direct_key_id])
    add('different-key-value', direct_key, forbidden=[direct_key_id], transform=lambda s: s.replace('key=#{key}', 'key=#{public_name}'))
    env = ROOT / 'testdata/hostile/generated/taxonomy/ruby-env-json-http-flow/positive-foxtailflow-extconf.rb'
    env_id = 'objectives/exfiltration/stealer/configuration/environment::ruby-filtered-secret-env-json-post'
    add('environment-json-export', env, [env_id])
    add('different-env-request', env, forbidden=[env_id], transform=lambda s: s.replace('http.request(request)', 'http.request(other_request)'))
    for folder in S.iterdir():
        add('suspicious-' + folder.name, next(folder.iterdir()), severity='suspicious')
    for folder in N.iterdir():
        add('ordinary-' + folder.name, next(folder.iterdir()), severity='ordinary')

    with tempfile.TemporaryDirectory(prefix='ruby-bad-review-') as temp:
        paths = []
        for name, (filename, source, *_rest) in cases.items():
            path = Path(temp) / name / filename
            path.parent.mkdir()
            path.write_text(source)
            paths.append(str(path))
        command = [os.environ.get('CLEAVE', str(ROOT.parent / 'cleave/target/release/cleave')),
                   '--traits-dir', str(ROOT), '--format=json', *paths]
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        observed = {}
        for report in objects(result.stdout):
            for item in report['files']:
                observed.setdefault(Path(item['path']).parent.name, []).extend(item.get('traits', []))
        failures = []
        for name, (_, _, required, forbidden, severity) in cases.items():
            traits = observed[name]
            hostile = {item['id'] for item in traits if item['crit'] == 5}
            suspicious = {item['id'] for item in traits if item['crit'] == 4}
            if required - hostile or forbidden & {item['id'] for item in traits}:
                failures.append((name, sorted(required - hostile), sorted(forbidden & {item['id'] for item in traits})))
            if severity == 'ordinary' and (hostile or suspicious):
                failures.append((name, 'unexpected severity', sorted(hostile | suspicious)))
            if severity == 'suspicious' and (hostile or not 2 <= len(suspicious) <= 3):
                failures.append((name, 'expected 2–3 suspicious and no hostile', sorted(hostile | suspicious)))
        assert not failures, json.dumps(failures, indent=2)
    print(f'Ruby bad-review regressions passed: {len(cases)} cases')


if __name__ == '__main__':
    main()
