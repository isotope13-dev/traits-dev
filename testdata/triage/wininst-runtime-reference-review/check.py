"""Check exact coverage preservation for the split Python runtime references.

Optional argument: pre-change traits directory. Fixtures are inert PE files;
none of the fixture bytes or analyzed programs are executed.
"""
import json
from pathlib import Path
import struct
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[3]
OLD = 'metadata/binary/debug::cpython-wininst-python-marker'
DLL = 'micro-behaviors/fs/path/library::python-versioned-dll-template'
ERROR = 'micro-behaviors/ui/dialog/error::python-installation-registry-missing'


def pe(payload, section=b'.data'):
    data = bytearray(1536)
    data[:2] = b'MZ'
    struct.pack_into('<I', data, 0x3c, 128)
    data[128:132] = b'PE\0\0'
    struct.pack_into('<HHIIIHH', data, 132, 0x14c, 2, 1107463063, 0, 0, 224, 0x102)
    optional = 152
    struct.pack_into('<H', data, optional, 0x10b)
    struct.pack_into('<I', data, optional + 16, 0x1000)
    struct.pack_into('<I', data, optional + 28, 0x400000)
    struct.pack_into('<II', data, optional + 32, 4096, 512)
    struct.pack_into('<II', data, optional + 56, 0x3000, 512)
    struct.pack_into('<H', data, optional + 68, 2)
    struct.pack_into('<I', data, optional + 92, 16)
    for i, (name, rva, offset, flags) in enumerate([
        (b'.text', 0x1000, 512, 0x60000020),
        (section, 0x2000, 1024, 0xc0000040),
    ]):
        header = optional + 224 + i * 40
        data[header:header + len(name)] = name
        struct.pack_into('<IIII', data, header + 8, 512, rva, 512, offset)
        struct.pack_into('<I', data, header + 36, flags)
    data[512] = 0xc3  # RET: no fixture is executed.
    data[1024:1024 + len(payload)] = payload
    return data


def scan(path, traits):
    result = subprocess.run(['cleave', '--traits-dir', str(traits), '--format', 'json', str(path)],
                            capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(result.stderr)
    report = json.loads(result.stdout)
    return {t['id']: t['crit'] for f in report['files'] for t in f.get('traits', [])}


cases = [
    ('dll', b'python%d%d.dll\0', b'.data', {DLL}),
    ('error', b'No Python installation found in the registry\0', b'.data', {ERROR}),
    ('both', b'python%d%d.dll\0No Python installation found in the registry\0', b'.data', {DLL, ERROR}),
    ('case', b'PYTHON%d%d.DLL\0NO PYTHON INSTALLATION FOUND IN THE REGISTRY\0', b'.data', {DLL, ERROR}),
    ('other-library', b'python25.dll\0', b'.data', set()),
    ('other-message', b'No Ruby installation found in the registry\0', b'.data', set()),
    ('wrong-section', b'python%d%d.dll\0No Python installation found in the registry\0', b'.rsrc', set()),
]
results = []
with tempfile.TemporaryDirectory(prefix='wininst-reference-') as temporary:
    for name, payload, section, expected in cases:
        path = Path(temporary) / (name + '.exe')
        path.write_bytes(pe(payload, section))
        current = scan(path, ROOT)
        assert {DLL, ERROR} & current.keys() == expected, (name, current)
        assert OLD not in current, name
        if len(sys.argv) > 1:
            before = scan(path, Path(sys.argv[1]))
            assert (OLD in before) == bool(expected), (name, before)
            assert {k: v for k, v in before.items() if v >= 4} == {
                k: v for k, v in current.items() if v >= 4}, name
        results.append({'case': name, 'observations': sorted(expected)})
print(json.dumps(results, indent=2))
