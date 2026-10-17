"""IoT ELF staging the ARM XMRig miner with pool and donate flag.

Run: python3 testdata/iot-xmrig-arm-stager/verify.py <scratch-directory>

IoT botnets (e.g. the catstorm Mirai variant) pack their miner stage
markers into concatenated string tables -- ``tcp-stompxmrig-armMemTotal``
-- where the word matcher for ``xmrig`` and the ``.text``-scoped
``donate-level`` matcher both miss. The staged release name plus a
Stratum endpoint plus the donate CLI flag is still a configured miner
invocation, which ``staged-arm-xmrig-stratum-miner`` convicts.

Controls: a minimal ELF32 ARM image carrying all three markers must
report the hostile; the miner name alone, and pool plus donate flag
without the miner name, must not.
"""
import json
import os
import struct
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STAGER = ('objectives/impact/cryptojacking/miner/runtime::'
          'staged-arm-xmrig-stratum-miner')

FULL_MARKERS = (
    'tcp-stompxmrig-armMemTotal:',
    'stratum+tcp://pool.example:3333',
    '--donate-level=1',
)
NAME_ONLY = ('xmrig-arm',)
POOL_ONLY = (
    'stratum+tcp://pool.example:3333',
    '--donate-level=1',
)


def build_elf(rodatas):
    """Minimal ELF32 ARM with marker strings inside .rodata."""
    blob = bytearray()
    for s in rodatas:
        blob += s.encode('ascii') + b'\x00'
    blob = bytes(blob)
    # Pad past small-file size gates (e.g. the miner name's size_min).
    while len(blob) < 1024:
        blob += b'\x00' * 64
    shstr = b'\x00.rodata\x00.shstrtab\x00'

    ehsize, shentsize, shnum = 52, 40, 3
    off_rodata = ehsize
    off_shstr = off_rodata + len(blob)
    shoff = off_shstr + len(shstr)

    eh = struct.pack(
        '<16sHHIIIIIHHHHHH',
        b'\x7fELF\x01\x01\x01' + b'\x00' * 9,
        2, 40, 1, 0, 0, shoff, 0, ehsize, 0, 0, shentsize, shnum, 2)

    def sh(name, stype, flags, addr, off, size, link=0, info=0,
           align=1, entsize=0):
        return struct.pack('<IIIIIIIIII', name, stype, flags, addr, off,
                           size, link, info, align, entsize)

    sh0 = sh(0, 0, 0, 0, 0, 0)
    sh1 = sh(1, 1, 2, 0, off_rodata, len(blob))
    sh2 = sh(9, 3, 0, 0, off_shstr, len(shstr))

    return eh + blob + shstr + sh0 + sh1 + sh2


def scan(path):
    result = subprocess.run(
        [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
         '--format', 'json', str(path)],
        env=dict(os.environ, CLEAVE_VALIDATE='0'),
        text=True, capture_output=True, check=True)
    report = json.loads(result.stdout)
    return {t['id'] for entry in report['files'] for t in entry['traits']}


def main():
    dest = Path(sys.argv[1])
    dest.mkdir(parents=True, exist_ok=True)

    positive = dest / 'miner-stage-positive.elf'
    positive.write_bytes(build_elf(FULL_MARKERS))
    ids = scan(positive)
    assert STAGER in ids, 'staged miner markers must convict'
    print('PASS miner-stage-positive.elf', flush=True)

    negative = dest / 'miner-name-only.elf'
    negative.write_bytes(build_elf(NAME_ONLY))
    ids = scan(negative)
    assert STAGER not in ids, 'miner name alone must not convict'
    print('PASS miner-name-only.elf', flush=True)

    pool_only = dest / 'pool-without-miner.elf'
    pool_only.write_bytes(build_elf(POOL_ONLY))
    ids = scan(pool_only)
    assert STAGER not in ids, 'pool without miner must not convict'
    print('PASS pool-without-miner.elf', flush=True)


if __name__ == '__main__':
    main()
