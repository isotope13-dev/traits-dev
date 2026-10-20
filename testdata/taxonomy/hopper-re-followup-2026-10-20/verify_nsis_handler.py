#!/usr/bin/env python3
"""Check the recovered handler in a bounded, CPU-only Unicorn model.

Requires unicorn. No Windows APIs, native sample launch, or network access.
Input is the exact Signs archive member, not an arbitrary executable.
"""
import argparse
import hashlib
import json
import struct
from pathlib import Path

import unicorn
from unicorn.x86_const import UC_X86_REG_EAX, UC_X86_REG_EBP, UC_X86_REG_ESP


def check(stage, exception, pc, address=0, debug_register=0):
    base, arena, stop = 0x10000000, 0x20000000, 0x2000F000
    uc = unicorn.Uc(unicorn.UC_ARCH_X86, unicorn.UC_MODE_32)
    uc.mem_map(base, 0x20000)
    uc.mem_write(base, stage)
    uc.mem_map(arena, 0x10000)
    pointers, record, context, stack = [arena + x for x in (0x100, 0x200, 0x400, 0x8000)]

    def write32(at, value):
        uc.mem_write(at, struct.pack("<I", value))

    write32(pointers, record)
    write32(pointers + 4, context)
    write32(record, exception)
    write32(record + 0x18, address)
    write32(context + 4, debug_register)
    write32(context + 0xB8, base + pc)
    write32(stack, stop)
    write32(stack + 4, pointers)
    uc.reg_write(UC_X86_REG_ESP, stack)
    uc.emu_start(base + 0x1E37B, stop, timeout=1_000_000, count=1000)
    result = uc.reg_read(UC_X86_REG_EAX)
    after = struct.unpack("<I", uc.mem_read(context + 0xB8, 4))[0] - base
    return result, after


def check_api_hash(stage, name):
    base, arena, stop = 0x10000000, 0x20000000, 0x2000F000
    uc = unicorn.Uc(unicorn.UC_ARCH_X86, unicorn.UC_MODE_32)
    uc.mem_map(base, 0x20000)
    uc.mem_write(base, stage)
    uc.mem_map(arena, 0x10000)
    uc.mem_write(arena + 0x8000, struct.pack("<II", stop, arena + 0x400))
    uc.mem_write(arena + 0x400, name.encode("ascii") + b"\0")
    uc.reg_write(UC_X86_REG_EBP, arena + 0x1000)
    uc.reg_write(UC_X86_REG_ESP, arena + 0x8000)
    uc.emu_start(base + 0x1D9BF, stop, timeout=1_000_000, count=10000)
    return uc.reg_read(UC_X86_REG_EAX)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("signs", type=Path)
    ap.add_argument("--output", type=Path)
    args = ap.parse_args()
    signs = args.signs.read_bytes()
    assert hashlib.sha256(signs).hexdigest() == (
        "1fa1c481c9bc28824a93dee673a5a5afeb4f0497cc4758120938cf7b5ec546a3"
    )
    key = struct.pack("<I", 0x786C749A)
    stage = bytes(c ^ key[i % 4] for i, c in enumerate(signs[0x4403:0x2341F]))
    assert hashlib.sha256(stage).hexdigest() == (
        "d87c43e225824a6aae3bb4613a448c66669e6b363d91b4fe144464fb67effc3b"
    )
    rows = []
    for code in (0xC0000005, 0xC000001D, 0xC0000096, 0x80000003, 0x80000004):
        pc = 0xF834
        result, after = check(stage, code, pc)
        assert result == 0xFFFFFFFF and after == pc + (stage[pc + 20] ^ 0x19)
        rows.append({"exception": hex(code), "before": hex(pc), "after": hex(after)})
    result, after = check(stage, 0xC0000005, 0xF834, address=0x10001)
    assert result == 0 and after == 0xF834
    result, after = check(stage, 0xDEADBEEF, 0xF834)
    assert result == 0 and after == 0xF834
    # The debug-register branch returns zero from a nested helper. Its caller
    # subsequently dereferences that value; it does not cleanly return SEARCH.
    try:
        check(stage, 0xC0000005, 0xF834, debug_register=1)
    except unicorn.UcError as error:
        assert error.errno == unicorn.UC_ERR_READ_UNMAPPED
    else:
        raise AssertionError("Expected the nonzero-Dr0 handler failure")
    hashes = {
        "RtlAddVectoredExceptionHandler": 0xED858285,
        "NtAllocateVirtualMemory": 0x88605FC6,
        "TerminateProcess": 0xAFF81EDD,
        "MessageBoxA": 0x299B7EEE,
        "ZwQueryVirtualMemory": 0x44209F30,
    }
    for name, expected in hashes.items():
        assert check_api_hash(stage, name) == expected, name
    report = {
        "handler_offset": "0x1e37b",
        "model": "CPU-only handler invocation with synthetic exception/context structures",
        "transformation": "Context.Eip += byte(Context.Eip + 20) XOR 0x19",
        "accepted_cases": rows,
        "rejected_controls": ["access above 0x10000", "unsupported exception code"],
        "debug_control": "Nonzero Dr0 causes an unmapped read in this handler model",
        "api_hash_routine_offset": "0x1d9bf",
        "verified_api_hashes": {name: hex(value) for name, value in hashes.items()},
    }
    if args.output:
        args.output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
