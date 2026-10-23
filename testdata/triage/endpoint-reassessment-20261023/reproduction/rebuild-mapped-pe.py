#!/usr/bin/env python3
"""Rebuild file layout from a recovered mapped PE; never load the specimen."""
import argparse
import hashlib
from pathlib import Path
import pefile

p = argparse.ArgumentParser()
p.add_argument('mapped_image', type=Path)
p.add_argument('output', type=Path)
a = p.parse_args()
data = a.mapped_image.read_bytes()
pe = pefile.PE(data=data)
extent = max([pe.OPTIONAL_HEADER.SizeOfHeaders] + [
    s.PointerToRawData + s.SizeOfRawData for s in pe.sections])
assert extent <= 64 * 1024 * 1024
result = bytearray(extent)
headers = pe.OPTIONAL_HEADER.SizeOfHeaders
result[:headers] = data[:headers]
for section in pe.sections:
    start = section.VirtualAddress
    size = section.SizeOfRawData
    assert start + size <= len(data)
    result[section.PointerToRawData:section.PointerToRawData + size] = data[start:start + size]
a.output.write_bytes(result)
print(hashlib.sha256(result).hexdigest())
