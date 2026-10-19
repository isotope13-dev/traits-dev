"""Build inert Mach-O byte-pattern controls; no executable entry point."""
import json
import struct
from pathlib import Path

root = Path(__file__).resolve().parent.relative_to(Path.cwd())

def image(code):
    base = 0x100000000
    header = struct.pack('<8I', 0xfeedfacf, 0x1000007, 3, 2, 1, 152, 0x200000, 0)
    segment = struct.pack('<II16sQQQQIIII', 0x19, 152, b'__TEXT', base, 4096,
                          0, 256 + len(code), 7, 5, 1, 0)
    section = struct.pack('<16s16sQQIIIIIIII', b'__text', b'__TEXT', base + 256,
                          len(code), 256, 4, 0, 0, 0x80000400, 0, 0, 0)
    return (header + segment + section).ljust(256, b'\0') + code

state = bytes.fromhex('69 c9 0d 66 19 00 81 c1 5f f3 6e 3c 89 0c 24 8b 0c 24 31 c1 89 4c 24 04 e9 00 00 00 00')
compare = bytes.fromhex('49 63 c6 4c 89 e7 41 c6 04 04 00 e8 00 00 00 00 4c 39 e8 0f 84 00 00 00 00')
terminal = bytes.fromhex('48 83 e0 1b 75 19 48 8d 7c 24 18 48 89 de e8 00 00 00 00 48 03 44 24 20 48 39 5c 24 18 76 02')
sipround = bytes.fromhex('49 01 dd 48 c1 c3 0d 4c 09 cf 4c 31 eb 49 c1 c5 20 49 31 fc 4d 01 e7 49 c1 c4 10 4d 31 fc 4d 01 e5 49 c1 c4 15 49 01 df 48 c1 c3 11 4c 31 fb 49 c1 c7 20')

def stack_bytes(data):
    data = data.ljust((len(data) + 3) // 4 * 4, b'\0')
    stores = b''.join(b'\xc7\x44\x24' + bytes([i]) + data[i:i+4]
                      for i in range(0, len(data), 4))
    return b'\x48\x83\xec\x40' + stores + b'\x48\x83\xc4\x40\xc3'

rules = [
    'objectives/anti-static/obfuscation/control-flow/dispatch::masked-arithmetic-dispatch-state',
    'objectives/anti-static/obfuscation/native-api-hash::export-trie-name-hash-resolution',
    'micro-behaviors/crypto/hash/hmac::siphash-arx-round-x64',
    'micro-behaviors/data/string/assembly::native-immediate-string',
]
controls = [
    ('encoded-dispatch', state * 5, [rules[0]]),
    ('dispatch-under-threshold', state * 4, []),
    ('ordinary-lcg', bytes.fromhex('69 c9 0d 66 19 00 81 c1 5f f3 6e 3c c3') * 8, []),
    ('hashed-export-terminal', compare + b'\x90' * 64 + terminal, [rules[1]]),
    ('name-compare-only', compare, []),
    ('export-terminal-only', terminal, []),
    ('siphash-round-only', sipround, [rules[2]]),
    ('stack-path', stack_bytes(b'/tmp/configuration\0'), [rules[3]]),
    ('stack-arithmetic-immediates', stack_bytes(b'z-iVz-iVz-iV'), []),
]
fixtures = []
for name, code, expected in controls:
    path = root / (name + '.macho')
    path.write_bytes(image(code))
    fixtures.append({'path': str(path), 'matched': expected,
                     'not_matched': [r for r in rules if r not in expected]})
(root / 'cases.json').write_text(json.dumps({'fixtures': fixtures}, indent=2) + '\n')
