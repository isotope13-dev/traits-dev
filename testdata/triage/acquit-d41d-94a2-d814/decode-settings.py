"""Recover the SETTINGS resource using the native agent's length/key layout."""
import json
import sys
import pefile
from Crypto.Cipher import ARC4

pe = pefile.PE(sys.argv[1])
for kind in pe.DIRECTORY_ENTRY_RESOURCE.entries:
    if kind.id != 10:
        continue
    for name in kind.directory.entries:
        if str(name.name) != 'SETTINGS':
            continue
        for language in name.directory.entries:
            entry = language.data.struct
            data = pe.get_data(entry.OffsetToData, entry.Size)
            length = data[0]
            key = data[1:1+length]
            plain = ARC4.new(key).decrypt(data[1+length:])
            print(json.dumps({'resource_rva': hex(entry.OffsetToData),
                              'resource_size': entry.Size, 'key_length': length,
                              'fields': [{'index': i, 'hex': v.hex(),
                                          'display': repr(v)}
                                         for i, v in enumerate(plain.split(b'\x1e'))]}, indent=2))
