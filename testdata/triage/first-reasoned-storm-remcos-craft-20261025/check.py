"""Inert PE and Swift controls. No fixture is executed.

Run with a scratch output directory: python3 <this-file> <scratch-dir>.
The generated PE has no entry point. Its imports and short instruction excerpts
exercise call setup, value-name binding and taxonomy consumers independently.
"""
import concurrent.futures
import json
import os
from pathlib import Path
import struct
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
HOOK = 'micro-behaviors/hardware/input/keyboard/hook::windows-keyboard-hook-install'
SERVICE = 'micro-behaviors/os/registry/write::x86-servicedll-delete-replace-128'
FETCH = 'micro-behaviors/communications/http/get::swift-urlsession-shared-data-from'


def pe(hook_type=13, value=b'servicedll', redirect=False, status=False):
    # Three independently mapped sections; no entry point or TLS callback.
    data = bytearray(0x1000)
    data[:2] = b'MZ'
    struct.pack_into('<I', data, 0x3c, 0x80)
    data[0x80:0x84] = b'PE\0\0'
    struct.pack_into('<HHIIIHH', data, 0x84, 0x14c, 3, 0, 0, 0, 224, 0x102)
    opt = 0x98
    struct.pack_into('<H', data, opt, 0x10b)
    struct.pack_into('<III', data, opt + 16, 0, 0x1000, 0x2000)
    struct.pack_into('<III', data, opt + 28, 0x400000, 0x1000, 0x200)
    struct.pack_into('<II', data, opt + 56, 0x4000, 0x200)
    struct.pack_into('<H', data, opt + 68, 3)
    struct.pack_into('<I', data, opt + 92, 16)
    struct.pack_into('<II', data, opt + 104, 0x3000, 80)
    for i, (name, raw, rva, size, flags) in enumerate([
        (b'.text', 0x200, 0x1000, 0x200, 0x60000020),
        (b'.rdata', 0x400, 0x2000, 0x400, 0x40000040),
        (b'.idata', 0x800, 0x3000, 0x400, 0xc0000040),
    ]):
        struct.pack_into('<8sIIIIIIHHI', data, 0x178 + i * 40, name, size,
                         rva, size, raw, 0, 0, 0, 0, flags)
    cursor = 0x880
    iats = {}
    def add(blob):
        nonlocal cursor
        pos = cursor
        data[pos:pos + len(blob)] = blob
        cursor += len(blob)
        cursor += cursor % 2
        return pos + 0x2800
    for i, (dll, names) in enumerate([
        ('USER32.dll', ['SetWindowsHookExA', 'CallNextHookEx']),
        ('KERNEL32.dll', ['GetModuleHandleA']),
        ('ADVAPI32.dll', ['RegDeleteValueA', 'RegSetValueExA']),
    ]):
        dll_rva = add(dll.encode() + b'\0')
        hint_names = [add(b'\0\0' + n.encode() + b'\0') for n in names]
        lookup = add(struct.pack('<' + 'I' * (len(names) + 1), *hint_names, 0))
        iat = add(struct.pack('<' + 'I' * (len(names) + 1), *hint_names, 0))
        struct.pack_into('<IIIII', data, 0x800 + i * 20, lookup, 0, 0, dll_rva, iat)
        iats.update({n: 0x400000 + iat + j * 4 for j, n in enumerate(names)})
    data[0x400:0x400 + len(value) + 1] = value + b'\0'
    if status:
        labels = b'Online Keylogger Started\0[ENTER]\0'
        data[0x440:0x440 + len(labels)] = labels
    word = lambda n: struct.pack('<I', n)
    code = (b'\x33\xff\x57\x57\xff\x15' + word(iats['GetModuleHandleA']) +
            b'\x50\x68' + word(0x401080) + b'\x6a' + bytes([hook_type]) +
            b'\xff\x15' + word(iats['SetWindowsHookExA']) + b'\xc3')
    data[0x200:0x200 + len(code)] = code
    code = (b'\x68' + word(0x402000) + b'\x52\xff\x15' + word(iats['RegDeleteValueA']) +
            b'\x68\x80\0\0\0\x50\x6a\x02\x6a\0\x68' + word(0x402000) +
            b'\x51\xff\x15' + word(iats['RegDeleteValueA' if redirect else 'RegSetValueExA']) + b'\xc3')
    data[0x240:0x240 + len(code)] = code
    assert cursor < 0xc00
    return data


def main(output):
    output.mkdir(parents=True, exist_ok=True)
    cases = []
    for name, content, present, absent in [
        ('lowercase-service-global-hook', pe(), {HOOK, SERVICE}, set()),
        ('uppercase-service-global-hook', pe(value=b'ServiceDLL'), {HOOK, SERVICE}, set()),
        ('mouse-hook', pe(hook_type=14), {SERVICE}, {HOOK}),
        ('different-value', pe(value=b'Unrelated!'), {HOOK}, {SERVICE}),
        ('wrong-write-iat', pe(redirect=True), {HOOK}, {SERVICE}),
    ]:
        path = output / (name + '.exe')
        path.write_bytes(content)
        cases.append((name, path, present, absent))
    for name in ['http-fetch', 'http-request', 'http-documentation', 'unrelated-data']:
        cases.append((name, HERE / (name + '.swift'),
                      {FETCH} if name == 'http-fetch' else set(),
                      set() if name == 'http-fetch' else {FETCH}))
    def check(case):
        name, path, present, absent = case
        result = subprocess.run([os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
                                 '--format', 'json', str(path)], capture_output=True, text=True)
        assert result.returncode == 0, (name, result.stderr)
        d = json.loads(result.stdout)
        (output / (name + '.json')).write_text(json.dumps(d))
        found = {t['id'] for f in d['files'] for t in f.get('traits', [])}
        assert present <= found, (name, 'missing', present - found)
        assert not absent & found, (name, 'unexpected', absent & found)
        # An ordinary global keyboard hook is useful capability evidence; it
        # cannot convict the fixture without recording/tasking evidence.
        if path.suffix == '.exe':
            assert not any(t.get('crit') == 5 for f in d['files'] for t in f.get('traits', [])), name
        return name
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        for name in pool.map(check, cases):
            print('PASS', name, flush=True)
    print(f'{len(cases)} controls passed')


if __name__ == '__main__':
    main(Path(sys.argv[1]))
