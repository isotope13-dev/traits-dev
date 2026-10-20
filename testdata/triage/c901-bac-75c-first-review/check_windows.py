#!/usr/bin/env python3
"""Check that ServiceDLL replacement requires code and APIs, not a DLL name."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument('samples', type=Path, nargs=2)
parser.add_argument('--work-dir', type=Path, required=True)
parser.add_argument('--cleave', default='cleave')
args = parser.parse_args()
root = Path(__file__).resolve().parents[3]
expected_hashes = {
    'bac398da6239a2b5bee903d4644da77b88cf7aec47773e24d140f112b9ebc2e3',
    '75c3098ba531198c71272f32cc51f61429a4f3a7a4d7aa8e2c5c8c9e28aef98d',
}
objective = 'objectives/persistence/system/service/loader::lanmanserver-servicedll-replacement-injector'
cases = {}
for sample in args.samples:
    source = sample.read_bytes()
    sha = hashlib.sha256(source).hexdigest()
    assert sha in expected_hashes, sha
    renamed = source.replace(b'StormServer.dll', b'OtherServer.dll')
    no_delete = source.replace(b'RegDeleteValueA', b'RegDeleteValueZ')
    fragment_changed = bytearray(source)
    assert source[0x132e:0x1333] == b'\x68\x80\x00\x00\x00'
    fragment_changed[0x132f] = 0x81
    value_changed = bytearray(source)
    assert source[0x1339:0x133d] == b'\x34\x43\x40\x00'
    value_changed[0x1339] = 0x35
    for name, content, wanted in (
        ('renamed-dll', renamed, True),
        ('no-delete-api', no_delete, False),
        ('changed-call-setup', bytes(fragment_changed), False),
        ('mismatched-value-pointer', bytes(value_changed), False),
    ):
        cases[sha[:12] + '-' + name + '.exe'] = (content, wanted)
assert len(cases) == 8
args.work_dir.mkdir(parents=True, exist_ok=True)
with tempfile.TemporaryDirectory(prefix='servicedll-controls-', dir=args.work_dir) as temp:
    for name, (content, _) in cases.items():
        (Path(temp) / name).write_bytes(content)
    result = subprocess.run([
        args.cleave, '--traits-dir', str(root), '--all-files', '--format', 'json', temp
    ], check=True, capture_output=True, text=True)
    assert not result.stderr.strip(), result.stderr
    decoder = json.JSONDecoder()
    remaining = result.stdout
    seen = set()
    while remaining.strip():
        remaining = remaining.lstrip()
        report, length = decoder.raw_decode(remaining)
        remaining = remaining[length:]
        for file in report['files']:
            name = Path(file['path']).name
            if name not in cases or 'pid' in file:
                continue
            seen.add(name)
            found = any(t['id'] == objective for t in file.get('traits', []))
            assert found == cases[name][1], (name, found)
            print(name + ': PASS')
    assert seen == cases.keys(), seen
print('8 controls passed')
