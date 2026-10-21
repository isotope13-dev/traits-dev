"""Focused controls for bytecode observations and shortened HTML handoffs.

Run with Python 3.12: uv run --python 3.12 python testdata/triage/phantom-html/check.py
Only compiles synthetic source; none of the fixture code is executed.
"""
import importlib.util
import json
import marshal
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[3]
DNS = 'micro-behaviors/communications/dns/label::pyc-base32-resolver-name-sequence'
CLEAN = 'micro-behaviors/fs/delete/file/command::pyc-detached-ping-delete-argv'
WIFI = 'micro-behaviors/hardware/wireless/network::netsh-plaintext-key-command-text'
REDIRECT = 'micro-behaviors/ui/window/navigation::instant-shortened-meta-refresh'
DECOY = 'objectives/evasion/decoy/lure::empty-blog-loading-shortener-handoff'

CASES = {
    'dns-helper.pyc': ('''import base64, socket
def transfer(data, domain):
    encoded = base64.b32encode(data).decode('ascii').rstrip('=')
    for i in range(0, len(encoded), 50):
        socket.getaddrinfo(encoded[i:i+50] + '.' + domain, None)
''', {DNS: True, CLEAN: False}),
    'unrelated-helpers.pyc': ('''import base64, socket
def encode(data):
    return base64.b32encode(data)
def lookup(host):
    return socket.getaddrinfo(host, None)
''', {DNS: False, CLEAN: False}),
    'plain-resolver.pyc': ('''import socket
def lookup(host):
    return socket.getaddrinfo(host, None)
''', {DNS: False}),
    'cleanup-helper.pyc': ('''import os, sys, subprocess
def cleanup():
    path = os.path.abspath(sys.argv[0])
    command = 'cmd.exe /C "ping -n 3 127.0.0.1 >nul & del /f /q "' + path
    subprocess.Popen(command, creationflags=subprocess.DETACHED_PROCESS)
''', {CLEAN: True, DNS: False}),
    'foreground-delete.pyc': ('''import os, sys, subprocess
def cleanup():
    path = os.path.abspath(sys.argv[0])
    command = 'cmd.exe /C "ping -n 3 127.0.0.1 >nul & del /f /q "' + path
    subprocess.run(command)
''', {CLEAN: False}),
    'audit-prose.pyc': ('''import subprocess
advice = "Passwords can be recovered with netsh wlan show profile name=X key=clear."
subprocess.run('netsh wlan show profiles', capture_output=True)
''', {WIFI: True, DNS: False, CLEAN: False,
       'objectives/credential-access/wifi::netsh-wlan-key-clear': False,
       'objectives/credential-access/wifi::netsh-wifi-password-extraction': False}),
}
CASES.update({
    'encoded-powershell.pyc': ('command = "powershell.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass -EncodedCommand "', {
        'micro-behaviors/process/argument/option::python-powershell-command-option': True,
    }),
    'product-references.pyc': ('''descriptions = ["CPU-Z application", "PuTTY SSH client", "Apache Tomcat server", "regsvr32.exe /s"]
''', {
        'micro-behaviors/os/application/target::cpuz-product-reference': True,
        'micro-behaviors/os/application/target::putty-product-reference': True,
        'micro-behaviors/os/application/target::apache-tomcat-product-reference': True,
        'micro-behaviors/fs/path/application/executable::regsvr32-name-reference': True,
        'micro-behaviors/process/create/launch::regsvr32-command-text': False,
        'metadata/file/string/application-name::tool-identity-cpuid': False,
        'metadata/file/string/application-name::tool-identity-putty': False,
    }),
    'interpreter-paths.js': ('const paths = ["bin/python", "bin/node", "bin/ruby"];', {
        'micro-behaviors/fs/path/application/interpreter::bin-python': True,
        'micro-behaviors/fs/path/application/interpreter::bin-node': True,
        'micro-behaviors/fs/path/application/interpreter::bin-ruby': True,
    }),
})
refresh = "<meta content='0;URL=https://bit.ly/example' http-equiv='refresh'>"
cover = "<title>...Loading...</title><div class='main no-items section' id='main'></div>"
CASES.update({
    'empty-blog-redirect.html': (refresh + cover, {REDIRECT: True, DECOY: True}),
    'ordinary-link.html': ("<a href='https://bit.ly/example'>Read more</a>" + cover,
                           {REDIRECT: False, DECOY: False}),
    'direct-loading-redirect.html': (refresh.replace('bit.ly/example', 'example.org/new') + cover,
                                     {REDIRECT: False, DECOY: False}),
    'commented-redirect.html': ('<!--' + refresh + '-->' + cover,
                               {REDIRECT: False, DECOY: False}),
    'shortened-redirect.html': (refresh, {REDIRECT: True, DECOY: False}),
    'separate-meta-elements.html': (
        "<meta content='0;URL=https://bit.ly/example' name='description'>"
        "<meta content='0;URL=https://example.org' http-equiv='refresh'>",
        {REDIRECT: False, DECOY: False}),
    'non-meta-attributes.html': (refresh.replace('<meta ', '<div '),
                                 {REDIRECT: False, DECOY: False}),
})

def main():
    if sys.version_info[:2] != (3, 12):
        raise SystemExit('Use Python 3.12 for the marshalled bytecode controls')
    with tempfile.TemporaryDirectory(prefix='controls-', dir=Path(__file__).parent) as tmp:
        paths = []
        for name, (source, _) in CASES.items():
            path = Path(tmp) / name
            if name.endswith('.pyc'):
                code = compile(source, name[:-1], 'exec')
                path.write_bytes(importlib.util.MAGIC_NUMBER + b'\0'*12 + marshal.dumps(code))
            else:
                path.write_text(source)
            paths.append(str(path))
        proc = subprocess.run([os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
                               '--format', 'json', *paths], capture_output=True, text=True)
        if proc.returncode:
            raise RuntimeError(proc.stderr)
        reports = []
        decoder = json.JSONDecoder()
        remaining = proc.stdout.lstrip()
        while remaining:
            report, end = decoder.raw_decode(remaining)
            reports.extend(report['files'])
            remaining = remaining[end:].lstrip()
        checked = 0
        for report in reports:
            name = Path(report['path']).name
            if name not in CASES:
                continue
            ids = {t['id'] for t in report.get('traits', [])}
            for trait, expected in CASES[name][1].items():
                assert (trait in ids) == expected, (name, trait, expected)
                checked += 1
        assert len({Path(r['path']).name for r in reports} & CASES.keys()) == len(CASES)
        print(f'{len(CASES)} fixtures; {checked} assertions passed')

if __name__ == '__main__':
    main()
