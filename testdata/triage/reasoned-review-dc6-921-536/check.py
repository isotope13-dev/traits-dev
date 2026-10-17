#!/usr/bin/env python3
"""Focused semantic controls; generates inert PE/source fixtures, executes none."""
import argparse
import json
import os
from pathlib import Path
import struct
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
BOOT = 'objectives/persistence/firmware/boot/record::embedded-bios-read-hook-bootkit'
VECTOR = 'micro-behaviors/os/msdos/interrupt::embedded-int13-vector-replacement'
PATCH = 'micro-behaviors/mem/write/arbitrary::embedded-bios-buffer-far-call-patch'
ARGV = 'micro-behaviors/process/create/shell/native::shell-c-caller-argv-reference'
ROOTREQ = 'micro-behaviors/process/identity/setuid::native-all-root-setresuid-reference'
PAIR = 'micro-behaviors/process/identity/setuid::root-setresuid-group-or-procfs-references'
IOV = 'micro-behaviors/data/buffer/record::iovec-buffer-address-as-length'
HEX = 'metadata/binary/resource/identity::delimited-hex-key-resource-fields'
FLAGS = 'metadata/binary/resource/identity::delimited-executable-two-one-fields'
RUNPE = 'objectives/execution/payload/process-inject::autoit-serialized-framework-runpe'
STARTUP = 'objectives/persistence/login/registry/run-key::autoit-runpe-hidden-startup-config'
VECTOR_BYTES = bytes.fromhex('66 8B 47 4C 67 66 26 A3 B2 00 00 00 C7 47 4C A7 00 8C 47 4E')
PATCH_BYTES = bytes.fromhex('26 C7 05 66 9A 66 33 C0 8C C8 66 C1 E0 04 66 05 04 02 00 00 66 26 89 45 02 26 C7 45 06 20 00')


def pe_data(payload, section=b'.data'):
    """Minimal inert x86 PE with one writable data section, no entry point."""
    b = bytearray(0x400)
    b[:2] = b'MZ'
    struct.pack_into('<I', b, 0x3c, 0x80)
    b[0x80:0x84] = b'PE\0\0'
    struct.pack_into('<HHIIIHH', b, 0x84, 0x14c, 1, 0, 0, 0, 0xe0, 0x102)
    o = 0x98
    struct.pack_into('<H', b, o, 0x10b)
    struct.pack_into('<I', b, o + 28, 0x400000)
    struct.pack_into('<II', b, o + 32, 0x1000, 0x200)
    struct.pack_into('<II', b, o + 56, 0x2000, 0x200)
    struct.pack_into('<H', b, o + 68, 2)
    struct.pack_into('<I', b, o + 92, 16)
    s = o + 0xe0
    b[s:s+8] = section.ljust(8, b'\0')
    struct.pack_into('<IIII', b, s + 8, 0x200, 0x1000, 0x200, 0x200)
    struct.pack_into('<I', b, s + 36, 0xc0000040)
    assert len(payload) <= 512
    b[512:512+len(payload)] = payload
    return bytes(b)


def scan(binary, path):
    r = subprocess.run([binary, '--traits-dir', str(ROOT), '--format', 'json', str(path)],
                       capture_output=True, text=True, env={**os.environ, 'CLEAVE_VALIDATE': '1'})
    if r.returncode:
        raise AssertionError(r.stderr)
    assert not any(x in r.stderr.lower() for x in ['warning:', 'validation failed']), r.stderr
    obj = json.loads(r.stdout)
    files = obj['files']
    return {t['id']: t.get('criticality', t.get('crit'))
            for f in files for t in f.get('findings', f.get('traits', []))}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cleave', default='cleave')
    parser.add_argument('--autoit', type=Path, help='optional original 92132990d4d0 sample')
    args = parser.parse_args()
    cases = []
    both = VECTOR_BYTES + b'\x90' * 64 + PATCH_BYTES
    cases += [('boot-pair.exe', pe_data(both), {BOOT, VECTOR, PATCH}, set()),
              ('vector-only.exe', pe_data(VECTOR_BYTES), {VECTOR}, {BOOT, PATCH}),
              ('patch-only.exe', pe_data(PATCH_BYTES), {PATCH}, {BOOT, VECTOR}),
              ('changed-ivt-slot.exe', pe_data(both.replace(b'\x47\x4c', b'\x47\x48')), {PATCH}, {BOOT, VECTOR}),
              ('changed-call-opcode.exe', pe_data(both.replace(b'\x66\x9a', b'\x66\x90')), {VECTOR}, {BOOT, PATCH})]
    cases += [('shell-argv.c', b'int f(char **argv){return execl("/bin/sh","sh","-p","-c",argv[1],0);}', {ARGV}, set()),
              ('compiler-argv.c', b'int f(char **argv){return execl("/usr/bin/cc","cc","-c",argv[1],0);}', set(), {ARGV}),
              ('argv-array.c', b'int f(char **argv){char *v[]={"-c",argv[1]};return 0;}', set(), {ARGV}),
              ('root-identity.c', b'int f(){setresuid(0,0,0);setresgid(0,0,0);return 0;}', {ROOTREQ, PAIR}, set()),
              ('iovec-address.c', b'void f(){v[0].iov_base=(void *)(uintptr_t)address;v[0].iov_len=(size_t)address;}', {IOV}, set()),
              ('iovec-size.c', b'void f(){v[0].iov_base=(void *)(uintptr_t)address;v[0].iov_len=(size_t)length;}', set(), {IOV})]
    for separator in ['NetsealIsTheBestLicensingSystemEverCreated', 'AlternativeDelimiter']:
        d = ('@' + separator + '@').encode()
        # Use the original AutoIt optional controls for full configuration.
        # A short stand-alone flags fixture
        # verifies that flags without the executable field do not match.
        cases += [(separator + '-flags.exe', pe_data(b'cvtres.exe' + d + b'2' + d + b'1' + d, b'.rsrc'), {FLAGS}, {RUNPE, STARTUP}),
                  (separator + '-bare-flags.exe', pe_data(d + b'2' + d + b'1' + d, b'.rsrc'), set(), {FLAGS, RUNPE, STARTUP})]
    if args.autoit:
        data = args.autoit.read_bytes()
        label = b'NetsealIsTheBestLicensingSystemEverCreated'
        cases += [('renamed-autoit.exe', data.replace(label, b'R' * len(label)), {HEX, FLAGS, RUNPE, STARTUP}, set()),
                  ('startup-disabled.exe', data.replace(b'@2@' + label + b'@1@', b'@0@' + label + b'@1@'), {HEX, RUNPE}, {FLAGS, STARTUP}),
                  ('no-editor-claim.exe', data.replace('SciTE'.encode('utf-16le'), 'Other'.encode('utf-16le')), {HEX, FLAGS}, {RUNPE, STARTUP})]
    with tempfile.TemporaryDirectory(prefix='trait-review-', dir=ROOT) as tmp:
        for name, data, yes, no in cases:
            path = Path(tmp) / name
            path.write_bytes(data)
            got = scan(args.cleave, path)
            assert yes <= got.keys(), (name, 'missing', yes - got.keys())
            assert not no & got.keys(), (name, 'unexpected', no & got.keys())
            if name == 'root-identity.c':
                assert got[ROOTREQ] in ['notable', 3] and got[PAIR] in ['notable', 3], got
            print('PASS', name)
    print(f'{len(cases)} focused controls passed')


if __name__ == '__main__':
    main()
