"""Focused negative controls for unsupported PE intent claims.

Usage: python3 check.py SCRATCH_DIRECTORY DOTNET_SAMPLE
Only static analysis is performed.
"""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location(
    'fixture', ROOT / 'testdata/packed-multipart-build-marker-exfil/verify.py')
fixture = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fixture)
DEST = Path(sys.argv[1])
DEST.mkdir(parents=True, exist_ok=True)

def scan(path):
    result = subprocess.run(
        [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
         '--format', 'json', str(path)],
        text=True, capture_output=True, check=True)
    report = json.loads(result.stdout)
    return {t['id'] for f in report['files'] for t in f['traits']}

retired = {
    'objectives/exfiltration/messaging/email::smtp-helo-mime-exfil',
    'objectives/exfiltration/messaging/email::smtp-helo-wininet',
    'objectives/evasion/process/injection/atom-bombing::atom-bombing-capable',
    'objectives/command-and-control/beacon/mutex::mutex-guid-crypto-http-coordination',
}
base = [('KERNEL32.dll', 'LoadLibraryA'), ('KERNEL32.dll', 'GetProcAddress')]
for name, imports, strings in [
    ('smtp-mime-wininet', base, ['HELO %s', 'Content-Transfer-Encoding: base64', 'WININET.dll']),
    ('atom-memory-write', base + [('KERNEL32.dll', 'GlobalAddAtomA'),
       ('KERNEL32.dll', 'GlobalGetAtomNameA'), ('KERNEL32.dll', 'WriteProcessMemory')], []),
    ('native-thread-name', base, ['NtCreateThreadEx']),
]:
    path = DEST / (name + '.exe')
    path.write_bytes(fixture.build_pe(imports, strings))
    ids = scan(path)
    assert not (ids & retired), (name, ids & retired)
    if name == 'atom-memory-write':
        assert not any('atom-bombing' in i for i in ids), ids
        assert 'micro-behaviors/communications/ipc/message::global-atom-table-readback' in ids
    if name == 'native-thread-name':
        assert 'micro-behaviors/process/create/thread::nt-create-thread-ex-name' in ids
        assert 'micro-behaviors/process/inject/runtime/call::native-remote-thread-create' not in ids
        assert 'micro-behaviors/process/inject/remote-thread::remote-thread-api-reference' not in ids
    print('PASS', name, flush=True)

target = 'objectives/command-and-control/backdoor/webshell/stager::dotnet-page-http-shellcode-stager'
sample = Path(sys.argv[2])
assert target in scan(sample)
data = sample.read_bytes()
# Break execution transfer while retaining all the native API names and HTTP
# context. A diagnostic page with those references must not match the stager.
needle = bytes.fromhex('8b0701c385c075e558c3')
assert data.count(needle) == 1
path = DEST / 'no-stage-return.dll'
path.write_bytes(data.replace(needle, bytes.fromhex('8b0701c385c075e55890')))
assert target not in scan(path)
print('PASS native API names without stage activation', flush=True)
