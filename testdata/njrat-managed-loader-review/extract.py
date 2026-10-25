#!/usr/bin/env python3
"""Statically recover the encrypted PE and verify the loader's strong name.

Usage: python3 extract.py SAMPLE SCRATCH
Requires dnfile, dncil and cryptography. Does not load or execute managed code.
"""
import base64
import gzip
import hashlib
import json
from pathlib import Path
import struct
import sys

import dnfile
from dncil.cil.body.reader import read_method_body_from_bytes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

sample, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
out.mkdir(parents=True, exist_ok=True)
original = sample.read_bytes()
assert hashlib.sha256(original).hexdigest() == 'fbd4db896bb05fdd2e25a28e7c19885d4f559268f0fef0c944739c255c7455bb'
pe = dnfile.dnPE(data=original)


def strings(method):
    row = pe.net.mdtables.MethodDef.rows[method - 1]
    body = read_method_body_from_bytes(pe.get_data(row.Rva, 65536))
    return [pe.net.user_strings.get(i.operand.rid).value for i in body.instructions if i.opcode.name == 'ldstr']


# Entry M128 -> M129: Base64 -> M130 AES-CBC -> M131 repeating-key XOR
# -> M132 gzip -> M57/M56 RunPE. Keys/IV originate in M123's initializer.
config, loader = strings(123), strings(129)
key = next(s.encode() for s in config if len(s) == 32)
iv = next(s.encode() for s in config if len(s) == 16 and s.isdigit())
xor_key = next(s.encode() for s in loader if s.startswith('MyXorKey'))
encoded = max(loader, key=len)
ciphertext = base64.b64decode(encoded, validate=True)
decryptor = Cipher(algorithms.AES(key), modes.CBC(iv)).decryptor()
plain = decryptor.update(ciphertext) + decryptor.finalize()
padding = plain[-1]
assert plain.endswith(bytes([padding]) * padding)
plain = plain[:-padding]
compressed = bytes(b ^ xor_key[i % len(xor_key)] for i, b in enumerate(plain))
payload = gzip.decompress(compressed)
assert payload[:2] == b'MZ'
(out / 'payload.exe').write_bytes(payload)

# ECMA-335 strong-name digest: zero the PE checksum and certificate directory,
# hash headers through the section table, hash section data while excluding
# the strong-name signature blob. RSA public key is the CLR Assembly key.
public = pe.net.mdtables.Assembly.rows[0].PublicKey.value
exponent = struct.unpack_from('<I', public, 28)[0]
modulus = int.from_bytes(public[32:], 'little')
sig_size = pe.net.struct.StrongNameSignatureSize
sig_off = pe.get_offset_from_rva(pe.net.struct.StrongNameSignatureRva)
signature = original[sig_off:sig_off + sig_size]
encoded_digest = pow(int.from_bytes(signature, 'little'), exponent, modulus).to_bytes(sig_size, 'big')
image = bytearray(original)
checksum = pe.OPTIONAL_HEADER.get_file_offset() + 64
security = pe.OPTIONAL_HEADER.DATA_DIRECTORY[4].get_file_offset()
image[checksum:checksum + 4] = bytes(4)
image[security:security + 8] = bytes(8)
digest = hashlib.sha1(image[:pe.sections[-1].get_file_offset() + 40])
for section in pe.sections:
    start, stop = section.PointerToRawData, section.PointerToRawData + section.SizeOfRawData
    if start <= sig_off < stop:
        digest.update(image[start:sig_off])
        digest.update(image[sig_off + sig_size:stop])
    else:
        digest.update(image[start:stop])
expected = b'\x30\x21\x30\x09\x06\x05\x2b\x0e\x03\x02\x1a\x05\x00\x04\x14' + digest.digest()
assert encoded_digest == b'\0\x01' + b'\xff' * (sig_size - len(expected) - 3) + b'\0' + expected
report = {
    'original_sha256': hashlib.sha256(original).hexdigest(),
    'payload_sha256': hashlib.sha256(payload).hexdigest(),
    'payload_size': len(payload),
    'transforms': ['Base64', 'AES-256-CBC/PKCS7', 'repeating-key XOR', 'gzip'],
    'strong_name_sha1': digest.hexdigest(),
    'strong_name_valid': True,
    'public_key_token': hashlib.sha1(public).digest()[-8:][::-1].hex(),
    'authenticode_present': bool(pe.OPTIONAL_HEADER.DATA_DIRECTORY[4].Size),
}
(out / 'extraction.json').write_text(json.dumps(report, indent=2))
print(json.dumps(report, indent=2))
