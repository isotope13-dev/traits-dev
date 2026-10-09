#!/usr/bin/env python3
"""Safely emulate the DOS sample with fake DOS calls and no filesystem I/O."""
import sys
from pathlib import Path
from unicorn import Uc, UC_ARCH_X86, UC_MODE_16, UC_HOOK_INTR
from unicorn.x86_const import *

body = Path(sys.argv[1]).read_bytes()
for failure in (None, 0x4e, 0x5b):
    machine = Uc(UC_ARCH_X86, UC_MODE_16)
    machine.mem_map(0, 0x100000)
    base = 0x10000
    machine.mem_write(base, b'\xcd\x20')
    machine.mem_write(base + 0x100, body)
    machine.mem_write(base + 0xfffc, b'\x00\x00')
    for register in (UC_X86_REG_CS, UC_X86_REG_DS, UC_X86_REG_ES, UC_X86_REG_SS):
        machine.reg_write(register, 0x1000)
    machine.reg_write(UC_X86_REG_SI, 0x100)
    machine.reg_write(UC_X86_REG_DI, 0xfffe)
    machine.reg_write(UC_X86_REG_SP, 0xfffc)
    events = []
    def c_string(address):
        return bytes(machine.mem_read(address, 128)).split(b'\0', 1)[0]
    def interrupt(_, number, unused):
        if number == 0x20:
            machine.emu_stop()
            return
        assert number == 0x21, hex(number)
        ax = machine.reg_read(UC_X86_REG_AX)
        service = ax >> 8
        address = base + machine.reg_read(UC_X86_REG_DX)
        flags = machine.reg_read(UC_X86_REG_EFLAGS)
        machine.reg_write(UC_X86_REG_EFLAGS, (flags & ~1) | (service == failure))
        if service == 0:
            machine.emu_stop()
        elif service == 0x4e:
            events.append(('search', c_string(address)))
            machine.mem_write(base + 0x9e, b'HOST.EXE\0')
        elif service == 0x5b:
            name = c_string(address)
            repeated = any(event[0] == 'create-new' for event in events)
            events.append(('create-new', name))
            machine.reg_write(UC_X86_REG_AX, 3 if repeated else 5)
            if repeated:
                machine.reg_write(UC_X86_REG_EFLAGS, flags | 1)
        elif service == 0x40:
            length = machine.reg_read(UC_X86_REG_CX)
            data = bytes(machine.mem_read(address, length))
            assert machine.reg_read(UC_X86_REG_BX) == 5
            assert data == (body + bytes(65536))[:length], (length, hex(address), data[:48].hex())
            events.append(('write-own-image', length))
            machine.reg_write(UC_X86_REG_AX, length)
        else:
            raise AssertionError(hex(service))
    machine.hook_add(UC_HOOK_INTR, interrupt)
    machine.emu_start(base + 0x100, base + 0x10000, count=200000)
    writes = [event for event in events if event[0] == 'write-own-image']
    assert len(writes) == (failure is None), events
    if failure is None:
        assert events[1][0] == 'create-new' and events[1][1].upper() == b'HOST.COM', events
        if body[4:7] == b'COM':
            assert writes[0][1] == 43
    print('failure=' + str(failure), events)
