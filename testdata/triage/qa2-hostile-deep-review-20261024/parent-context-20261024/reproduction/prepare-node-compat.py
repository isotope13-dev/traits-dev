"""Prepare a synthetic-interpreter copy; original source is never overwritten."""
from pathlib import Path
import hashlib,json
w=Path('/tmp/qa2-parent-review')
source=(w/'app/index.js').read_bytes()
assert hashlib.sha256(source).hexdigest()=='9afa39608797499494b858b019c99a48ffef87bf53dd729d5cf7a162c6f73fb0'
offsets=[711492,722149]
for offset in sorted(offsets,reverse=True):
    assert source[offset-1:offset+6]==b'}await '
    source=source[:offset]+b';'+source[offset:]
(w/'index-quickjs-compatible.js').write_bytes(source)
print('Inserted two empty statements after block-level function declarations to avoid QuickJS parser incompatibility.')
