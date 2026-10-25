#!/usr/bin/env python3
"""Reproduce offline recovery; never execute the extracted code.

Requires pycryptodome. Offsets/parameters below were recovered from Rust main
and its decryption function, not guessed from detection names.
"""
import argparse
import base64
import hashlib
import io
from pathlib import Path
import zipfile
from Crypto.Cipher import AES

parser = argparse.ArgumentParser()
parser.add_argument('sample', type=Path)
parser.add_argument('output', type=Path)
args = parser.parse_args()
data = args.sample.read_bytes()
assert hashlib.sha256(data).hexdigest() == 'd39298d192ef33de7ffa4ae1ae62700b4074a2ef379fd83bb1651647341923f1'

def rdata(rva, count):
    return data[rva - 0x1a00:rva - 0x1a00 + count]

password = base64.b64decode(rdata(0x610046, 44))
salt = bytes.fromhex(rdata(0x610072, 32).decode())
nonce = bytes.fromhex(rdata(0x610092, 24).decode())
tag = bytes.fromhex(rdata(0x6100aa, 32).decode())
# The loop terminating at RVA 0x5845 compares against 0x21943.
key = hashlib.pbkdf2_hmac('sha256', password, salt, 137539, 32)
plain = AES.new(key, AES.MODE_GCM, nonce=nonce).decrypt_and_verify(
    rdata(0xe2b40, 0x52d022), tag)
args.output.mkdir(parents=True, exist_ok=True)
(args.output / 'decrypted.zip').write_bytes(plain)
with zipfile.ZipFile(io.BytesIO(plain)) as z:
    for member in z.infolist():
        target = args.output / member.filename
        if member.is_dir():
            continue
        assert target.resolve().is_relative_to(args.output.resolve())
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(z.read(member))
    runtime = z.read('app-1.49.1/python310.zip')
with zipfile.ZipFile(io.BytesIO(runtime)) as z:
    (args.output / 'encodings-init.pyc').write_bytes(z.read('encodings/__init__.pyc'))
print('Authenticated ZIP and Python bootstrap bytecode recovered.')
