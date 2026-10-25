"""Trace only the two decoded functions with in-memory file/crypto/HTTP stubs."""
import ast
import base64
import hashlib
import io
import json
from pathlib import Path
import tarfile
import types
import urllib.request

source = Path(__file__).with_name('encrypted-collector.py').read_text()
module = ast.parse(source)
functions = [n for n in module.body if isinstance(n, ast.FunctionDef)]
assert [n.name for n in functions] == ['collect', 'pc_post']
events = {'reads': [], 'requests': []}


def fake_open(path, mode):
    assert mode == 'rb'
    events['reads'].append(path)
    return io.BytesIO(b'LOGIN-SENTINEL' if path.endswith('logins.json') else b'KEY-SENTINEL')


class Cipher:
    def encrypt(self, data):
        events['padded_report'] = data
        return b'CIPHERTEXT-SENTINEL'


class Wrapper:
    def encrypt(self, key):
        events['wrapped_key'] = key
        return b'WRAPPED-KEY-SENTINEL'


class Response:
    status = 200

    def __enter__(self):
        return self

    def __exit__(self, *_):
        pass


def fake_urlopen(request, timeout):
    events['requests'].append(request)
    assert timeout == 120
    return Response()


environment = {'SENTINEL_SECRET': 'ENV-SENTINEL'}
globals_ = {
    '__builtins__': __builtins__, 'base64': base64, 'json': json, 'io': io,
    'tarfile': tarfile, 'hashlib': hashlib, 'open': fake_open,
    'time': types.SimpleNamespace(time=lambda: 1234, sleep=lambda _: None),
    'os': types.SimpleNamespace(environ=environment, urandom=lambda n: b'K' * n,
                                uname=lambda: types.SimpleNamespace(nodename='fixture-host')),
    'AES': types.SimpleNamespace(MODE_CBC=2, new=lambda *_: Cipher()),
    'RSA': types.SimpleNamespace(construct=lambda _: object()),
    'PKCS1_OAEP': types.SimpleNamespace(new=lambda _: Wrapper()),
    'pad': lambda b, n: b + bytes([n - len(b) % n]) * (n - len(b) % n),
    'urllib': types.SimpleNamespace(request=types.SimpleNamespace(
        Request=urllib.request.Request, urlopen=fake_urlopen)),
}
# This excludes imports, thread creation, the polling daemon, and outer exec.
exec(compile(ast.Module(body=functions, type_ignores=[]), '<stubbed-functions>', 'exec'), globals_)
globals_['collect']()
assert len(events['requests']) == 1
request = events['requests'][0]
padded = events['padded_report']
report = json.loads(padded[:-padded[-1]])
assert base64.b64decode(report['logins.json']) == b'LOGIN-SENTINEL'
assert base64.b64decode(report['key4.db']) == b'KEY-SENTINEL'
assert report['env'] == environment
assert events['wrapped_key'] == b'K' * 32
with tarfile.open(fileobj=io.BytesIO(request.data), mode='r:gz') as archive:
    assert archive.getnames() == ['hdr.json', 'data.bin', 'key.bin']
    assert archive.extractfile('data.bin').read() == b'K' * 16 + b'CIPHERTEXT-SENTINEL'
    assert archive.extractfile('key.bin').read() == b'WRAPPED-KEY-SENTINEL'
assert request.headers['X-sha256'] == hashlib.sha256(request.data).hexdigest()
print(json.dumps({'reads': events['reads'], 'report_fields': list(report),
                  'tar_members': ['hdr.json', 'data.bin', 'key.bin'],
                  'request_method': request.method, 'request_url': request.full_url,
                  'network': 'stubbed', 'crypto': 'stubbed; data flow only'}))
