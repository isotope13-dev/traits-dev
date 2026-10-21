#!/usr/bin/env python3
"""Exercise import-only false convictions and kernel I/O profile boundaries.

All PE derivatives are scanned as data; none is executed. Payload bytes stay
in the supplied scratch directory, outside the trait repository.
"""
import argparse
import json
from pathlib import Path
import struct
import subprocess

ROOT = Path(__file__).resolve().parents[3]
PROFILE = 'micro-behaviors/mem/write/arbitrary::unsigned-debug-api-remote-write-profile'
OLD = 'objectives/evasion/process/injection/runtime::unsigned-anti-debug-cross-process-write-loader'
DISK = 'micro-behaviors/fs/disk/raw::kernel-disk-irp-api-profile'
BUILD = 'micro-behaviors/fs/file/handle::io-build-asynchronous-fsd-request'
CALL = 'micro-behaviors/os/kernel/device::iof-call-driver'
NATIVE_WRITE = 'micro-behaviors/fs/write/file/handle::nt-write-file-import'
CREATE = 'micro-behaviors/os/registry/access::create-registry-key'
SET = 'micro-behaviors/os/registry/write::set-registry-value'
BOOT = 'objectives/persistence/firmware/boot/record::embedded-bios-read-hook-bootkit'
HIDE = 'objectives/evasion/kernel-hide/hook::windows-syscall-directory-result-hiding'
KEYS = 'objectives/collection/keylog/polling::native-xor-key-recording'
ENV = 'micro-behaviors/os/registry/access::python-user-environment-create'
FOLDER = 'micro-behaviors/os/registry/access::python-user-folder-command-create'
STUB = 'micro-behaviors/os/registry/value-name::stubpath-value-name'
UAC = 'objectives/privilege-escalation/elevation-control/uac-bypass/hijack::computerdefaults-uac-bypass'


def image_sections(data):
    pe = struct.unpack_from('<I', data, 0x3c)[0]
    count = struct.unpack_from('<H', data, pe + 6)[0]
    table = pe + 24 + struct.unpack_from('<H', data, pe + 20)[0]
    for i in range(count):
        at = table + i * 40
        size, offset = struct.unpack_from('<II', data, at + 16)
        yield data[at:at+8].rstrip(b'\0'), offset, size


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--sample', required=True, type=Path)
    p.add_argument('--scratch', required=True, type=Path)
    p.add_argument('--cleave', default='cleave')
    a = p.parse_args()
    a.scratch.mkdir(parents=True, exist_ok=True)
    driver = a.sample.read_bytes()
    dll_tail = driver[0x8d88:]
    dll = dll_tail[:max(off + size for _, off, size in image_sections(dll_tail))]
    inert = bytearray(dll)
    for name, off, size in image_sections(dll):
        if name == b'.text':
            inert[off:off+size] = b'\xcc' * size
    cases = [
        ('renamed.sys', driver, {DISK, BUILD, CALL, NATIVE_WRITE, CREATE, SET, BOOT, HIDE}, {OLD}),
        ('payload.dll', dll, {PROFILE, KEYS}, {OLD, DISK}),
        # Retaining imports while deleting executable code must not infer
        # anti-debugging, injection, key recording, or any hostile behavior.
        ('imports-only.dll', bytes(inert), {PROFILE}, {OLD, KEYS}),
        ('no-debug-name.dll', dll.replace(b'IsDebuggerPresent', b'IsDebuggerAbsent!'),
         {KEYS}, {PROFILE, OLD}),
        ('no-remote-write.dll', dll.replace(b'WriteProcessMemory', b'ProbeProcessMemory'),
         {KEYS}, {PROFILE, OLD}),
        ('other-device.sys', driver.replace('\\Driver\\Disk'.encode('utf-16le'),
                                            '\\Driver\\Null'.encode('utf-16le')),
         {BUILD, CALL}, {DISK}),
        ('no-builder.sys', driver.replace(b'IoBuildAsynchronousFsdRequest', b'XoBuildAsynchronousFsdRequest'),
         {CALL}, {BUILD, DISK}),
        ('no-dispatch.sys', driver.replace(b'IofCallDriver', b'XofCallDriver'),
         {BUILD}, {CALL, DISK}),
        ('no-native-write.sys', driver.replace(b'ZwWriteFile', b'ZwProbeFile'),
         {DISK}, {NATIVE_WRITE}),
        ('environment.py', b'import winreg\nwinreg.CreateKey(winreg.HKEY_CURRENT_USER, "Environment")\n',
         {ENV}, {FOLDER}),
        ('folder.py', b'import winreg\nwinreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Software\\Classes\\Folder\\shell\\open\\command")\n',
         {FOLDER}, {ENV}),
        ('read-only.py', b'import winreg\nwinreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment")\n',
         set(), {ENV, FOLDER}),
        ('value.ps1', b'$name = "StubPath"\n', {STUB}, set()),
        ('near-value.ps1', b'$name = "StubPaths"\n', set(), {STUB}),
        # Creating a key alone is no longer counted as a value write by the
        # ancestor write-directory selector used in this UAC rule.
        ('key-create-only.py', b'import winreg, subprocess\n'
         b'winreg.CreateKey(winreg.HKEY_CURRENT_USER, "Environment")\n'
         b'p = r"shell\\open\\command"\n'
         b'subprocess.Popen(["computerdefaults.exe"])\n', {ENV}, {UAC}),
    ]
    results = []
    for name, content, want, reject in cases:
        path = a.scratch / name
        path.write_bytes(content)
        proc = subprocess.run([a.cleave, '--no-update-check', '--traits-dir', str(ROOT),
            '--format', 'json', str(path)], capture_output=True, text=True, check=True)
        report = json.loads(proc.stdout)
        primary = next(f for f in report['files'] if f['path'] == str(path))
        found = {t['id']: t for t in primary['traits']}
        assert not (want - found.keys()), (name, 'missing', want - found.keys())
        assert not (reject & found.keys()), (name, 'unexpected', reject & found.keys())
        for trait in want - {KEYS, BOOT, HIDE}:
            assert found[trait]['crit'] == 3, (name, trait, found[trait]['crit'])
        if name == 'imports-only.dll':
            assert not [t['id'] for t in found.values() if t['crit'] >= 4], name
        results.append({'case': name, 'required': sorted(want), 'rejected': sorted(reject)})
    (a.scratch / 'results.json').write_text(json.dumps(results, indent=2) + '\n')
    print(f'{len(cases)} static boundary controls passed')


if __name__ == '__main__':
    main()
