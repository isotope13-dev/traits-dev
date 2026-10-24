#!/usr/bin/env python3
"""Recover this Node SEA resource layout without loading or executing code.

Usage: extract_sea.py <package/bin/vercel> <scratch-output-directory>
"""
import hashlib
import json
from pathlib import Path
import re
import struct
import sys

binary = Path(sys.argv[1]).read_bytes()
dest = Path(sys.argv[2]).resolve()
dest.mkdir(parents=True, exist_ok=True)
for match in re.finditer(b'NODE_SEA_BLOB\0', binary):
    off = match.start()
    if off < 12:
        continue
    namesz, descsz, _ = struct.unpack_from('<III', binary, off - 12)
    if namesz != 14:
        continue
    start = off + 16  # ELF note name padded to a multiple of four.
    if binary[start:start + 4] == bytes.fromhex('20 da 43 01'):
        blob = binary[start:start + descsz]
        assert len(blob) == descsz
        break
else:
    raise ValueError('No supported Node SEA note')

# Serialized SEA bootstrap header, then length-prefixed path and source.
pos = 9


def number():
    global pos
    assert pos + 8 <= len(blob)
    value = struct.unpack_from('<Q', blob, pos)[0]
    pos += 8
    return value


def span():
    global pos
    length = number()
    assert pos + length <= len(blob)
    value = blob[pos:pos + length]
    pos += length
    return value


source_path = span().decode()
source = span()
(dest / 'sea-main.js').write_bytes(source)
assets = {}
for _ in range(number()):
    name = span().decode()
    assert '/' not in name and '\\' not in name
    assets[name] = span()
    (dest / name).write_bytes(assets[name])
assert pos == len(blob), (pos, len(blob))
manifest = json.loads(assets['__pkg_manifest__'])
assert not manifest.get('compression'), 'This extractor expects uncompressed VFS entries'
archive = assets['__pkg_archive__']
index = {}
for name, (offset, length) in manifest['offsets'].items():
    target = (dest / 'vfs' / name.lstrip('/')).resolve()
    assert target.is_relative_to(dest / 'vfs')
    assert offset >= 0 and length >= 0 and offset + length <= len(archive)
    contents = archive[offset:offset + length]
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(contents)
    index[name] = {'size': length, 'sha256': hashlib.sha256(contents).hexdigest()}
(dest / 'index.json').write_text(json.dumps(index, indent=2) + '\n')
print(json.dumps({'source_path': source_path, 'entrypoint': manifest['entrypoint'],
                  'files': len(index), 'assets': {k: len(v) for k, v in assets.items()}}))
