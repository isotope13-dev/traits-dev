#!/usr/bin/env python3
"""RGB API names remain neutral; harvesting requires byte-array code.

These synthetic PE controls replace a retired external-sample test that
incorrectly treated RGB API names as proof of byte collection. A triple
getter-to-byte-array shape is independent evidence; no API token alone
can substitute for it.
"""
import importlib.util
from pathlib import Path
import sys

root = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location(
    'pico_controls', root / 'testdata/picoscope-suite-context/verify.py')
pico = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pico)
dest = Path(sys.argv[1])
dest.mkdir(parents=True, exist_ok=True)
shape = bytes.fromhex(
    '19 8D 01 00 00 01 25 16 12 06 28 01 00 00 0A 9C '
    '25 17 12 06 28 02 00 00 0A 9C '
    '25 18 12 06 28 03 00 00 0A 9C 6F 04 00 00 0A')
base = pico.build_pe(pico.DOTNET_IMPORTS, pico.STEGO_STRINGS)
for label, blob, expected in [
    ('api-only', base, False),
    ('byte-array', base[:0x500] + shape + base[0x500 + len(shape):], True),
    ('missing-array-store', base[:0x500] + shape.replace(b'\x9c', b'\x00')
     + base[0x500 + len(shape):], False),
]:
    target = dest / (label + '.exe')
    target.write_bytes(blob)
    found = pico.scan(target)
    assert pico.DECOMPOSITION in found, (label, 'RGB profile missing')
    assert (pico.RED_CHANNEL in found) == expected, label
    assert not any('dotnet-red-channel-stego-reflective-loader' in t
                   for t in found), label
    print('PASS', label, flush=True)
