"""Static PE controls and signed-carrier counterfactuals; never execute samples.
Usage: check.py <scratch-dir> <original-IconLib.dll>
"""
import ast
import json
import os
from pathlib import Path
import re
import struct
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
DEST, CARRIER = map(Path, sys.argv[1:])
DEST.mkdir(parents=True, exist_ok=True)
# Reuse the existing, reviewed inert two-section PE builder without running
# that module's command-line test runner.
module = ast.parse((ROOT / 'testdata/taxonomy/byte-transform-bounds/check.py').read_text())
namespace = {'struct': struct}
exec(compile(ast.Module(body=[n for n in module.body if isinstance(n, ast.FunctionDef) and n.name == 'image'], type_ignores=[]), '<fixture-builder>', 'exec'), namespace)
image = namespace['image']
A = 'micro-behaviors/data/arithmetic::x64-index-scaled-byte-subtraction-loop'
E = 'micro-behaviors/data/arithmetic::go-field-base-sum-call-setup'
R = 'micro-behaviors/mem/alloc/executable::go-abi-rwx-reserve-commit-call-x64'
D = 'objectives/anti-analysis/debugger-detect/check::peb-ntglobalflag-mask-check'
V = 'objectives/anti-analysis/vm-detect/instruction::x64-cpuid-hypervisor-bit-vendor-gate'
F = 'micro-behaviors/os/api-resolution/hash-based::x64-fnv64-export-name-hash-walk'
W = 'objectives/persistence/system/watchdog::hypervisor-check-with-server-watchdog-rearm'
C = 'metadata/signed/certificate/signature::autoit-container-after-signeddata'
H = 'objectives/evasion/masquerade/cert::ca-signed-autoit-certificate-padding'
I = 'objectives/evasion/process/injection/hollowing/process::autoit-suspended-image-replacement-source'
P = 'objectives/evasion/process/hook/inline::autoit-native-hotpatch-zero-return-source'
J = 'objectives/evasion/process/injection/hollowing/process::autoit-hollowing-with-native-hotpatch'
RULES = {A, E, R, D, V, F, W, C, H, I, P, J}
si = bytes.fromhex('0F B6 14 01 48 89 CE 48 C1 E6 05 48 29 CE 29 F2 83 C2 F2 88 14 08 48 FF C1 48 81 F9 00 00 01 00 7C DE')
rwx = bytes.fromhex('B9 00 30 00 00 BF 40 00 00 00 31 F6 45 31 C0 49 89 F1 4D 89 C2 45 31 DB 31 C0 E8 00 00 00 00')
entry = bytes.fromhex('8B 40 10') + b'\x90' * 320 + bytes.fromhex('48 8B 8C 24 10 00 00 00 48 01 C8') + b'\x90' * 270 + bytes.fromhex('48 89 84 24 20 00 00 00 48 8B 84 24 20 00 00 00 31 DB 31 C9 48 89 CF E8 00 00 00 00')
# The entry fixture needs larger mapped sections than the small builder.
def large_image(code):
    data = image(b'\xc3')
    data.extend(bytes(1536))
    struct.pack_into('<II', data, 0x190, 2048, 0x1000)
    struct.pack_into('<I', data, 0x198, 2048)
    struct.pack_into('<I', data, 0x1b0 + 20, 2560)
    data[512:512+len(code)] = code
    return data

debug = bytes.fromhex('65 48 8B 04 25 60 00 00 00 8B 88 BC 00 00 00 80 E1 70 F6 D9 1B FF 83 E7 02')
vm = bytes.fromhex('B8 01 00 00 00 33 C9 0F A2 89 44 24 30 89 5C 24 34 89 54 24 3C 85 C9 78 07 33 FF E9 00 00 00 00 B8 00 00 00 40 33 C9 0F A2')
fnv = bytes.fromhex('43 8B 14 83 48 B9 25 23 22 84 E4 9C F2 CB 49 03 D7 0F B6 02 84 C0 74 1D 90 0F B6 C0 48 8D 52 01 48 33 C8 0F B6 02 49 0F AF CD 84 C0 75 EB 48 33 CD 48 3B CE')
log = b'watchdog tier re-armed from server layout (reserve=\0'
cases = [
 ('si-transform', image(si), {A}),
 ('si-wrong-store', image(si.replace(bytes.fromhex('88 14 08'), bytes.fromhex('88 0C 08'))), set()),
 ('si-in-data', image(b'\xc3', si), set()),
 ('rwx-forwarded-registers', image(rwx), {R}),
 ('rw-allocation', image(rwx.replace(bytes.fromhex('BF 40'), bytes.fromhex('BF 04'))), set()),
 ('rwx-in-data', image(b'\xc3', rwx), set()),
 ('entry-junk-gaps', large_image(entry), {E}),
 ('entry-wrong-field', large_image(entry.replace(bytes.fromhex('8B 40 10'), bytes.fromhex('8B 40 14'))), set()),
 ('entry-no-call', large_image(entry[:-5]), set()),
 ('x64-heap-mask', image(debug), {D}),
 ('x64-other-mask', image(debug.replace(bytes.fromhex('E1 70'), bytes.fromhex('E1 01'))), set()),
 ('hypervisor-vendor-gate', image(vm), {V}),
 ('other-cpuid-leaf', image(vm.replace(bytes.fromhex('B8 00 00 00 40'), bytes.fromhex('B8 00 00 00 00'))), set()),
 ('vm-gate-in-data', image(b'\xc3', vm), set()),
 ('fnv64-export-walk', image(fnv), {F}),
 ('fnv64-in-data', image(b'\xc3', fnv), set()),
 ('vm-with-watchdog-rearm', image(vm, log), {V, W}),
 ('watchdog-alone', image(b'\xc3', log), set()),
]
# Preserve the original x86 mask-and-branch path after consolidating the
# equivalent x64 observation into its canonical trait.
x86 = image(bytes.fromhex('64 A1 30 00 00 00 F7 40 68 70 00 00 00 74 01'))
struct.pack_into('<H', x86, 0x84, 0x14c)
cases.append(('x86-heap-mask-retained', x86, {D}))
b = CARRIER.read_bytes()
nt = struct.unpack_from('<I', b, 0x3c)[0]
directory = nt + 24 + 96 + 32  # Original carrier is PE32.
cert, _ = struct.unpack_from('<II', b, directory)
end = (cert + 12 + int.from_bytes(b[cert+10:cert+12], 'big') + 7) & ~7
clean = bytearray(b[:end])
struct.pack_into('<I', clean, directory+4, end-cert)
struct.pack_into('<I', clean, cert, end-cert)
cases.extend([
 ('renamed-signed-container', b, {C, H}),
 ('signed-carrier-without-script', clean, set()),
 ('signed-carrier-unstructured-padding', clean + bytes(100000), set()),
])
hollow = b'\n'.join([
 b'If @error Then Return',
 b'$c("kernel32.dll", "bool", "CreateProcessW", "wstr", $p, "wstr", $a, "ptr", 0, "ptr", 0, "int", 0, "dword", 4, "ptr", 0)',
 b'$c("kernel32.dll", "bool", "GetThreadContext", "handle", $t)',
 b'$c("kernel32.dll", "ptr", "VirtualAllocEx", "handle", $p, "ptr", 0, "dword_ptr", $n, "dword", 12288, "dword", 64)',
 b'$c("ntdll.dll", "int", "NtUnmapViewOfSection", "ptr", $p)',
 b'$c("kernel32.dll", "bool", "SetThreadContext", "handle", $t)',
 b'$c("kernel32.dll", "dword", "ResumeThread", "handle", $t)',
])
patch = b'\n'.join([
 b'If @error Then Return',
 b'Local $stub[4] = [72, 49, 192, 195]',
 b'$fn = $c("kernel32.dll", "ptr", "GetProcAddress", "ptr", $mod, "str", "ZwManageHotPatch")',
 b'$c("kernel32.dll", "bool", "WriteProcessMemory", "handle", $p, "ptr", $fn[0] + $i, "ptr", $buf, "dword", 1, "ptr", 0)',
])
cases.extend([
 ('autoit-hollowing', hollow, {I}),
 ('autoit-not-suspended', hollow.replace(b'"dword", 4,', b'"dword", 0,'), set()),
 ('autoit-api-list', b'@error CreateProcessW GetThreadContext VirtualAllocEx NtUnmapViewOfSection SetThreadContext ResumeThread', set()),
 ('autoit-hotpatch', patch, {P}),
 ('autoit-no-stub', patch.replace(b'[72, 49, 192, 195]', b'[0, 0, 0, 0]'), set()),
 ('autoit-no-write', patch.replace(b'WriteProcessMemory', b'ReadProcessMemory'), set()),
 ('autoit-both', hollow + b'\n' + patch, {I, P, J}),
])
paths = []
for name, content, expected in cases:
    path = DEST / (name + ('.au3' if name.startswith('autoit-') else '.exe'))
    path.write_bytes(content)
    paths.append(path)
# Load the rule tree once; path-specific reports still evaluate independently.
result = subprocess.run([os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT), '--format', 'json', *map(str, paths)], capture_output=True, text=True)
assert result.returncode == 0, result.stderr
decoder = json.JSONDecoder()
remaining = result.stdout.strip()
files = []
while remaining:
    report, end = decoder.raw_decode(remaining)
    files.extend(report['files'])
    remaining = remaining[end:].lstrip()
for (name, _, expected), path in zip(cases, paths):
    matched_files = [f for f in files if f['path'] == str(path) or f['path'].startswith(str(path) + '!!')]
    assert matched_files, (name, 'no report returned')
    actual = {t['id'] for f in matched_files for t in f.get('traits', [])} & RULES
    assert actual == expected, (name, sorted(expected), sorted(actual), result.stderr)
    print('PASS ' + name, flush=True)
