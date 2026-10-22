"""Mutate operands in the supplied PE; never execute samples or generated PEs."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import struct
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('sample', type=Path)
parser.add_argument('scratch', type=Path)
args = parser.parse_args()
args.scratch.mkdir(parents=True, exist_ok=True)
original = args.sample.read_bytes()
assert hashlib.sha256(original).hexdigest() == '0d0f5689f2233e3ced73a0706207def5f192ad64cd4a082c0023060631e27c63'
# The reviewed PE uses distinct RVA-to-file deltas for .text and .rdata.
def operand(data, rva, old, new):
    offset = rva - (0xa00 if rva < 0x109000 else 0xc00)
    assert data[offset:offset + len(old)] == old, (hex(rva), old.hex(), data[offset:offset + len(old)].hex())
    data[offset:offset + len(old)] = new

task_atom = 'micro-behaviors/process/argument/option::go-x64-schtasks-hourly-command-setup'
startup_atom = 'micro-behaviors/fs/path/autostart::go-x64-startup-path-component-array'
policy_atom = 'micro-behaviors/process/argument/option::go-executionpolicy-bypass-argument-pair'
task = 'objectives/persistence/system/scheduled-task::go-clipboard-clipper-repeating-task'
startup = 'objectives/persistence/login/startup/shortcut::go-clipboard-clipper-startup-shortcut'
clipper = 'objectives/impact/crypto-manipulation/clipboard::go-ethereum-clipboard-swap'
cases = [(args.sample, {task_atom, startup_atom, policy_atom, task, startup, clipper}, set())]
for name, rva, old, new, absent in [
    ('different-command', 0x14524e, b'schtasks', b'notasksx', {task_atom, task}),
    ('delete-action', 0x144f68, b'/create', b'/delete', {task_atom, task}),
    ('different-schedule', 0x144cd6, b'hourly', b'manual', {task_atom, task}),
    # All strings remain; change the RIP-relative operand to a different word.
    ('different-startup-operand', 0xf7a1e, original[0xf701e:0xf7022],
     struct.pack('<i', 0x144f6f - (0xf7a1b + 7)), {startup_atom, startup}),
    ('different-policy-operand', 0xf7bbd, original[0xf71bd:0xf71c1],
     struct.pack('<i', 0x144ce2 - (0xf7bba + 7)), {policy_atom}),
    ('different-array-slot', 0xf7a13, b'\x00\x01\x00\x00', b'\x08\x01\x00\x00', {startup_atom, startup}),
]:
    data = bytearray(original)
    operand(data, rva, old, new)
    dest = args.scratch / (name + '.exe')
    dest.write_bytes(data)
    cases.append((dest, {clipper}, absent))
root = Path(__file__).resolve().parents[3]
run = subprocess.run([os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(root),
                      '--format', 'jsonl', 'analyze', *[str(c[0]) for c in cases]],
                     capture_output=True, text=True)
if run.returncode:
    raise RuntimeError(run.stderr)
reports = {}
for line in run.stdout.splitlines():
    for report in json.loads(line).get('files', []):
        reports[Path(report['path']).resolve()] = {t['id'] for t in report.get('traits', [])}
for path, expected, absent in cases:
    actual = reports[path.resolve()]
    assert expected <= actual and not absent & actual, (path, expected - actual, absent & actual)
(args.scratch / 'binary-reports.jsonl').write_text(run.stdout)
print(f'Passed {len(cases)} original-PE and operand-boundary cases')
