#!/usr/bin/env python3
"""Static positive and near-miss controls for the native sample review.

Usage: check.py <Salat sample> <scratch directory>
Never executes any fixture. Large mutation fixtures remain outside the repo.
"""
import concurrent.futures
import json
import os
from pathlib import Path
import struct
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
SAMPLE, OUT = map(Path, sys.argv[1:])
OUT.mkdir(parents=True, exist_ok=True)
SOURCE = SAMPLE.read_bytes()
PE = struct.unpack_from('<I', SOURCE, 0x3c)[0]
SEC = PE + 24 + struct.unpack_from('<H', SOURCE, PE + 20)[0]
KEYLOG = 'objectives/collection/keylog/hook::go-keyboard-hook-recording-profile'
HARVEST = 'objectives/credential-access/browser/chromium::go-browser-login-query-with-keylogging'
FAMILY = 'well-known/malware/rat/salat::salat-stealer-rat'
HOOK = 'micro-behaviors/hardware/input/keyboard/hook::go-x86-keyboard-hook-profile'
QUERY = 'micro-behaviors/data/db/query::chromium-login-query-reference'
MANAGED = {f'metadata/binary/symbols/name::dotnet-{x}-method-name'
           for x in ['kill', 'append', 'create-instance']}
CASES = []

def add(name, data, yes=(), no=()):
    path = OUT / name
    path.write_bytes(data)
    CASES.append((path, set(yes), set(no)))

def replaced(old, new):
    assert len(old) == len(new) and old in SOURCE
    return SOURCE.replace(old, new)

add('original.exe', SOURCE, [KEYLOG, HARVEST, FAMILY, HOOK, QUERY], MANAGED)
# All executable bytes remain, only the hook selector changes to WH_GETMESSAGE.
add('wrong-hook-id.exe', replaced(bytes.fromhex('c7000d0000008b4c24'),
                                 bytes.fromhex('c700030000008b4c24')),
    ['micro-behaviors/data/db/query::chromium-login-column-select-upx0'], [HOOK, KEYLOG, HARVEST, FAMILY])
# Retain the SQL keyword and store references, but remove the secret columns.
add('no-login-columns.exe', replaced(b'SELECT origin_url, action_url, username_value, password_value',
                                    b'SELECT origin_url, action_url, ordinary_value, ordinary_value'),
    [HOOK, KEYLOG], [QUERY, HARVEST, FAMILY])
# This preserves query selection and hook mechanics; a missing conversion API
# must still prevent the recording claim, and consequently the family verdict.
add('no-key-conversion.exe', replaced(b'ToUnicodeEx', b'NoUnicodeEx'),
    [HOOK, 'micro-behaviors/data/db/query::chromium-login-column-select-upx0'], [KEYLOG, HARVEST, FAMILY])
# Test the original .text code placement independently of the UPX0 fallback.
text_variant = bytearray(SOURCE)
text_variant[SEC:SEC + 8] = b'.text\0\0\0'
add('text-layout.exe', text_variant, [HOOK, KEYLOG], [QUERY, HARVEST, FAMILY])

# Inert PE32 with optional CLR data directory: names alone are never a socket,
# kill or reflection operation. A real CLR header gates managed-name metadata.
def inert_pe(clr=False):
    data = bytearray(0x800)
    data[:2] = b'MZ'
    struct.pack_into('<I', data, 0x3c, 0x80)
    data[0x80:0x84] = b'PE\0\0'
    struct.pack_into('<HHIIIHH', data, 0x84, 0x14c, 1, 0, 0, 0, 224, 0x102)
    opt = 0x98
    struct.pack_into('<H', data, opt, 0x10b)
    struct.pack_into('<I', data, opt + 28, 0x400000)
    struct.pack_into('<II', data, opt + 32, 0x1000, 0x200)
    struct.pack_into('<II', data, opt + 56, 0x2000, 0x200)
    struct.pack_into('<H', data, opt + 68, 3)
    struct.pack_into('<I', data, opt + 92, 16)
    struct.pack_into('<8sIIIIIIHHI', data, opt + 224, b'.text\0\0\0',
                     0x600, 0x1000, 0x600, 0x200, 0, 0, 0, 0, 0x40000040)
    if clr:
        struct.pack_into('<II', data, opt + 96 + 14 * 8, 0x1000, 72)
        struct.pack_into('<IHHIIII', data, 0x200, 72, 2, 5, 0x1080, 0x80, 1, 0)
        data[0x280:0x284] = b'BSJB'
        struct.pack_into('<HHII', data, 0x284, 1, 1, 0, 12)
        data[0x290:0x29c] = b'v4.0.30319\0\0'
    tokens = b'\0Send\0Receive\0Kill\0Append\0CreateInstance\0'
    data[0x400:0x400 + len(tokens)] = tokens
    return data

add('native-method-words.exe', inert_pe(), [], MANAGED | {HOOK, KEYLOG, HARVEST, FAMILY})
add('managed-method-words.exe', inert_pe(True), MANAGED, [HOOK, KEYLOG, HARVEST, FAMILY])
# This is a static SELECT fixture with no record capture or credential target
# chain. The query observation must not by itself convict a browser utility.
query_only = inert_pe()
q = b'SELECT origin_url, action_url, username_value, password_value FROM logins\0'
query_only[0x500:0x500 + len(q)] = q
add('query-only.exe', query_only, ['micro-behaviors/data/db/access::chromium-login-sql'], [KEYLOG, HARVEST, FAMILY])


# A repeated text measurement is independent of the sample's maliciousness.
# Four runs are a near miss; five runs establish the stated population only.
PROFILE = 'metadata/file/profile/string-population::punctuation-prefixed-word-runs'
for count in (4, 5):
    data = inert_pe()
    words = b'~abc def ghi jkl mno\0' * count
    data[0x500:0x500 + len(words)] = words
    add(f'word-runs-{count}.exe', data, [PROFILE] if count == 5 else [],
        [HARVEST, FAMILY] + ([PROFILE] if count == 4 else []))

def scan(case):
    path, yes, no = case
    run = subprocess.run([os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
                          '--format', 'json', str(path)], capture_output=True, text=True,
                         env=dict(os.environ, CLEAVE_VALIDATE='0'), check=True)
    obj = json.loads(run.stdout)
    ids = {t['id'] for f in obj['files'] for t in f.get('traits', [])}
    return {'case': path.name, 'missing': sorted(yes - ids), 'unexpected': sorted(no & ids)}

with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    results = list(pool.map(scan, CASES))
print(json.dumps(results, indent=2))
(OUT / 'results.json').write_text(json.dumps(results, indent=2) + '\n')
sys.exit(any(r['missing'] or r['unexpected'] for r in results))
