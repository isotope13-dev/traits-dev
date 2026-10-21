"""Inert ELF controls for linked calls, signal values, and section placement.

The fixture has no entry point or program headers. Never execute it.
Run: python3 testdata/taxonomy/i386-packet-task-review/check.py
"""
import concurrent.futures
import json
import struct
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FLOOD = 'micro-behaviors/communications/flood::i386-table-indexed-datagram-loop'
KILL = 'micro-behaviors/process/terminate/kill::i386-logged-sigkill-call-sequence'
RIVAL = 'objectives/impact/degrade/rival-bot/competitor::multiarch-bot-procfs-rival-killer'
TASK = 'objectives/command-and-control/botnet/dispatch::i386-framed-attack-task-code'
DOS = 'objectives/impact/dos/udp::i386-framed-packet-table-flood'
TRACE = 'objectives/anti-analysis/debugger-detect/check::i386-self-trace-failure-check'
XOR = 'micro-behaviors/data/encoding/xor::i386-four-lane-table-xor-loop'
ALL = {FLOOD, KILL, RIVAL, TASK, DOS, TRACE, XOR}

# Code excerpts with the link targets rebuilt below. No addresses, domain,
# key value, taunt or sample basename contributes to any of these rules.
PARTS = {
    'loop': (0x000, '680040000050508b44b3fc50e83964000083c40c40508b44b3fc508b44b5fc4650e8fd2e000083c41039f774c6ebd1'),
    'strlen': (0x100, '5731c08b7c240883c9fff2aef7d14989c85fc3'),
    'send': (0x180, '5383ec208d44241c506a01e8d80a0000ff74243cff74243cff74243cff74243ce80239000083c4186a0089c3ff742420e8b30a000089d883c4285bc3'),
    'send_impl': (0x200, '83ec248b442428894424148b44242c894424188b4424308944241c8b442434894424208d442414506a09e8451d0000'),
    'site': (0x280, 'e8ee4c000083c4186a0956e84d430000'),
    'kill': (0x300, '5383ec088b5424108b4c241487d3b825000000cd8087d3'),
    'dispatch': (0x380, '66c1c808663d000466898424f61500000f870b010000c707000000006802400000668b8424fa15000025ffff0000508d842428100000508b154ca9050852e86622000083c41083f8ff748285c0749268004000006a028d9424fe15000052a14ca9050850e840220000668b84240616000066c1c808668984240616000025ffff00006800400000508d8c243810000051a14ca9050850e80e22000083c41c8d8424c415000050668b8424fe15000025ffff0000508d84242c10000050e886b8ffff'),
    'parser': (0x500, '5557565383ec1c8b5c24348b7424308b7c243883fb03770b83c8ff83c41c5b5e5f5dc38b0666c1c808c1c81066c1c80883fb04890774e18a460483fb0588470474d68a460588470584c074cc8d53fa8954241031d288c28d049239442410'),
    'recv': (0x600, '5383ec208d44241c506a01e8d80a0000ff74243cff74243cff74243cff74243ce80239000083c4186a0089c3ff742420e8b30a000089d883c4285bc3'),
    'recv_impl': (0x680, '83ec248b442428894424148b44242c894424188b4424308944241c8b442434894424208d442414506a0ae8e61d0000'),
    'probe': (0x700, '6a006a016a006a00e8e183000083c42040740483c40cc383ec0c6a01e88ab90000'),
    'ptrace': (0x780, '57565383ec108b7c24208d442430894424088b4c24248d47ff8b5424288b74242c83f80277048d74240c5389fbb81a000000cd80'),
    'xor': (0x880, '8b1989d001d889eb301889d08b1901d889fb301889d08b1901d889f3301889d08b194201d88a1c2430188b410425ffff000039d07fca'),
}


def link(code, origin, instruction, target):
    src = PARTS[origin][0] + instruction
    dst = PARTS[target][0]
    assert code[src] == 0xe8
    struct.pack_into('<i', code, src + 1, dst - src - 5)


def code_bytes():
    code = bytearray(b'\x90' * 0xa00)
    for offset, value in PARTS.values():
        code[offset:offset + len(bytes.fromhex(value))] = bytes.fromhex(value)
    for args in [('loop', 12, 'strlen'), ('loop', 33, 'send'),
                 ('send', 32, 'send_impl'), ('site', 11, 'kill'),
                 ('dispatch', 62, 'recv'), ('dispatch', 100, 'recv'),
                 ('dispatch', 150, 'recv'), ('dispatch', 188, 'parser'),
                 ('recv', 32, 'recv_impl'), ('probe', 8, 'ptrace')]:
        link(code, *args)
    return code


CONTEXT = (b'agent_x86\0agent_mips\0agent_arm\0/proc/%d/exe\0'
           b'/proc/%d/maps\0Killed process: %s, PID: %d\0')


def elf(code, context=CONTEXT, in_rodata=False):
    data = bytearray(0x3000)
    ident = b'\x7fELF\x01\x01\x01' + b'\0' * 9
    struct.pack_into('<16sHHIIIIIHHHHHH', data, 0, ident, 2, 3, 1,
                     0, 0, 0x2900, 0, 52, 0, 0, 40, 4, 3)
    labels = b'\0.text\0.rodata\0.shstrtab\0'
    sections = [(1, 0x200, 6, b'' if in_rodata else code),
                (7, 0x1000, 2, (code if in_rodata else b'') + context),
                (15, 0x2800, 0, labels)]
    for i, (label, offset, flags, content) in enumerate(sections, 1):
        data[offset:offset + len(content)] = content
        struct.pack_into('<10I', data, 0x2900 + i * 40, label,
                         3 if i == 3 else 1, flags, 0x8048000 + offset,
                         offset, len(content), 0, 0, 4, 0)
    return data


def changed(name, relative, replacement):
    code = code_bytes()
    offset = PARTS[name][0] + relative
    code[offset:offset + len(replacement)] = replacement
    return code


def redirected(origin, instruction, target):
    code = code_bytes()
    link(code, origin, instruction, target)
    return code


cases = [
    ('linked-code', elf(code_bytes()), ALL, set()),
    ('no-process-context', elf(code_bytes(), b''), ALL - {RIVAL}, {RIVAL}),
    ('strings-only', elf(b''), set(), ALL),
    ('code-in-rodata', elf(code_bytes(), in_rodata=True), set(), ALL),
    ('sigterm', elf(changed('site', 9, b'\x0f')), ALL - {KILL, RIVAL}, {KILL, RIVAL}),
    ('redirected-kill', elf(redirected('site', 11, 'strlen')),
     ALL - {KILL, RIVAL}, {KILL, RIVAL}),
    ('redirected-send', elf(redirected('loop', 33, 'recv')),
     ALL - {FLOOD, DOS}, {FLOOD, DOS}),
    ('wrong-send-operation', elf(changed('send_impl', 41, b'\x0a')),
     ALL - {FLOOD, DOS}, {FLOOD, DOS}),
    ('redirected-strlen', elf(redirected('loop', 12, 'kill')),
     ALL - {FLOOD, DOS}, {FLOOD, DOS}),
    ('redirected-receive', elf(redirected('dispatch', 150, 'send')),
     ALL - {TASK, DOS}, {TASK, DOS}),
    ('wrong-receive-operation', elf(changed('recv_impl', 41, b'\x09')),
     ALL - {TASK, DOS}, {TASK, DOS}),
    ('redirected-parser', elf(redirected('dispatch', 188, 'strlen')),
     ALL - {TASK, DOS}, {TASK, DOS}),
    ('wrong-record-bound', elf(changed('dispatch', 6, b'\x00\x08')),
     ALL - {TASK, DOS}, {TASK, DOS}),
    ('redirected-probe', elf(redirected('probe', 8, 'kill')),
     ALL - {TRACE}, {TRACE}),
    ('non-traceme-request', elf(changed('probe', 7, b'\x10')),
     ALL - {TRACE}, {TRACE}),
]


def check(case):
    name, content, present, absent = case
    path = Path(output) / (name + '.elf')
    path.write_bytes(content)
    result = subprocess.run(['cleave', '--traits-dir', str(ROOT), '--format', 'json', str(path)],
                            capture_output=True, text=True, check=True)
    data = json.loads(result.stdout)
    found = {t['id'] for f in data['files'] for t in f.get('traits', [])}
    assert present <= found, (name, 'missing', sorted(present - found))
    assert not (absent & found), (name, 'unexpected', sorted(absent & found))
    return name


if __name__ == '__main__':
    with tempfile.TemporaryDirectory(prefix='i386-task-review-') as output:
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
            for name in pool.map(check, cases):
                print('PASS', name, flush=True)
    print(f'{len(cases)} linked-call and near-miss controls passed')
