"""Regression checks scan source and bytecode; no fixture is executed."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
ENGINE = os.environ.get('CLEAVE', 'cleave')
ENV = 'objectives/exfiltration/stealer/env::python-proc-environ-encrypted-upload'
BUNDLE = 'micro-behaviors/fs/read/file/full::python-proc-environ-json-bundle'
UPLOAD = 'micro-behaviors/communications/http/upload::python-credential-dictionary-encrypted-post'
PADDING = 'micro-behaviors/crypto/cipher::pycrypto-padding-module-ref'
NULL = 'micro-behaviors/process/fd/dup::python-null-device-dup2'
TOUCH = 'micro-behaviors/fs/file/create::python-path-touch'
LOCK = 'micro-behaviors/fs/lock::python-fcntl-exclusive-nonblocking'
RANSOM = 'objectives/impact/ransom/encrypt/bytecode::pyc-cbc-file-encryption-ransom-demand'
AES = 'micro-behaviors/crypto/symmetric/aes/library::pycrypto-aes-import'

def findings(path):
    result = subprocess.run([ENGINE, '--traits-dir', str(ROOT), '--format', 'json', str(path)],
                            check=True, text=True, capture_output=True)
    data = json.loads(result.stdout)
    def walk(value):
        if isinstance(value, dict):
            if isinstance(value.get('id'), str):
                yield value['id']
            for item in value.values():
                yield from walk(item)
        elif isinstance(value, list):
            for item in value:
                yield from walk(item)
    return set(walk(data))

def main():
    original = (HERE / 'collector.py').read_text()
    cases = [
        ('collector.py', original, {ENV, BUNDLE, UPLOAD, PADDING}, set()),
        ('other-root.py', original.replace("Path('/proc')", "Path('/reports')"),
         {UPLOAD, PADDING}, {ENV, BUNDLE}),
        ('other-store.py', original.replace('records[str(process_file)]', 'local_only[str(process_file)]'),
         {PADDING}, {ENV, BUNDLE, UPLOAD}),
        ('other-reader.py', original.replace('process_file.read_bytes()', 'unrelated_file.read_bytes()'),
         {UPLOAD}, {ENV, BUNDLE}),
        ('overwritten.py', original.replace('    serialized =', '    records = {}\n    serialized ='),
         {PADDING}, {ENV, BUNDLE, UPLOAD}),
        ('other-json.py', original.replace('json.dumps(records)', 'json.dumps(telemetry)'),
         {PADDING}, {ENV, BUNDLE, UPLOAD}),
        ('discarded-cipher.py', original.replace('data=envelope + vector + ciphertext', "data=b'heartbeat'"),
         {BUNDLE}, {ENV, UPLOAD}),
        ('read-only.py', original.split('    serialized =')[0], set(), {ENV, BUNDLE, UPLOAD}),
        ('null.py', "import os\nfd = os.open('/dev/null', os.O_RDWR)\nos.dup2(fd, 1)\n", {NULL}, set()),
        ('other-fd.py', "import os\nfd = os.open('/dev/null', os.O_RDWR)\nos.dup2(other_fd, 1)\n", set(), {NULL}),
        ('other-device.py', "import os\nfd = os.open('/dev/tty', os.O_RDWR)\nos.dup2(fd, 1)\n", set(), {NULL}),
        ('touch.py', "from pathlib import Path\nmarker = Path('/tmp/done')\nmarker.touch()\n", {TOUCH}, set()),
        ('object-touch.py', "marker = Widget()\nmarker.touch()\n", set(), {TOUCH}),
        ('lock.py', 'import fcntl\nfcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)\n', {LOCK}, set()),
        ('blocking.py', 'import fcntl\nfcntl.flock(lock, fcntl.LOCK_EX)\n', set(), {LOCK}),
        ('comment-lock.py', '# fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)\n', set(), {LOCK}),
        ('padding-only.py', 'from Crypto.Util.Padding import pad\n', {PADDING}, {AES}),
        ('no-padding.py', 'from Crypto.Cipher import AES\n', {AES}, {PADDING}),
    ]
    with tempfile.TemporaryDirectory(prefix='proc-upload-controls-') as directory:
        base = Path(directory)
        for name, source, required, forbidden in cases:
            path = base / name
            path.write_text(source)
            actual = findings(path)
            assert required <= actual, (name, 'missing', required - actual)
            assert not (forbidden & actual), (name, 'unexpected', forbidden & actual)
        # Preserve the migrated padding reference in real marshal bytecode,
        # including its existing ransomware consumer and a no-demand control.
        source = '''from Crypto.Util.Padding import pad
def encrypt():
    return ('MODE_CBC', 'decrypt pay bitcoin')
def walk():
    pass
def remove():
    pass
'''
        import marshal
        for name, body, required, forbidden in [
            ('ransom.pyc', source, {PADDING, RANSOM}, set()),
            ('padding.pyc', source.replace('decrypt pay bitcoin', 'ordinary archive'), {PADDING}, {RANSOM}),
        ]:
            path = base / name
            code = compile(body, name, 'exec')
            path.write_bytes(importlib.util.MAGIC_NUMBER + bytes(12) + marshal.dumps(code))
            actual = findings(path)
            assert required <= actual, (name, 'missing', required - actual)
            assert not (forbidden & actual), (name, 'unexpected', forbidden & actual)
    # Existing positive outside this review retains its padding signal.
    assert PADDING in findings(ROOT / 'testdata/hostile/png-tail-decrypt.py')
    print('21 source/bytecode positive and near-miss controls passed')

if __name__ == '__main__':
    main()
