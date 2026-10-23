"""Run with: uv run --with pyyaml --with yara-x python verify.py SAMPLES_ROOT.

Controls modify recovered originals in memory; they are not replacement samples.
The shared far-call correction also checks pre-existing attack fixtures.
"""
import json
import sys
from pathlib import Path

import yaml
import yara_x

ROOT = Path(__file__).resolve().parents[3]
SAMPLES = Path(sys.argv[1])
BOT = next(p for p in (SAMPLES / 'ba6b45458302').glob('2026*')
           if not p.name.endswith(('.BENIGN', '.MALICIOUS'))).read_bytes()
DOS = (SAMPLES / '7e080f1f6b58/Virus.DOS.DG.386').read_bytes()
WRAPPER = next(p for p in (SAMPLES / '8bc154405b1c').glob('2026*')
               if not p.name.endswith(('.BENIGN', '.MALICIOUS'))).read_bytes()
RULES = {
    'record': 'micro-behaviors/communications/socket/receive/x86-length-prefixed-record.yaml',
    'download': 'micro-behaviors/process/deploy/file-exec/x86-urlmon-winexec-buffer.yaml',
    'registry': 'objectives/persistence/login/winlogon/userinit/native-task-agent.yaml',
    'burst': 'micro-behaviors/communications/flood/x86-counted-datagrams.yaml',
    'infect': 'objectives/impact/infect/binary/dos/file/si-saved-handle-entry.yaml',
}
COMPILED = {}
for key, name in RULES.items():
    document = yaml.safe_load((ROOT / name).read_text())
    if 'traits' in document:
        source = document['traits'][0]['if']['source']
    else:
        source = next(c['source'] for c in document['composite_rules'][0]['all']
                      if c.get('type') == 'yara')
    COMPILED[key] = yara_x.compile(source)

RESULTS = []


def check(label, key, data, expected):
    actual = bool(COMPILED[key].scan(data).matching_rules)
    RESULTS.append({'case': label, 'rule': key, 'expected': expected, 'actual': actual})
    assert actual == expected, RESULTS[-1]


def change(data, offset, value):
    data = bytearray(data)
    data[offset:offset + len(value)] = value
    return bytes(data)


def bot_offset(address):
    return address - 0x401000 + 0x400


for key in ('record', 'download', 'registry', 'burst'):
    check('original bot', key, BOT, True)
    check('changed product description', key,
          change(BOT, 0x5f78, b'X\x00'), True)
    check('Tor networking executable', key,
          (ROOT / 'testdata/benign/tor-0.4.7.15.exe').read_bytes(), False)
    check('distinct variant-upload wrapper', key, WRAPPER, False)
    check('distinct embedded module implant', key, WRAPPER[0x3b000:], False)

# Binding controls retain all API strings and the surrounding operation.
check('download destination differs from executed path', 'download',
      change(BOT, bot_offset(0x401c69), b'\x18'), False)
check('recv operand changed to send IAT', 'record',
      change(BOT, bot_offset(0x40184f), bytes.fromhex('20614000')), False)
check('sendto operand changed to send IAT', 'burst',
      change(BOT, bot_offset(0x402b10), bytes.fromhex('20614000')), False)
check('delay operand changed to ExitThread IAT', 'burst',
      change(BOT, bot_offset(0x402b35), bytes.fromhex('1c604000')), False)
check('Userinit write operand points to ProductName', 'registry',
      change(BOT, bot_offset(0x402100), bytes.fromhex('78744000')), False)
check('concatenation delimiter is not comma', 'registry',
      change(BOT, 0x538c, b';'), False)

check('DOS memory image', 'infect', DOS, True)
check('DOS COM without memory prefix', 'infect', DOS[0x100:], True)
check('DOS family marker changed', 'infect', change(DOS, 0x280, b'XY'), True)
check('DOS non-jump entry buffer', 'infect', change(DOS, 0x258, b'\x90'), False)
check('DOS displacement stored in different buffer', 'infect',
      change(DOS, 0x1e9, bytes.fromhex('6002')), False)
check('DOS append reads different source', 'infect',
      change(DOS, 0x203, bytes.fromhex('2001')), False)
check('DOS saved length comes from different cell', 'infect',
      change(DOS, 0x1e2, bytes.fromhex('6002')), False)


def hex_rule(pattern):
    return yara_x.compile('rule check_bytes { strings: $x = { ' + pattern +
                          ' } condition: $x }')


def bytecheck(label, rule, data, expected):
    actual = bool(rule.scan(data).matching_rules)
    RESULTS.append({'case': label, 'expected': expected, 'actual': actual})
    assert actual == expected, RESULTS[-1]


shared = yaml.safe_load((ROOT / 'micro-behaviors/fs/write/file/handle/dos.yaml').read_text())
far = next(t for t in shared['traits'] if t['id'] == 'dos-int21-write-far')
saved = next(t for t in shared['traits'] if t['id'] == 'dos-int21-write-saved-vector')
old = hex_rule('B4 40 [0-16] (2E FF 1E|EA)')
new = hex_rule(far['if']['pattern'])
tail = hex_rule(saved['if']['pattern'])
bytecheck('old false far-call on DG subtraction', old, DOS, True)
bytecheck('corrected far-call on DG', new, DOS, False)
bytecheck('retained CS far-call', new,
          bytes.fromhex('9c b440 bb0500 2eff1e3412'), True)
bytecheck('retained immediate far jump via saved-vector rule', tail,
          bytes.fromhex('b440 ea34127856'), True)
won = (ROOT / 'testdata/hostile/dos-com/won-2339').read_bytes()
bytecheck('existing Won saved-vector writes', tail, won, True)
dikshev = (ROOT / 'testdata/hostile/dos-com/dikshev-192b').read_bytes()
bytecheck('old false far-call on Dikshev SUB operand', old, dikshev, True)
bytecheck('corrected far-call on Dikshev', new, dikshev, False)
append = yaml.safe_load((ROOT / 'micro-behaviors/fs/write/file/handle/dos-append-entry-header.yaml').read_text())
bytecheck('retained Dikshev append/header technique',
          hex_rule(append['traits'][0]['if']['pattern']), dikshev, True)
copy = yaml.safe_load((ROOT / 'micro-behaviors/mem/write/arbitrary/dos-three-byte-entry.yaml').read_text())
entry_copy = hex_rule(copy['traits'][0]['if']['pattern'])
bytecheck('DOS host-entry copy', entry_copy, DOS, True)
bytecheck('copy destination is not COM entry', entry_copy,
          change(DOS, 0x23e, b'\x02'), False)
decode = yaml.safe_load((ROOT / 'micro-behaviors/data/decode/xor/sub-xor-buffer.yaml').read_text())
decoder = hex_rule(decode['traits'][0]['if']['pattern'])
bytecheck('bot subtraction/XOR decoder', decoder, BOT, True)
bytecheck('byte operation is not XOR', decoder,
          change(BOT, bot_offset(0x401df4), b'\x02'), False)
bytecheck('Tor has no matching subtraction/XOR loop', decoder,
          (ROOT / 'testdata/benign/tor-0.4.7.15.exe').read_bytes(), False)
print(json.dumps(RESULTS, indent=2))
