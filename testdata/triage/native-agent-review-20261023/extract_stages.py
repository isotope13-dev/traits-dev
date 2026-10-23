"""Recover the reviewed AutoIt and Go stages without executing sample code.
Usage: extract_stages.py <IconLib.dll> <Go-loader.exe> <scratch-dir>
Requires pefile and autoit-ripper (already present in the lab).
"""
import hashlib
import importlib
import json
from pathlib import Path
import re
import sys

import pefile
from autoit_ripper import extract

carrier, loader, output = map(Path, sys.argv[1:])
output.mkdir(parents=True, exist_ok=True)
# The real EA06 script expands to 12,671,157 bytes, above the ripper's default
# 10 MB ceiling. Its deassembled UTF-8 representation is smaller.
importlib.import_module('autoit_ripper.decompress').MAX_SCRIPT_SIZE = 30000000
records = []
for index, (name, data) in enumerate(extract(carrier.read_bytes()) or []):
    script = output / f'autoit-{index}.au3'
    script.write_bytes(data)
    records.append({'path': str(script), 'source_name': name, 'sha256': hashlib.sha256(data).hexdigest()})
    if name == 'script.au3':
        source = data.decode()
        # The reviewed script's initial $X assignments are a hex PE; later
        # globals bind DllCall and DllStruct helpers used by the RunPE path.
        initial = source[:source.index('Global')]
        joined = ''.join(re.findall(r'"([0-9a-fA-Fx]+)"', initial))
        payload = bytes.fromhex(joined[2:])
        pefile.PE(data=payload)
        path = output / 'autoit-runpe-payload.exe'
        path.write_bytes(payload)
        records.append({'path': str(path), 'sha256': hashlib.sha256(payload).hexdigest()})

image = pefile.PE(str(loader))
# Addresses and constants below are extraction evidence for this build,
# not classifier indicators. main.arJGDJ at VA 0x593160 returns this buffer.
length = 0x522b7
buffer = bytearray(bytes.fromhex('5b57816f70947c9b')[:7] +
                   image.get_data(0x5f386d - image.OPTIONAL_HEADER.ImageBase, length - 7))
buffer = bytearray((value - 31 * index - 14) & 255 for index, value in enumerate(buffer))
buffer.reverse()
buffer = bytearray((value - 13 * index - 123) & 255 for index, value in enumerate(buffer))
for index in range(0, len(buffer) - 1, 2):
    buffer[index], buffer[index + 1] = buffer[index + 1], buffer[index]
payload = bytes((value - 7 * index - 47) & 255 for index, value in enumerate(buffer))
pefile.PE(data=payload)
path = output / 'go-mapped-payload.exe'
path.write_bytes(payload)
records.append({'path': str(path), 'sha256': hashlib.sha256(payload).hexdigest()})
(output / 'extraction.json').write_text(json.dumps(records, indent=2) + '\n')
print(json.dumps(records, indent=2))
