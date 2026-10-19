#!/usr/bin/env python3
"""Inert PE controls; optionally mutate a supplied mailbox-loader specimen.

Usage: python3 check.py SCRATCH_DIR [MAILBOX_SAMPLE]
No fixture or specimen is loaded or executed. Cleave only reads their bytes.
"""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location(
    'gui_controls', ROOT / 'testdata/taxonomy/windows-gui-intent-boundaries/run.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
work = Path(sys.argv[1]) / 'sdl-managed-native-controls'
work.mkdir(parents=True, exist_ok=True)
GATE = 'metadata/binary/instruction::x86-nine-byte-x-tag-dot-argument-call-gate'
MAIL = 'objectives/execution/payload/file-exec::pop3-tagged-exe-association-loader'
SQLITE = 'metadata/binary/layout/embedded::sqlite-format-header-reference'
FAIL = 'micro-behaviors/process/create/shell/native::shell-spawn-failure-message'
RETIRED = {
    'objectives/evasion/process/injection/hook::unsigned-dynamic-windows-hook-injector',
    'objectives/evasion/process/injection/hook::unsigned-named-windows-hook-injector',
    'objectives/evasion/process/injection/memory::code-injection-flush',
    'objectives/command-and-control/dropper/staging/resource::dotnet-aes-resource-hidden-process-profile',
    'objectives/privilege-escalation/exploit/shell::unable-to-spawn-shell',
    'objectives/privilege-escalation/exploit/shell::spawn-shell-fail-banner',
    'micro-behaviors/data/db/sqlite::sqlite-format',
}
expect = {}
def save(name, data, present=(), absent=()):
    (work / name).write_bytes(data)
    expect[name] = (set(present), set(absent) | RETIRED)

imports = {
    'KERNEL32.dll': ['LoadLibraryA', 'GetProcAddress', 'GetThreadContext',
                     'FlushInstructionCache'],
    'USER32.dll': ['SetWindowsHookExW', 'UnhookWindowsHookEx', 'PostThreadMessageW'],
}
save('ordinary-hook-and-cache-apis.exe', module.pe(imports, []), [
    'micro-behaviors/ui/window/hook::unsigned-imported-window-hook-loader-api-set',
    'micro-behaviors/mem/sync/cache::flush-instruction-cache',
])
save('shell-failure-with-bin-sh.exe', module.pe({}, ['unable to spawn shell', '/bin/sh']), [FAIL])
save('sqlite-reference.exe', module.pe({}, ['SQLite format 3']), [SQLITE])
save('sqlite-absent.exe', module.pe({}, ['unrelated database header']), absent=[SQLITE])
# Import addresses and stack displacements are fixture values, never specimen
# fingerprints. Both LEA displacement encodings express the same stack pointer.
head = '6A 09 8D 84 24 80 00 00 00 52 50 E8 00 00 00 00 83 C4 10 85 C0 0F 84 00 00 00 00 80 7C 24 40 58 0F 85 00 00 00 00 '
tail = ' 6A 2E 51 FF 15 00 20 40 00 83 C4 08 85 C0 74 00 0F BE 50 FF 8D 70 FF 52 FF 15 04 20 40 00 83 C4 04 85 C0'
for section in ['text', 'unnamed']:
    for lea in ['4C 24 60', '8C 24 80 00 00 00']:
        code = bytes.fromhex(head + '8D ' + lea + tail)
        image = bytearray(module.pe({}, [], code))
        if section == 'unnamed':
            image[0x178:0x180] = bytes(8)
        save(f'gate-{section}-{len(code)}.exe', image, [GATE + ('-text' if section == 'text' else '-unnamed')], [MAIL])
        if section == 'unnamed' and len(code) == 80:
            save('gate-no-x.exe', image.replace(b'\x40\x58\x0f\x85', b'\x40\x59\x0f\x85'), absent=[GATE, GATE + '-text', GATE + '-unnamed', MAIL])
            save('gate-no-dot.exe', image.replace(b'\x6a\x2e\x51', b'\x6a\x2f\x51'), absent=[GATE, GATE + '-text', GATE + '-unnamed', MAIL])
if len(sys.argv) > 2:
    original = Path(sys.argv[2]).read_bytes()
    save('mailbox-renamed.exe', original, [GATE, MAIL])
    check = b'\x80\x7c\x24\x42\x58\x0f\x85'
    assert original.count(check) == 1
    save('mailbox-no-x.exe', original.replace(check, check[:4] + b'\x59' + check[5:]), absent=[GATE, GATE + '-text', GATE + '-unnamed', MAIL])
    assert b'RETR %d' in original
    save('mailbox-no-retr.exe', original.replace(b'RETR %d', b'XXXX %d'), [GATE + '-unnamed'], [MAIL])
result = subprocess.run(['cleave', '--traits-dir', str(ROOT), '--format', 'jsonl', str(work)],
                        check=True, capture_output=True, text=True)
records = [json.loads(line) for line in result.stdout.splitlines() if line.strip()]
checked = []
for report in records:
    for entry in report['files']:
        name = Path(entry['path']).name
        if name not in expect:
            continue
        traits = {t['id']: t for t in entry['traits']}
        present, absent = expect[name]
        assert present <= traits.keys(), (name, 'missing', present - traits.keys())
        assert not absent & traits.keys(), (name, 'unexpected', absent & traits.keys())
        for identity in [FAIL, SQLITE]:
            if identity in traits:
                assert traits[identity]['crit'] == 3, (name, identity, 'must remain notable')
        checked.append(name)
assert set(checked) == set(expect), (set(expect) - set(checked))
print(json.dumps({'passed': len(checked), 'cases': sorted(checked)}, indent=2))
