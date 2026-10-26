#!/usr/bin/env python3
"""Boundary checks using mutations of the reviewed native specimen, never execution."""
import argparse
import json
import struct
import subprocess
from pathlib import Path
import pefile

p = argparse.ArgumentParser()
p.add_argument('--sample', type=Path, required=True)
p.add_argument('--scratch', type=Path, required=True)
a = p.parse_args()
a.scratch.mkdir(parents=True, exist_ok=True)
data = a.sample.read_bytes()
pe = pefile.PE(data=data)

def off(va):
    return pe.get_offset_from_rva(va - pe.OPTIONAL_HEADER.ImageBase)

def encode(text, multiplier, seed, wide=False):
    out = bytearray()
    for j, ch in enumerate(text + '\0'):
        byte = ord(ch) ^ ((j * multiplier + seed) & 255)
        shift = j % 7 + 1
        byte = ((byte << shift) | (byte >> (8 - shift))) & 255
        out += bytes([byte, 0]) if wide else bytes([byte])
    return out

H_AMSI = 'objectives/evasion/anti-av/blinding::concealed-amsi-session-local-patch'
H_TASK = 'objectives/persistence/system/scheduled-task::concealed-boot-task-with-amsi-tampering'
H_UAC = 'objectives/privilege-escalation/elevation-control/uac-bypass/com::concealed-api-cmstplua-uac-bypass'
H_INJECT = 'objectives/evasion/process/injection/runtime::hidden-api-remote-write-loader'
H_MASK = 'objectives/evasion/masquerade/version-resource/microsoft-utility::unsigned-system-config-impersonator-with-hostile-loader'
N_COPY = 'micro-behaviors/mem/write/arbitrary::x64-xor-rax-bytes-to-stack-buffer'
N_WRITE = 'micro-behaviors/mem/write/arbitrary::x64-iat-current-process-write-call'
S_VM = 'objectives/anti-analysis/vm-detect/instruction::x64-cpuid-hypervisor-bit-vendor-gate'
N_BOOT = 'micro-behaviors/os/autorun/task-trigger::rotate-xor-boot-trigger-name'
N_AMSI = 'micro-behaviors/os/security/amsi::rotate-xor-open-session-name'
N_REG = 'micro-behaviors/os/autorun/control::x64-scheduler-boot-service-account-profile'
N_ARITH = 'metadata/binary/instruction/sequence::x64-multiply-shift-xor-branch'
N_HASH = 'micro-behaviors/os/api-resolution/hash-based::multiplicative-export-mixing-profile-x64'

cases = []
def case(name, content, yes=(), no=()):
    path = a.scratch / name
    path.write_bytes(content)
    cases.append((path, set(yes), set(no)))

case('renamed.exe', data, [H_AMSI, H_TASK, H_UAC, H_MASK, S_VM, N_ARITH], [N_HASH])
case('sihost.exe', data, [H_MASK, H_AMSI, H_TASK], [N_HASH])
# Re-encode every string these new detectors need, changing both key parameters.
mut = bytearray(data)
k = data.index(bytes.fromhex('0f b6 c0 6b c0 0d 05 b1 00 00 00 25 ff 00 00 00'))
mut[k + 5] = 17
struct.pack_into('<I', mut, k + 7, 0x5a)
for va, text, wide in [
    (0x1400b6acc, 'AmsiOpenSession', False),
    (0x1400b7a3a, 'CoGetObject', False),
    (0x1400b6b20, 'BootTrigger', True),
]:
    encoded = encode(text, 17, 0x5a, wide)
    mut[off(va):off(va) + len(encoded)] = encoded
case('different-key.exe', mut, [H_AMSI, H_TASK, H_UAC], [N_HASH])
mut = bytearray(data)
mut[off(0x1400b6acc)] ^= 2
case('different-resolved-target.exe', mut, [N_WRITE, N_COPY, H_UAC], [N_AMSI, H_AMSI, H_TASK, H_INJECT])
mut = bytearray(data)
mut[off(0x1400b6b20)] ^= 2
case('renamed-boot-trigger-id.exe', mut, [H_AMSI, N_REG, H_TASK], [N_BOOT])
mut = bytearray(data)
mut[off(0x1400791d5) + 1] = 9
case('different-trigger-kind.exe', mut, [H_AMSI, N_BOOT], [N_REG, H_TASK])
# Break the GetCurrentProcess function-pointer slot binding, retaining imports.
mut = bytearray(data)
mut[off(0x140070843) + 14] ^= 8
case('different-handle-call-slot.exe', mut, [N_AMSI, N_COPY, H_UAC], [N_WRITE, H_AMSI, H_TASK])
# Patch construction without the hostile XOR-RAX instruction bytes is not this patch.
mut = bytearray(data)
copy = off(0x14006cae0)
source_rva = 0x6cae0 + 7 + struct.unpack_from('<i', data, copy + 3)[0]
mut[pe.get_offset_from_rva(source_rva)] = 0x90
case('ordinary-patch-buffer.exe', mut, [N_AMSI, N_WRITE, H_UAC], [N_COPY, H_AMSI, H_TASK])
mut = bytearray(data)
for va in [0x14007cb0f, 0x140087f23]:
    mut[off(va) + 2] = 0x80
case('different-com-method.exe', mut, [H_AMSI, N_BOOT], [N_REG, H_TASK])
mut = bytearray(data)
# The original bit-31 gate survives without a hypervisor vendor-leaf query.
mut[off(0x140003206) + 4] = 0
case('ordinary-cpuid-leaf.exe', mut, [H_AMSI, H_TASK], [S_VM])

result = subprocess.run(['cleave', '--format', 'json', *[str(x[0]) for x in cases]], capture_output=True, text=True)
if result.returncode:
    raise SystemExit(result.stderr)
s = result.stdout
reports = []
decoder = json.JSONDecoder()
while s.strip():
    report, length = decoder.raw_decode(s.lstrip())
    s = s.lstrip()[length:]
    reports.extend(report['files'])
by_path = {x['path']: {t['id'] for t in x.get('traits', [])} for x in reports}
summary = []
for path, yes, no in cases:
    found = by_path[str(path)]
    missing, extra = yes - found, no & found
    assert not missing and not extra, (path.name, sorted(missing), sorted(extra))
    summary.append({'case': path.name, 'required_present': sorted(yes), 'required_absent': sorted(no)})
print(json.dumps(summary, indent=2))
