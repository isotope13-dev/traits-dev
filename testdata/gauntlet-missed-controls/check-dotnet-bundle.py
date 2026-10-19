"""Static .NET bundle regressions; no generated or supplied specimen is run.

Synthetic hosts return immediately and have no managed entry point. Optional
real specimens stay external to this repository. All child identity checks
use content hashes, not a filename's asserted trust or company metadata.
"""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import struct
import subprocess
import tempfile
import zlib

parser = argparse.ArgumentParser()
parser.add_argument('--cleave', required=True)
parser.add_argument('--host', type=Path)
parser.add_argument('--jar', type=Path)
parser.add_argument('--application', type=Path)
parser.add_argument('--library', type=Path)
parser.add_argument('--reports', type=Path)
args = parser.parse_args()
repo = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('pe_controls', repo / 'testdata/managed-records-review/verify.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
signature = bytes.fromhex('8b1202b96a612038727b930214d7a03213f5b9e6efae3318ee3b2dce24b36aae')
partial = 'metadata/file/archive::partial-extraction'
recording = 'objectives/collection/keylog/polling::managed-polled-character-recording'
env = dict(os.environ, CLEAVE_NO_UPDATE_CHECK='1', XDG_CACHE_HOME='/tmp/gauntlet-cache',
           RAYON_NUM_THREADS='2')
retired = 'objectives/command-and-control/dropper/staging/temp::encoded-temp-command-stager'


def string(value):
    encoded = value.encode()
    length = len(encoded)
    prefix = bytearray()
    while length >= 128:
        prefix.append((length & 127) | 128)
        length >>= 7
    return bytes(prefix) + bytes([length]) + encoded


def bundle(version=6, compressed=True, names=('probe.py',), declared=None):
    host = module.build_pe([], b'')
    # Remove the synthetic CLR directory: a bundle host is a native PE.
    struct.pack_into('<II', host, 0x98 + 96 + 14 * 8, 0, 0)
    host[0x280:0x280 + 4] = b'none'
    marker = len(host)
    host += bytes(8) + signature
    entries = []
    for name in names:
        source = b"print('inert bundle control')\n"
        compressor = zlib.compressobj(wbits=-15)
        data = compressor.compress(source) + compressor.flush() if compressed else source
        entries.append((name, len(host), len(source), len(data) if compressed else 0))
        host += data
    header = len(host)
    struct.pack_into('<Q', host, marker, header)
    host += struct.pack('<III', version, 0, len(entries)) + string('control')
    if version >= 2:
        host += bytes(40)
    for name, offset, size, stored in entries:
        host += struct.pack('<QQ', offset, size if declared is None else declared)
        if version >= 6:
            host += struct.pack('<Q', stored)
        host += b'\x01' + string(name)
    return host


def analyze(path, label, memory=100):
    run = subprocess.run([args.cleave, '--traits-dir', str(repo), '--max-file-mem', str(memory),
                          '--format=json', 'analyze', str(path)], env=env,
                         capture_output=True, text=True, check=True, timeout=900)
    result = json.loads(run.stdout)
    assert not any(t['id'] == retired for f in result['files'] for t in f.get('traits', [])), label
    if args.reports:
        args.reports.mkdir(parents=True, exist_ok=True)
        (args.reports / (label + '.json')).write_text(run.stdout)
    return result['files']


def check_library():
    files = analyze(args.library, 'native-support-library')
    traits = {t['id']: t for f in files for t in f.get('traits', [])}
    # Test the concrete import, not its bare-OR union: output pruning can
    # omit the union once the retired objective no longer consumes it.
    required = {'metadata/file/encoded::large-base64-like-string',
                'micro-behaviors/fs/temp/directory::temp-file-staging-primitives',
                'micro-behaviors/fs/path/application/executable::cmd-exe-image-name',
                'micro-behaviors/process/create/spawn::create-process-w'}
    assert required <= traits.keys(), ('library', 'underlying observations retained')
    assert not any(t['crit'] >= 4 for t in traits.values()), 'Unbound references must not become a stager verdict'
    print('PASS native support library: observations retained, no stager assertion', flush=True)


# A library-only invocation is a focused rerun, without rebuilding all hosts.
if args.library and not (args.host or args.jar):
    check_library()
    raise SystemExit(0)

with tempfile.TemporaryDirectory(prefix='gauntlet-bundle-') as scratch:
    scratch = Path(scratch)
    for version, compressed in [(1, False), (2, False), (6, False), (6, True)]:
        label = f'v{version}-compressed-{compressed}'
        path = scratch / (label + '.exe')
        path.write_bytes(bundle(version, compressed))
        files = analyze(path, label)
        assert any(f['path'].endswith('probe.py') for f in files), label
        assert not any(t['crit'] >= 4 for f in files for t in f.get('traits', [])), label
        print('PASS', label, flush=True)
    for name, body in [('truncated-manifest', bundle()[:-1]),
                       ('oversized-member', bundle(declared=200 * 1024 * 1024)),
                       ('wrong-expanded-size', bundle(declared=3))]:
        path = scratch / (name + '.exe')
        path.write_bytes(body)
        files = analyze(path, name)
        assert any(t['id'] == partial for f in files for t in f.get('traits', [])), name
        assert not any(f['path'].endswith('probe.py') for f in files), name
        print('PASS', name, flush=True)
    path = scratch / 'duplicate.exe'
    path.write_bytes(bundle(names=('probe.py', 'PROBE.py')))
    files = analyze(path, 'duplicate-paths')
    children = [f for f in files if f['path'].lower().endswith(('.py'))]
    assert len(children) == 2 and len({f['path'].lower() for f in children}) == 2
    print('PASS duplicate paths retained separately', flush=True)
    path = scratch / 'unsafe.exe'
    path.write_bytes(bundle(names=('../escape.py', 'probe.py')))
    files = analyze(path, 'unsafe-path')
    assert any(f['path'].endswith('probe.py') for f in files)
    assert not any('escape.py' in f['path'] for f in files)
    print('PASS unsafe member rejected; sibling retained', flush=True)

if args.host or args.jar:
    assert args.application, '--application is required to verify real child identity'
    expected_sha = hashlib.sha256(args.application.read_bytes()).hexdigest()
    for label, sample in [('essential-native-host', args.host), ('essential-full-jar', args.jar)]:
        if sample is None:
            continue
        files = analyze(sample, label)
        children = [f for f in files if f.get('sha') == expected_sha]
        assert children, (label, 'application bytes must be recovered')
        assert any(any(t['id'] == recording for t in f.get('traits', [])) for f in children), (label, 'recording finding on actual child')
        assert any(any(t['id'] == recording for t in f.get('traits', [])) for f in files if f.get('id') == 0), (label, 'finding rollup')
        print('PASS', label, 'application hash, child finding and rollup', flush=True)

if args.library:
    check_library()
