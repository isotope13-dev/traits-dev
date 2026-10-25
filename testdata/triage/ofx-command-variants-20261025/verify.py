"""Static matcher controls. Never execute a specimen or contact its endpoints.

Usage: python3 verify.py SAMPLES_DIRECTORY SCRATCH_DIRECTORY [ORIGINAL_PE]
Mutations are derived controls, not recovered artifacts or runtime observations.
"""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
samples, output = map(Path, sys.argv[1:3])
output.mkdir(parents=True, exist_ok=True)
PIPE = 'micro-behaviors/communications/ipc/pipe::x64-compared-command-process-pipe-readback'
CAPTURE = 'micro-behaviors/hardware/display/screenshot::x64-compared-command-desktop-capture-handler'
FLAGS = 'objectives/anti-analysis/debugger-detect/check::peb-ntglobalflag-mask-check'
C2 = 'objectives/command-and-control/remote-command/tasking::discord-extortion-shell-tasking'
SCREEN = 'objectives/exfiltration/stealer/screen::discord-extortion-screen-upload'
UPLOAD = 'objectives/exfiltration/stealer/file::discord-extortion-file-upload-task'
TIMING = 'objectives/anti-analysis/sandbox-detect/timing::x64-uptime-cpu-shared-abort'
TRACKED = {PIPE, CAPTURE, FLAGS, C2, SCREEN, UPLOAD, TIMING}
specimens = [
    ('b6e35505eb79/different-resource-abort-destination.exe',
     'b6e35505eb79450758533cb188800cd89532786fce09b39c16ed1dbd8a6db115'),
    ('aaf11286add1/no-screen-task-verb.exe',
     'aaf11286add1391208a3a40181093c1d96e1b7951eebe783c977dbcce27c3dc8'),
    ('8da1a1a7e0a1/no-shell-task-verb.exe',
     '8da1a1a7e0a150746532be7b54abb775b057b0ce205adc4b639abb299b8072b9'),
]
cases = []
for index, (name, digest) in enumerate(specimens):
    path = samples / name
    assert hashlib.sha256(path.read_bytes()).hexdigest() == digest
    present = TRACKED - ({TIMING} if index == 0 else set())
    cases.append((path, present, TRACKED - present))

original = (samples / specimens[0][0]).read_bytes()
aliased = original.replace(b'!exec\0', b'!help\0').replace(b'!screen\0', b'!status\0')
assert len(aliased) == len(original)


def save(name, data, absent=(), present=None):
    path = output / (name + '.exe')
    path.write_bytes(data)
    absent = set(absent) | {TIMING}
    present = TRACKED - absent if present is None else set(present)
    cases.append((path, present, absent))


def alter(name, va, delta=1, absent=()):
    data = bytearray(aliased)
    data[va - 0x140000000 - 0xC00] ^= delta
    save(name, data, absent)


save('both-task-verbs-renamed', aliased)
# Decode the call operand and import thunks; a matching byte sequence elsewhere
# in .text must not replace a broken edge in the command's execution path.
for name, va in [
    ('pipe-other-callee', 0x14001443E),
    ('pipe-other-import', 0x1400123A2),
    ('process-other-import', 0x14001248F),
    ('read-other-import', 0x14001253F),
    ('read-other-handle', 0x140012539),
    ('pipe-unequal-skip-targets', 0x140014410),
]:
    alter(name, va, absent=() if name.startswith('read-') else {PIPE, C2, SCREEN, UPLOAD})
for name, va in [
    ('capture-other-callee', 0x14001455B),
    ('capture-other-width-import', 0x14000E601),
    ('capture-other-height-import', 0x14000E60F),
    ('capture-other-dc-import', 0x14000E62A),
    ('capture-other-blit-import', 0x14000E68F),
    ('capture-other-output-buffer', 0x140014559),
    ('capture-unequal-skip-targets', 0x140014546),
]:
    alter(name, va, absent={CAPTURE, SCREEN})
alter('different-debug-field', 0x140016D78, absent={FLAGS})
alter('different-debug-mask', 0x140016D7C, absent={FLAGS})
# Both ReadFile call sites can prove pipe readback. Breaking just one leaves
# the other valid; breaking both must remove the handler observation.
for name, addresses in [
    ('both-read-imports-changed', [0x14001253F, 0x1400125E8]),
    ('both-read-handles-changed', [0x140012539, 0x1400125E2]),
]:
    data = bytearray(aliased)
    for va in addresses:
        data[va - 0x140000000 - 0xC00] ^= 1
    save(name, data, {PIPE, C2, SCREEN, UPLOAD})
# Moving the creation and one read slot together preserves their relation.
data = bytearray(aliased)
for va in [0x14001239C, 0x140012539]:
    data[va - 0x140000000 - 0xC00] ^= 0x10
save('same-renamed-pipe-slot', data)
# Removing the extortion leg retains the two neutral handler observations.
data = aliased.replace(b'payment is confirmed', b'payment is optional!')
save('handler-without-ransom-text', data, {C2, SCREEN, UPLOAD})
# Preserve each previously admitted NtGlobalFlag form, including 32-bit code.
old_patterns = [
    '64 A1 30 00 00 00 F7 40 68 70 00 00 00 74',
    '64 A1 30 00 00 00 F7 40 68 70 00 00 00 75',
    '64 A1 30 00 00 00 F7 40 68 70 00 00 00 0F 84',
    '64 A1 30 00 00 00 F7 40 68 70 00 00 00 0F 85',
    '65 48 8B 04 25 60 00 00 00 8B 88 BC 00 00 00 80 E1 70 F6 D9 1B FF 83 E7 02',
]
for index, pattern in enumerate(old_patterns):
    data = bytearray(aliased)
    data[0x16163:0x16183] = b'\x90' * 32
    code = bytes.fromhex(pattern)
    data[0x16163:0x16163 + len(code)] = code
    save('retained-debug-form-' + str(index), data)
for name in ['tor-0.4.7.15.exe', 'csharp-independent-pipes.exe',
             'managed-native-interop-only.exe', 'ffplay-media-controls/ffplay.exe']:
    path = ROOT / 'testdata/benign' / name
    assert path.exists(), path
    cases.append((path, set(), TRACKED))

if len(sys.argv) == 4:
    recovered = Path(sys.argv[3])
    assert hashlib.sha256(recovered.read_bytes()).hexdigest() == '5ca11fb0605c517cc6c4943d746956dc7023f1366b1a13c83033dfb3424cf3cf'
    cases.append((recovered, TRACKED, set()))

result = subprocess.run(
    [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
     '--disable', 'radare2', '--format', 'json', *[str(p) for p, _, _ in cases]],
    text=True, capture_output=True, check=True,
)
(output / 'reports.json').write_text(result.stdout)
(output / 'reports.log').write_text(result.stderr)
decoder = json.JSONDecoder()
remaining, files = result.stdout.strip(), {}
while remaining:
    report, end = decoder.raw_decode(remaining)
    files.update((f['path'], f) for f in report['files'])
    remaining = remaining[end:].strip()
checks = []
for path, present, absent in cases:
    actual = {t['id'] for t in files[str(path)].get('traits', [])}
    checks.append({'name': path.name, 'missing': sorted(present - actual),
                   'unexpected': sorted(absent & actual)})
(output / 'checks.json').write_text(json.dumps(checks, indent=2) + '\n')
assert not [c for c in checks if c['missing'] or c['unexpected']], checks
print(f'Passed {len(checks)} static specimen and boundary controls.')
