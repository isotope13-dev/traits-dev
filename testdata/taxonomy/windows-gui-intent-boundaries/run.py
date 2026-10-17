#!/usr/bin/env python3
"""Inert PE controls for GUI/API co-occurrence versus recording/injection.

All entry points return immediately. Fixtures are generated in --output-dir;
no specimen bytes, executable payloads, or third-party libraries are needed.
"""
import argparse
import hashlib
import json
import pathlib
import struct
import subprocess


def pe(imports, strings, code=b''):
    text = b'\xc3' + b'\x90' * 31 + code
    text = text.ljust(0x400, b'\0')
    rdata = bytearray(0x2000)
    pos = 0x100
    def alloc(data):
        nonlocal pos
        start = pos
        rdata[start:start + len(data)] = data
        pos += len(data)
        pos = (pos + 3) & ~3
        return 0x2000 + start
    for n, (lib, names) in enumerate(imports.items()):
        lib_rva = alloc(lib.encode() + b'\0')
        names_rva = [alloc(b'\0\0' + name.encode() + b'\0') for name in names]
        table = b''.join(struct.pack('<I', x) for x in names_rva) + b'\0' * 4
        lookup = alloc(table)
        iat = alloc(table)
        struct.pack_into('<IIIII', rdata, n * 20, lookup, 0, 0, lib_rva, iat)
    for string in strings:
        alloc(string.encode() + b'\0')
    # A compressed/data resource's entropy has no bearing on hostile intent.
    resource = b''.join(hashlib.sha256(struct.pack('<I', n)).digest()
                        for n in range(0x28000 // 32))
    headers = bytearray(0x400)
    headers[:2] = b'MZ'
    struct.pack_into('<I', headers, 0x3c, 0x80)
    headers[0x80:0x84] = b'PE\0\0'
    struct.pack_into('<HHIIIHH', headers, 0x84, 0x14c, 4, 1494530977,
                     0, 0, 224, 0x102)
    opt = 0x98
    struct.pack_into('<H', headers, opt, 0x10b)
    struct.pack_into('<III', headers, opt + 16, 0x1000, 0x1000, 0x2000)
    struct.pack_into('<III', headers, opt + 28, 0x400000, 0x1000, 0x200)
    struct.pack_into('<HH', headers, opt + 40, 5, 1)
    struct.pack_into('<II', headers, opt + 56, 0x2e000, 0x400)
    struct.pack_into('<H', headers, opt + 68, 2)
    struct.pack_into('<IIIIII', headers, opt + 72,
                     0x100000, 0x1000, 0x100000, 0x1000, 0, 16)
    struct.pack_into('<II', headers, opt + 104, 0x2000, (len(imports) + 1) * 20)
    sections = [(b'.text', 0x1000, text, 0x60000020),
                (b'.rdata', 0x2000, bytes(rdata), 0x40000040),
                (b'.data', 0x4000, bytes(0x200), 0xc0000040),
                (b'.rsrc', 0x5000, resource, 0x40000040)]
    raw = 0x400
    for n, (name, rva, data, flags) in enumerate(sections):
        struct.pack_into('<8sIIIIIIHHI', headers, opt + 224 + n * 40,
                         name, len(data), rva, len(data), raw, 0, 0, 0, 0, flags)
        raw += len(data)
    return bytes(headers) + b''.join(s[2] for s in sections)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cleave', default='cleave')
    parser.add_argument('--output-dir', type=pathlib.Path, required=True)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    imports = {
        'KERNEL32.dll': ['GetModuleFileNameA', 'GetShortPathNameA',
          'GetEnvironmentVariableA', 'CreateProcessA', 'VirtualAllocEx',
          'WriteProcessMemory', 'CreateRemoteThread', 'GetProcAddress',
          'GetModuleHandleA', 'FindResourceA', 'SizeofResource', 'LoadResource',
          'LockResource', 'WinExec', 'VirtualAlloc'],
        'USER32.dll': ['SetWindowsHookExW', 'CallNextHookEx',
          'UnhookWindowsHookEx', 'GetDesktopWindow'],
        'GDI32.dll': ['BitBlt', 'GetDIBits'],
        'gdiplus.dll': ['GdipSaveImageToStream'],
    }
    strings = ['LoadLibraryA', 'comspec', ' /c  del ', 'svchost.exe',
        'http://example.invalid/update.php', 'POST /submit HTTP/1.1',
        'Content-Type: application/x-www-form-urlencoded']
    # Address operands and stack displacements are arbitrary fixture values.
    setup = bytes.fromhex('68 04 01 00 00 29 db 50 53 ff 15 00 20 40 00'
        ' 85 c0 0f 84 00 00 00 00 8d 4c 24 64 68 04 01 00 00 8d 54 24 68'
        ' 51 52 ff 15 04 20 40 00 85 c0 0f 84 00 00 00 00'
        ' 8d 84 24 6c 02 00 00 68 04 01 00 00 50 68 00 30 40 00'
        ' ff 15 08 20 40 00')
    handoff = bytes.fromhex('50 ff 15 0c 20 40 00 85 c0 75 00') + bytes(9)
    handoff += bytes.fromhex('c3 8b 4c 24 20 6a 00 6a 00 56 50 6a 00 6a 00 51'
                            ' ff 15 10 20 40 00')
    keylog = 'objectives/collection/keylog/hook::keyboard-hook-http-post'
    cleanup = 'objectives/evasion/self-delete/process::native-dll-injector-shell-cleanup'
    neutral = 'micro-behaviors/data/embedded/payload/resource::unsigned-resource-winexec-api-profile'
    image = 'micro-behaviors/ui/graphics/image::gdi-image-save-network-api-profile'
    cases = [
        ('gui-http', [], b'', [neutral, image], [keylog, cleanup]),
        ('keyboard-without-recording', ['WH_KEYBOARD_LL'], b'',
         [neutral, image], [keylog, cleanup]),
        ('recording-keyboard', ['WH_KEYBOARD_LL', 'Online Keylogger Started'],
         b'', [keylog, neutral], [cleanup]),
        ('injection-without-cleanup-code', [], handoff, [neutral], [cleanup]),
        ('resource-injector-cleanup', [], setup + handoff, [cleanup], [keylog]),
        ('wrong-thread-entry', [], setup + handoff.replace(b'\x56\x50\x6a',
         b'\x56\x52\x6a'), [neutral], [cleanup]),
    ]
    results = []
    for name, extra, code, required, absent in cases:
        path = args.output_dir / (name + '.exe')
        path.write_bytes(pe(imports, strings + extra, code))
        proc = subprocess.run([args.cleave, '--traits-dir', '.', '--format',
                               'json', str(path)], capture_output=True, text=True)
        if proc.returncode:
            raise RuntimeError(proc.stderr)
        report = json.loads(proc.stdout)
        def traits(value):
            if isinstance(value, dict):
                if 'id' in value and 'crit' in value:
                    yield value['id']
                for v in value.values(): yield from traits(v)
            elif isinstance(value, list):
                for v in value: yield from traits(v)
        matched = set(traits(report))
        missing = set(required) - matched
        unexpected = set(absent) & matched
        assert not missing and not unexpected, (name, missing, unexpected)
        results.append({'case': name, 'required': required, 'absent': absent,
                        'passed': True})
        print(name + ': PASS')
    (args.output_dir / 'results.json').write_text(json.dumps(results, indent=2)+'\n')

if __name__ == '__main__':
    main()
