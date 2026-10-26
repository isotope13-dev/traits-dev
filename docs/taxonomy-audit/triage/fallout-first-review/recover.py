#!/usr/bin/env python3
"""Recover AutoIt source, its native loader and payload without executing them.

Requires pefile, autoit-ripper and pycryptodome. The source is a detokenized
reconstruction. Native resources and the decrypted PE retain their byte content.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re

import pefile
from autoit_ripper import extract, AutoItVersion
from Crypto.Cipher import AES


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('sample', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    original = args.sample.read_bytes()
    assert hashlib.sha256(original).hexdigest() == '31d3d0726b295054c0a3dd46a55224fffe7da8b6723ad12b230575afec88fa1d'
    pe = pefile.PE(data=original)
    resources = {}
    for kind in pe.DIRECTORY_ENTRY_RESOURCE.entries:
        for name in kind.directory.entries:
            entry = name.directory.entries[0].data.struct
            resources[str(name.name or name.id).lower()] = pe.get_data(entry.OffsetToData, entry.Size)
    outputs = {'netwire.exe': resources['rhitfgabocng']}
    source = next(data for name, data in extract(original, AutoItVersion.EA06) if name.endswith('.au3')).decode('utf-8').replace('\r\n', '\n')
    (args.output / 'script.au3').write_text(source)
    constants = {}
    for match in re.finditer(r'^Func (\w+) \( \).*?^EndFunc', source, re.M | re.S):
        body = match.group()
        use = re.search(r'&= \$\w+ \( \$(\w+) \[', body)
        if not use:
            continue
        array = re.search(r'Local \$' + use[1] + r' \[ "\d+" \] = \[ (.*?) \]', body)
        if array:
            codes = re.findall(r'\$IEAIZGJOJWGVHIL \( "0x([0-9A-F]+)" \)', array[1])
            if codes:
                constants[match[1]] = ''.join(chr(int(code, 16)) for code in codes)
    normalized = source[:source.index('Func TUPVMCEMGCHCGAIXXSGF')] + source[source.rindex('EndFunc') + 7:]
    for name, value in constants.items():
        normalized = re.sub(r'\b' + name + r' \( \)', lambda _: json.dumps(value), normalized)
    (args.output / 'normalized.au3').write_text(normalized)
    # Constants recovered above establish MD5 -> CryptDeriveKey AES-256.
    # Microsoft documents MD5 pad expansion and the default zero-IV CBC mode.
    password = b'wirkwecunhnipqgeikzhkxkvjegszsqyklazbwsvoznbuzhocc'
    digest = hashlib.md5(password).digest()
    key = b''.join(hashlib.md5(bytes(v ^ pad for v in digest) + bytes([pad]) * 48).digest() for pad in (0x36, 0x5c))
    text = b''.join(resources[n] for n in ('amsi1', 'uevagentpolicygenerator2', 'actxprxy3'))
    encrypted = bytes.fromhex(text[2:].decode('ascii'))
    decrypted = AES.new(key, AES.MODE_CBC, bytes(16)).decrypt(encrypted)
    pad = decrypted[-1]
    assert 0 < pad <= 16 and decrypted[-pad:] == bytes([pad]) * pad
    outputs['warzone.exe'] = decrypted[:-pad]
    loader = normalized[normalized.index('Func UHAP'):normalized.index('Func ACL')]
    blocks = {int(m[1]): m[2] for m in re.finditer(r'If \$1711300772 = (\d+) Then\n(.*?)\n\t\tEndIf', loader, re.S)}
    state, visited, hexcode = 804661967, set(), ''
    while state in blocks and state not in visited:
        visited.add(state)
        block = blocks[state]
        hexcode += ''.join(m[1] for m in re.findall(r'\$BIN_SHELLCODE (?:=|&=) "(0x)?([A-F0-9]+)"', block))
        if 'ExitLoop' in block:
            break
        next_state = re.search(r'\$1711300772 = (\d+)', block)
        if not next_state:
            break
        state = int(next_state[1])
    outputs['injection.bin'] = bytes.fromhex(hexcode)
    for name, data in outputs.items():
        (args.output / name).write_bytes(data)
        print(name, len(data), hashlib.sha256(data).hexdigest())


if __name__ == '__main__':
    main()
