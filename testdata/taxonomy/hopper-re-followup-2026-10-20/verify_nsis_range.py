"""Replay the captured NSIS DLL-range arithmetic with independent field controls.

Only the 174-byte, hash-checked block runs in Unicorn. No APIs, host processes,
network, or sample entry point execute. The input is trace_nsis_remote.py output.
"""
import argparse
import hashlib
import json
import struct
from pathlib import Path

import unicorn
from unicorn.x86_const import UC_X86_REG_EBP, UC_X86_REG_ESP


def check(code, alignment, export_rva, raw_size):
    stage, frame, stack, dll = 0x1115c288, 0x200ffd00, 0x200ffcdc, 0x50080000
    uc = unicorn.Uc(unicorn.UC_ARCH_X86, unicorn.UC_MODE_32)
    uc.mem_map(0, 0x1000)
    uc.mem_map(0x11177000, 0x1000)
    uc.mem_map(0x200ff000, 0x1000)
    uc.mem_map(0x50020000, 0x70000)

    def put(address, value):
        uc.mem_write(address, struct.pack('<I', value))

    for address, value in [(0x30, 0x50020000), (0x5002000c, 0x50070000),
                           (0x50070014, 0x50071000), (0x50071000, 0x50072000),
                           (0x50072010, dll), (dll + 0x3c, 0x100),
                           (dll + 0x138, alignment), (dll + 0x178, export_rva),
                           (dll + 0x208, raw_size)]:
        put(address, value)
    uc.mem_write(stage + 0x1bca7, code)
    uc.reg_write(UC_X86_REG_EBP, frame)
    uc.reg_write(UC_X86_REG_ESP, stack)
    uc.emu_start(stage + 0x1bca7, stage + 0x1bd55, count=1000, timeout=1000000)
    get = lambda address: struct.unpack('<I', uc.mem_read(address, 4))[0]
    result = {'section_alignment': alignment, 'export_directory_rva': export_rva,
              'first_section_raw_size': raw_size, 'source_address': hex(get(stack + 4)),
              'saved_read_length': get(frame + 0x28), 'saved_raw_size': get(stack + 8)}
    assert get(stack + 4) == dll + alignment
    assert get(frame + 0x28) == export_rva
    assert get(stack + 8) == raw_size
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('trace', type=Path)
    ap.add_argument('--output', type=Path)
    args = ap.parse_args()
    report = json.loads(args.trace.read_text())
    assert report['stage_sha256'] == 'd87c43e225824a6aae3bb4613a448c66669e6b363d91b4fe144464fb67effc3b'
    code = bytes.fromhex(report['range_setup']['hex'])
    assert hashlib.sha256(code).hexdigest() == '7501ceded165373f48e8ed5a2e09d7a32183cb9d2031bb525a02792b26a3d474'
    rows = [check(code, *values) for values in [(0, 0, 0x1000), (0x1000, 0x2000, 0x1000),
            (0x2000, 0x2000, 0x1000), (0x1000, 0x3000, 0x1000), (0x1000, 0x2000, 0x800)]]
    result = {'verified': len(rows), 'cases': rows}
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
