#!/usr/bin/env python3
"""Transcribe static string transforms; never loads or executes sample classes.

Input is the trusted CFR text output for be1bac242554. The final two XOR keys
are inferred from coherent URL/filename pairs because the outer helper is absent.
"""
import json
import re
import sys
from pathlib import Path

source = Path(sys.argv[1]).read_text()
static = source[source.index('    static {'):source.index('    private static String')]
literals = re.findall(r'(?:String )?string = ("(?:\\.|[^"\\])*");', static)
assert len(literals) == 2
blobs = [json.loads(s) for s in literals]
table = []
for blob, length in zip(blobs, [24, 71]):
    pos = 0
    while pos < len(blob):
        chunk = blob[pos:pos + length]
        assert len(chunk) == length
        table.append([ord(c) ^ [28, 16, 80, 74, 120, 43, 86][i % 7]
                      for i, c in enumerate(chunk)])
        pos += length
        if pos == len(blob):
            break
        length = ord(blob[pos])
        pos += 1
assert len(table) == 8
switch = source[source.index('switch (cArray[0] & 0xFF)'):]
seeds = {int(a): int(b) for a, b in re.findall(r'case (\d+):\s*\{\s*n3 = (\d+);', switch)}
calls = [(32167, 21200), (32163, -20565), (32165, -9897), (32160, -32698),
         (32162, -14997), (32166, 9188), (32161, -21771), (32164, -22541)]
values = []
for index, operand in calls:
    chars = table[(index ^ 0x7DA1) & 65535]
    seed = seeds.get(chars[0] & 255, 51)
    keys = [((operand & 255) - seed) & 255, (((operand & 65535) >> 8) - seed) & 255]
    decoded = []
    for i, char in enumerate(chars):
        slot = i % 2
        plain = char ^ keys[slot]
        decoded.append(plain)
        keys[slot] = ((keys[slot] >> 3 | keys[slot] << 5) ^ plain) & 255
    value = ''.join(chr(c ^ [4, 112][(len(decoded) - 1 - i) % 2])
                    for i, c in enumerate(decoded))
    values.append(value)
assert all(v.startswith('https://') for v in values[:4]), values
assert all(v.endswith('.jar') for v in values), values
print(json.dumps({'method': 'Static table transform and inferred alternating outer XOR keys 4/112',
                  'values': values}, indent=2))
