"""Static regression controls; never loads or executes specimen code.

Usage: python3 check.py GANDCRAB_SAMPLE SCRATCH_DIRECTORY
"""
import json
import importlib.util
import os
from pathlib import Path
import struct
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
CAP = 'objectives/impact/ransom/encrypt/capi::capi-rsaenh-file-encryptor'
REC = 'objectives/impact/ransom/recovery-inhibition::native-ransomware-stack-shadow-removal'
WM = 'objectives/impact/ransom/recovery-inhibition::x86-stack-shadowcopy-delete-command'
VSS = 'objectives/impact/ransom/recovery-inhibition::x86-stack-vssadmin-delete-shadows-command'
CRASH = 'well-known/lib/development/breakpad-legacy::crashpad-client-section'
REMOTE = 'micro-behaviors/process/inject/remote-thread::remote-thread-memory-api-profile'
SECURITY_A = 'micro-behaviors/process/terminate/kill::security-name-enumeration-termination-api-profile'
SECURITY_B = 'micro-behaviors/process/terminate/kill::security-name-toolhelp-termination-api-profile'
TIMEOUT = 'micro-behaviors/fs/delete/file/command::timeout-delayed-file-delete-command'
GEN = 'micro-behaviors/crypto/key/generate::crypt-gen-key'
EXPORT = 'micro-behaviors/crypto/key/export::crypt-export-key'
ALLOC = 'micro-behaviors/mem/alloc/executable::executable-allocation-cmd-name-profile'
OLD_BACKDOOR = 'objectives/command-and-control/backdoor/binary::unsigned-virtual-alloc-cmd'


def main():
    sample, scratch = map(Path, sys.argv[1:3])
    work = scratch / 'focused-controls'
    work.mkdir(parents=True, exist_ok=True)
    for stale in ['no-http-send.exe', 'no-user-field.exe']:
        (work / stale).unlink(missing_ok=True)
    original = sample.read_bytes()
    fixture = (ROOT / 'testdata/benign/crashpad-client-injection-controls.exe').read_bytes()
    # The old positive is a 716-byte import fixture whose CPADinfo raw-data
    # pointer is beyond EOF. It supplies no CrashpadInfo object.
    expected = {}

    def add(name, blob, checks):
        (work / name).write_bytes(blob)
        expected[name] = checks

    add('gand-original.exe', original, {CAP: True, WM: True, VSS: True, REC: True,
                                     CRASH: False, TIMEOUT: True,
                                     GEN: True, EXPORT: True, ALLOC: True, OLD_BACKDOOR: False,
                                     SECURITY_A: True, SECURITY_B: True})
    add('label-only.exe', fixture, {CRASH: False, REMOTE: True, REC: False})
    header = bytearray(fixture)
    header.extend(bytes(1536-len(header)))
    pe = struct.unpack_from('<I', header, 60)[0]
    sections = pe+24+struct.unpack_from('<H', header, pe+20)[0]
    second = sections+40
    struct.pack_into('<I', header, second+8, 40)
    struct.pack_into('<II', header, second+16, 512, 1024)
    struct.pack_into('<III', header, 1024, 0x43506164, 40, 1)
    add('crashpad-v1.exe', header, {CRASH: True, REMOTE: True, REC: False})
    wide = bytearray(header)
    struct.pack_into('<I', wide, 1028, 56)
    add('crashpad-v1-size56.exe', wide, {CRASH: True, REMOTE: True})
    wrong = bytearray(header)
    struct.pack_into('<I', wrong, 1032, 2)
    add('wrong-version.exe', wrong, {CRASH: False, REMOTE: True})
    wrong = bytearray(header)
    wrong[1024:1028] = b'XXXX'
    add('wrong-magic.exe', wrong, {CRASH: False, REMOTE: True})
    # Mutate each real command at its immediate stores, leaving all other
    # ransomware code and family signatures in place.
    # Convert a shadowcopy "sh" store into "qu". VA 0x10004613 maps to 0x3a13.
    no_wm = bytearray(original)
    assert original[0x3a13:0x3a17] == bytes.fromhex('c7442444')
    no_wm[0x3a17:0x3a1b] = 'qu'.encode('utf-16le')
    add('no-wmic-delete.exe', no_wm, {WM: False, VSS: True, REC: True, CAP: True})
    no_vss = bytearray(original)
    assert original[0x3ab1:0x3ab5] == bytes.fromhex('c7442474')
    no_vss[0x3ab5:0x3ab9] = 'xx'.encode('utf-16le')
    add('no-vssadmin-delete.exe', no_vss, {WM: True, VSS: False, REC: True, CAP: True})
    both = bytearray(no_wm)
    both[0x3ab5:0x3ab9] = 'xx'.encode('utf-16le')
    add('no-shadow-removal.exe', both, {WM: False, VSS: False, REC: False, CAP: True})
    no_crypto = original.replace(b'CryptEncrypt\0', b'XryptEncrypt\0')
    add('no-encryption-api.exe', no_crypto, {CAP: False, REC: False,
                                           WM: True, VSS: True})
    no_gen = original.replace(b'CryptGenKey\0', b'XryptGenKey\0')
    add('no-keygen.exe', no_gen, {GEN: False, EXPORT: True, CAP: True})
    no_export = original.replace(b'CryptExportKey\0', b'XryptExportKey\0')
    add('no-key-export.exe', no_export, {EXPORT: False, GEN: True, CAP: True})
    # Reuse the repository's inert PE builder to prove that executable-memory
    # and cmd.exe references alone remain neutral. Entry points return first.
    spec = importlib.util.spec_from_file_location(
        'gui_controls', ROOT / 'testdata/taxonomy/windows-gui-intent-boundaries/run.py')
    builder = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(builder)
    alloc_code = bytes.fromhex('6a40680030000068000400006a00ff1500204000')
    for name, imports, strings, code, present in [
        ('local-jit-command-references.exe', {'KERNEL32.dll': ['VirtualAlloc']},
         ['cmd.exe'], alloc_code, True),
        ('local-allocation-no-command.exe', {'KERNEL32.dll': ['VirtualAlloc']},
         ['other.exe'], alloc_code, False),
        ('command-name-no-allocation.exe', {'KERNEL32.dll': ['CloseHandle']},
         ['cmd.exe'], b'', False),
    ]:
        add(name, builder.pe(imports, strings, code),
            {ALLOC: present, OLD_BACKDOOR: False, REC: False})
    result = subprocess.run([os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
                             '--json', str(work)], capture_output=True, text=True)
    (scratch / 'focused.after.jsonl').write_text(result.stdout)
    (scratch / 'focused.after.log').write_text(result.stderr)
    assert result.stdout.strip(), result.stderr
    seen = set()
    for line in result.stdout.splitlines():
        for entry in json.loads(line)['files']:
            name = Path(entry['path']).name
            if name not in expected:
                continue
            traits = {t['id']: t for t in entry.get('traits', [])}
            for trait, present in expected[name].items():
                assert (trait in traits) == present, (name, trait, present)
            if name == 'local-jit-command-references.exe':
                assert traits[ALLOC]['crit'] == 3
                assert not [t for t in traits.values() if t['crit'] == 5], name
            # Library identity cannot erase an accurate remote API capability.
            if name.startswith('crashpad-'):
                assert traits[REMOTE]['crit'] == 3, name
            seen.add(name)
    assert seen == set(expected), (seen, set(expected))
    print(f'PASS: {len(seen)} static identity, recovery and crypto controls')


if __name__ == '__main__':
    main()
