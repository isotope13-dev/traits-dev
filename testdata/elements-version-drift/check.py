#!/usr/bin/env python3
"""Check the behavior boundaries changed during the Elements triage."""
import json
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parents[2]
if len(sys.argv) > 1:
    output = Path(sys.argv[1]).read_text()
else:
    output = subprocess.check_output([
        'cleave', '--traits-dir', str(root), '--format', 'json',
        str(root / 'testdata/native-proc-self-unlink'),
        str(root / 'testdata/elements-version-drift'),
    ], text=True, cwd=root)
decoder = json.JSONDecoder()
files = {}
while output.strip():
    output = output.lstrip()
    report, end = decoder.raw_decode(output)
    output = output[end:]
    for file in report['files']:
        files[Path(file['path']).name] = {t['id'] for t in file.get('traits', [])}

checks = 0

def check(file, present=(), absent=()):
    global checks
    assert file in files, f'Missing fixture: {file}'
    ids = files[file]
    for trait in present:
        assert trait in ids, f'{file}: missing {trait}'
    for trait in absent:
        assert trait not in ids, f'{file}: unexpected {trait}'
    checks += 1

self_delete = 'objectives/evasion/self-delete/file/script::native-proc-self-path-unlink'
check('positive.c', present=[self_delete])
check('renamed-positive.cpp', present=[self_delete])
for name in ['autostart.c', 'different-target.c', 'overwritten-buffer.c', 'other-symlink.c']:
    check(name, absent=[self_delete])
native_apis = [
    'micro-behaviors/communications/socket/bind/function::native-sockaddr-bind-call',
    'micro-behaviors/fs/file/handle::source-commit-transaction-call',
    'micro-behaviors/fs/file/stat::source-getfilesize-reference',
    'micro-behaviors/fs/delete/file/library::remove-source-call',
    'micro-behaviors/os/application/target::wallet-brand-coinbase',
    'micro-behaviors/crypto/symmetric/analysis::meet-in-middle-marker',
]
check('native-positive.c', present=native_apis)
check('native-negative.cpp', absent=native_apis + [
    'micro-behaviors/fs/file/handle::commit-transaction-import',
    'micro-behaviors/fs/file/handle::commit-transaction-api',
    'micro-behaviors/communications/socket/bind/function::bind',
    'micro-behaviors/communications/socket/listen::source-bind-call',
    'micro-behaviors/fs/delete/file/library::remove',
])
check('license-credit.cpp', present=[
    'metadata/package/license::openssl-project-copyright',
    'metadata/package/license::openssl-eric-young-copyright',
], absent=['well-known/lib/crypto/openssl::openssl-implementation-identifiers'])
check('native-operations.cpp', present=[
    'micro-behaviors/data/arithmetic::indexed-xor-array-assignment',
    'micro-behaviors/dylib/lookup::get-proc-address-source-call',
    'micro-behaviors/data/format/bitcoin-script::bitcoin-opreturn-source',
    'micro-behaviors/data/format/bitcoin-script::bitcoin-opreturn-source-text',
], absent=['micro-behaviors/crypto/symmetric/xor/loop::indexed-xor-array-assignment'])
check('ascii-pixels.xpm', present=['metadata/file/magic/identity::xpm-source-header'],
      absent=['metadata/lang/natural/script::lang-korean-source'])
check('native-positive.c', present=['metadata/lang/natural/script::lang-korean-source'])
python_xor = 'micro-behaviors/data/arithmetic::python-xor-expression'
check('xor-expression.py', present=[python_xor])
check('xor-operator.py', present=[python_xor])
check('xor-string.py', absent=[python_xor])
write_traits = [
    'micro-behaviors/fs/write/file/handle::native-write-file-call',
    'micro-behaviors/fs/write/file/full::native-looped-write-call',
]
check('write-positive.c', present=write_traits)
check('write-negative.cpp', absent=write_traits)
print(f'PASS: {checks} positive and near-miss checks')
