#!/usr/bin/env python3
"""Generate data-only mutation controls; scan without executing Java content."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument('sample', type=Path)
parser.add_argument('--work-dir', type=Path, required=True)
parser.add_argument('--cleave', default='cleave')
args = parser.parse_args()
root = Path(__file__).resolve().parents[3]
expected = json.loads(Path(__file__).with_name('controls.json').read_text())
source = args.sample.read_bytes()
assert hashlib.sha256(source).hexdigest() == expected['source_sha256']
start = source.index(b'<%@')
end = source.index(b'\nsr\x00', start) + 1
jsp = source[start:end]
cases = {
    'renamed.ser': source,
    'renamed-payload.ser': source.replace(b'TDG9XQ4L2W7', b'RENAMED1234'),
    'missing-aspectj.ser': source.replace(
        b'SimpleCache$StoreableCachingMap', b'SimpleCache$StoreableCachingMaq'),
    'missing-hashset.ser': source.replace(b'java.util.HashSet', b'java.util.HashSeq'),
    'wrong-classdesc.ser': source.replace(
        b'\x72\x00\x35org.apache', b'\x74\x00\x35org.apache'),
    'ordinary.jsp': jsp,
    'graph-only.ser': source[:start] + b'<%@ page contentType="text/plain" %><% %>' + b' ' * (len(jsp) - 41) + source[end:],
    'no-shell.ser': source.replace(b'/bin/sh', b'/bin/zz'),
    'prose.jsp': jsp + b'\n' + b'\n'.join((
        b'org.apache.commons.collections4.keyvalue.TiedMapEntry',
        b'org.apache.commons.collections4.map.LazyMap',
        b'org.apache.commons.collections4.functors.ConstantTransformer',
        b'org.aspectj.weaver.tools.cache.SimpleCache$StoreableCachingMap')),
}
assert cases.keys() == expected['expected'].keys()
args.work_dir.mkdir(parents=True, exist_ok=True)
with tempfile.TemporaryDirectory(prefix='java-gadget-controls-', dir=args.work_dir) as temp:
    for name, content in cases.items():
        (Path(temp) / name).write_bytes(content)
    result = subprocess.run([
        args.cleave, '--traits-dir', str(root), '--all-files', '--format', 'json', temp
    ], check=True, capture_output=True, text=True)
    assert not result.stderr.strip(), result.stderr
    # Directory analysis emits concatenated JSON report objects.
    remaining = result.stdout
    decoder = json.JSONDecoder()
    files = []
    while remaining.strip():
        remaining = remaining.lstrip()
        report, length = decoder.raw_decode(remaining)
        remaining = remaining[length:]
        files.extend(report['files'])
    assert len(files) == len(cases), len(files)
    for file in files:
        name = Path(file['path']).name
        high = sorted(t['id'] for t in file.get('traits', []) if t['crit'] >= 4)
        assert high == sorted(expected['expected'][name]), (name, high)
        print(name + ': PASS')
print(str(len(cases)) + ' controls passed')
