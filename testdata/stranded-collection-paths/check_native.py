"""Mutate encrypted source in the supplied specimen; analyze, never execute it."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('sample', type=Path)
parser.add_argument('scratch', type=Path)
args = parser.parse_args()
original = args.sample.read_bytes()
assert hashlib.sha256(original).hexdigest() == '8202c3887b75b107f76385fe36e7949860b7931cebd2c65899649556c37e30bc'
args.scratch.mkdir(parents=True, exist_ok=True)
start, length = 0x14de0, 37077
state, plain = 0x11667, bytearray()
for byte in original[start:start + length]:
    plain.append(byte ^ (state & 255))
    state = ((state * 0x3785) & 0xffffffff) % 35999

wallet = 'objectives/credential-access/wallet/desktop::password-phishing-desktop-wallet-read-profile'
variants = {
    'collector': (bytes(plain), True),
    'without-masked-prompt': (bytes(plain).replace(b'hidden answer', b'xxxxxx xxxxxx'), False),
    'without-read': (bytes(plain).replace(b' to read ', b' to xxxx '), False),
    'without-wallet-store': (bytes(plain).replace(b'Monero/wallets', b'X' * len(b'Monero/wallets')), False),
}
for name, (source, expected) in variants.items():
    assert len(source) == length
    encrypted, state = bytearray(), 0x11667
    for byte in source:
        encrypted.append(byte ^ (state & 255))
        state = ((state * 0x3785) & 0xffffffff) % 35999
    output = bytearray(original)
    for offset in [0x4c90, 0x14de0]:
        output[offset:offset + length] = encrypted
    (args.scratch / (name + '.macho')).write_bytes(output)

root = Path(__file__).resolve().parents[2]
result = subprocess.run([os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(root),
                         '--format', 'json', str(args.scratch)], capture_output=True, text=True)
assert result.stdout, result.stderr
remaining, found = result.stdout, {}
while remaining.strip():
    report, end = json.JSONDecoder().raw_decode(remaining.lstrip())
    remaining = remaining.lstrip()[end:]
    for file in report['files']:
        found[Path(file['path']).stem] = {trait['id'] for trait in file.get('traits', [])}
for name, (_, expected) in variants.items():
    assert (wallet in found[name]) == expected, (name, found[name])
    print(name, 'matched' if expected else 'not matched')
