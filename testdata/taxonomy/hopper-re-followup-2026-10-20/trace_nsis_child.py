"""Replay the copied NSIS loader entry in a bounded child-only CPU model.

The input is the sparse snapshot emitted at the exact parent bulk-copy boundary.
No sample or Windows DLL is loaded natively. The pointer overwrite, Windows
thread ABI, TEB/PEB values, stack and return address are synthetic fixtures.
"""
import argparse
import hashlib
import json
import struct
import time
from collections import deque
from pathlib import Path

import capstone
import pefile
import unicorn
from unicorn.x86_const import (
    UC_X86_REG_EAX, UC_X86_REG_EBP, UC_X86_REG_EBX, UC_X86_REG_ECX,
    UC_X86_REG_EDI, UC_X86_REG_EDX, UC_X86_REG_EFLAGS, UC_X86_REG_EIP,
    UC_X86_REG_ESI, UC_X86_REG_ESP,
)


COPY_BASE = 0x70000000
COPY_BYTES = 0x4000000
SOURCE_BASE = 0x10000000
SOURCE_STAGE = 0x1115C288
CHILD_STAGE = COPY_BASE + SOURCE_STAGE - SOURCE_BASE
ENTRY_OFFSET = 0xAF
ENTRY = CHILD_STAGE + ENTRY_OFFSET
THUNK_SLOT = 0x50083020
STACK_BASE = 0x20000000
STACK_BYTES = 0x200000
RETURN_SENTINEL = 0x3000F000
SAMPLE_SHA256 = 'b0860714c103ef1ba4287b84dee4158574f2c3244ae89f3824e9f80434db6114'
THREAD_START = 0x40352D


def api_hash(name):
    value = 5381
    for byte in name.encode():
        value = ((value * 33 + byte) ^ 1547477174) & 0xFFFFFFFF
    return value


API_NAMES = {api_hash(name): name for name in [
    'RtlAddVectoredExceptionHandler', 'NtAllocateVirtualMemory',
    'NtQueryVirtualMemory', 'ZwQueryVirtualMemory', 'NtProtectVirtualMemory',
    'NtSetInformationThread', 'EnumWindows', 'TerminateProcess', 'MessageBoxA',
    'LdrLoadDll', 'LdrGetProcedureAddress', 'NtQueryInformationProcess',
    'CreateProcessInternalW', 'InternetOpenA', 'InternetSetOptionA',
]}


class ModeledLowFault(Exception):
    pass


class PrivilegedFault(Exception):
    pass


PRIVILEGED = {'sysexit', 'sysret', 'lldt', 'ltr', 'mwait', 'monitor', 'lgdt',
              'lidt', 'lmsw', 'clts', 'invlpg', 'wbinvd', 'invd', 'vmptrld',
              'vmclear', 'vmxon', 'vmlaunch', 'vmresume', 'vmcall', 'in', 'out',
              'insb', 'insd', 'outsb', 'outsd', 'cli', 'sti', 'hlt', 'rdmsr', 'wrmsr'}


def load_snapshot(snapshot_dir):
    manifest = json.loads((snapshot_dir / 'copied-region-manifest.json').read_text())
    assert int(manifest['source_base'], 16) == SOURCE_BASE
    assert int(manifest['destination_base'], 16) == COPY_BASE
    assert manifest['virtual_bytes'] == COPY_BYTES
    pages = {}
    digest = hashlib.sha256()
    listed = {int(item['destination'], 16): item for item in manifest['nonzero_pages']}
    for address in range(COPY_BASE, COPY_BASE + COPY_BYTES, 4096):
        item = listed.get(address)
        if item is None:
            data = bytes(4096)
        else:
            data = (snapshot_dir / 'copied-region-pages' / f'{address:08x}.bin').read_bytes()
            assert len(data) == 4096
            assert any(data)
            assert hashlib.sha256(data).hexdigest() == item['sha256']
            pages[address] = data
        digest.update(data)
    assert len(pages) == len(listed)
    assert digest.hexdigest() == manifest['source_sha256']
    return manifest, pages


def run_case(pages, image, case, instruction_limit, seconds):
    uc = unicorn.Uc(unicorn.UC_ARCH_X86, unicorn.UC_MODE_32)
    uc.mem_map(COPY_BASE, COPY_BYTES, unicorn.UC_PROT_ALL)
    for address, data in pages.items():
        uc.mem_write(address, data)
    uc.mem_map(image['base'], image['mapped_bytes'], unicorn.UC_PROT_ALL)
    uc.mem_write(image['base'], image['data'])
    # Inherited from the parent's earlier synthetic NtMapViewOfSection result.
    # The true mshtml bytes are unavailable, so this remains zero-filled.
    uc.mem_map(0x600000, 0x20000, unicorn.UC_PROT_ALL)
    uc.mem_map(STACK_BASE, STACK_BYTES, unicorn.UC_PROT_READ | unicorn.UC_PROT_WRITE)
    uc.mem_map(0x30000000, 0x10000, unicorn.UC_PROT_ALL)
    uc.mem_write(RETURN_SENTINEL, b'\xcc')
    for module_base in {case.get('ntdll_base', 0x30008000),
                        case.get('kernel32_base', 0x30008000)}:
        if module_base != 0x30008000:
            uc.mem_map(module_base, 0x10000, unicorn.UC_PROT_ALL)
    # The slot is separate from the copied loader. Updating it here represents
    # the parent's pending four-byte remote write without changing parent state.
    uc.mem_map(THUNK_SLOT & ~4095, 4096, unicorn.UC_PROT_READ | unicorn.UC_PROT_WRITE)
    uc.mem_write(THUNK_SLOT, struct.pack('<I', ENTRY))
    # Minimal x86 TEB/PEB aliases used by this loader family. They are fixtures,
    # not values read from a host process.
    uc.mem_map(0, 4096, unicorn.UC_PROT_READ | unicorn.UC_PROT_WRITE)
    uc.mem_map(0x50000000, 0x10000, unicorn.UC_PROT_READ | unicorn.UC_PROT_WRITE)
    uc.mem_map(0x50020000, 0x10000, unicorn.UC_PROT_READ | unicorn.UC_PROT_WRITE)
    uc.mem_map(0x50090000, 0x5000, unicorn.UC_PROT_READ | unicorn.UC_PROT_WRITE)
    uc.mem_write(0x18, struct.pack('<I', 0x50000000))
    uc.mem_write(0x30, struct.pack('<I', 0x50020000))
    uc.mem_write(0x50000030, struct.pack('<I', 0x50020000))
    # PEB_LDR_DATA.InMemoryOrderModuleList -> first image entry. Relative to
    # that list-link pointer, +0x14 is the PE32 LDR entry's EntryPoint field.
    uc.mem_write(0x5002000C, struct.pack('<I', 0x50021000))
    uc.mem_write(0x50020010, struct.pack('<I', 0x50090000))
    uc.mem_write(0x50021014, struct.pack('<I', 0x50022008))
    uc.mem_write(0x5002201C, struct.pack('<I', case.get('peb_entry', THREAD_START)))
    def write_unicode(structure, address, value):
        encoded = value.encode('utf-16le')
        uc.mem_write(structure, struct.pack('<HHI', len(encoded), len(encoded) + 2, address))
        uc.mem_write(address, encoded + b'\0\0')
    write_unicode(0x50090038, 0x50092000, r'C:\triage\RFQ Fabrics.exe')
    write_unicode(0x50090040, 0x50093000, r'"C:\triage\RFQ Fabrics.exe"')
    uc.mem_write(0x50090048, struct.pack('<I', 0x50094000))

    sp = STACK_BASE + STACK_BYTES // 2
    uc.mem_write(sp, struct.pack('<II', RETURN_SENTINEL, case['argument']))
    for register, value in [
        (UC_X86_REG_EAX, case['eax']), (UC_X86_REG_EBX, case.get('ebx', 0)),
        (UC_X86_REG_ECX, case['ecx']), (UC_X86_REG_EDX, THREAD_START),
        (UC_X86_REG_ESI, case.get('esi', 0)), (UC_X86_REG_EDI, case.get('edi', 0)),
        (UC_X86_REG_EBP, 0),
        (UC_X86_REG_ESP, sp), (UC_X86_REG_EIP, ENTRY),
    ]:
        uc.reg_write(register, value)

    decoder = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
    started = time.monotonic()
    recent = deque(maxlen=96)
    initial = []
    milestones = []
    unique = set()
    low_writes = []
    count = 0
    stop = {'reason': None}
    events = []
    faults = []
    stubs = {}
    veh = False
    marker_skip = False
    window_call = None
    window_return = 0x3000E000
    alloc_next = 0x40000000
    sparse_reservations = []

    def read32(address):
        return struct.unpack('<I', uc.mem_read(address, 4))[0]

    def return_from_call(value, stack_arguments=0):
        current_sp = uc.reg_read(UC_X86_REG_ESP)
        target = read32(current_sp)
        uc.reg_write(UC_X86_REG_EAX, value)
        uc.reg_write(UC_X86_REG_ESP, current_sp + 4 + 4 * stack_arguments)
        uc.reg_write(UC_X86_REG_EIP, target)

    def stub_for(name_hash):
        for address, old_hash in stubs.items():
            if old_hash == name_hash:
                return address
        address = 0x30000000 + 16 * len(stubs)
        stubs[address] = name_hash
        return address

    def code_hook(model, address, size, user):
        nonlocal count, veh, alloc_next, marker_skip, window_call
        count += 1
        unique.add(address)
        recent.append({'address': hex(address),
                       'stage_offset': hex(address - CHILD_STAGE) if CHILD_STAGE <= address < CHILD_STAGE + 0x20000 else None})
        if len(initial) < 512:
            data = bytes(model.mem_read(address, min(size, 15)))
            insn = next(decoder.disasm(data, address, count=1), None)
            initial.append({**recent[-1], 'bytes': data.hex(),
                            'instruction': None if insn is None else insn.mnemonic + ' ' + insn.op_str})
        offset = address - CHILD_STAGE
        if address == window_return:
            assert window_call is not None
            assert model.reg_read(UC_X86_REG_ESP) == window_call['stack']
            window_call['completed'] += 1
            if model.reg_read(UC_X86_REG_EAX) == 0 or window_call['completed'] >= 12:
                completed = window_call['completed']
                window_call = None
                events.append({'assumption': 'EnumWindows callback sequence completed in the child CPU model',
                               'synthetic_windows': completed})
                return_from_call(1, 2)
            else:
                model.mem_write(window_call['stack'] - 12,
                                struct.pack('<III', window_return,
                                            0x70000 + window_call['completed'],
                                            window_call['parameter']))
                model.reg_write(UC_X86_REG_ESP, window_call['stack'] - 12)
                model.reg_write(UC_X86_REG_EIP, window_call['callback'])
            return
        if offset == 0x1D38B and not marker_skip:
            marker_skip = True
            model.reg_write(UC_X86_REG_ESI, 0x7FFFE000)
            events.append({'assumption': 'child process-memory marker scan has no match; middle iterations are omitted and the terminal iteration executes'})
        if offset in (0x205, 0x23A, 0xFC07, 0xFD59, 0x1AAFF) and not any(item['stage_offset'] == hex(offset) for item in milestones):
            current_sp = model.reg_read(UC_X86_REG_ESP)
            milestones.append({'stage_offset': hex(offset), 'registers': {
                'eax': hex(model.reg_read(UC_X86_REG_EAX)), 'ebx': hex(model.reg_read(UC_X86_REG_EBX)),
                'ecx': hex(model.reg_read(UC_X86_REG_ECX)), 'edx': hex(model.reg_read(UC_X86_REG_EDX)),
                'esi': hex(model.reg_read(UC_X86_REG_ESI)), 'edi': hex(model.reg_read(UC_X86_REG_EDI)),
                'esp': hex(current_sp), 'ebp': hex(model.reg_read(UC_X86_REG_EBP))},
                'stack': [hex(struct.unpack('<I', model.mem_read(current_sp + 4 * i, 4))[0]) for i in range(12)]})
        if address == CHILD_STAGE + 0x1B153:
            name_hash = read32(model.reg_read(UC_X86_REG_ESP) + 4)
            if name_hash == 0xF125414C:
                events.append({'module_hash': hex(name_hash),
                               'assumption': 'unidentified optional module is absent in the child model'})
                model.reg_write(UC_X86_REG_EBX, 0)
                return_from_call(0, 1)
                return
            module = ({0x35FDFBFF: case.get('ntdll_base', 0x30008000),
                       0x5EA5C095: case.get('kernel32_base', 0x30008000)}
                      .get(name_hash, 0x30008000))
            events.append({'module_hash': hex(name_hash), 'synthetic_module': hex(module)})
            model.reg_write(UC_X86_REG_EBX, module)
            return_from_call(module, 1)
            return
        if address == CHILD_STAGE + 0x1A839:
            name_hash = model.reg_read(UC_X86_REG_EDX)
            name = API_NAMES.get(name_hash, hex(name_hash))
            address = stub_for(name_hash)
            events.append({'resolved_api': name, 'hash': hex(name_hash), 'stub': hex(address)})
            return_from_call(address)
            return
        if address in stubs:
            name_hash = stubs[address]
            name = API_NAMES.get(name_hash, hex(name_hash))
            current_sp = model.reg_read(UC_X86_REG_ESP)
            arguments = [read32(current_sp + 4 + 4 * index) for index in range(8)]
            event = {'api': name, 'args': [hex(value) for value in arguments],
                     'return': hex(read32(current_sp))}
            events.append(event)
            if name == 'RtlAddVectoredExceptionHandler':
                veh = True
                event['assumption'] = 'synthetic vectored handler registration succeeds in the child CPU model'
                return_from_call(1, 2)
                return
            if name == 'NtAllocateVirtualMemory':
                process, base_pointer, _, size_pointer, allocation_type, protection = arguments[:6]
                requested = read32(size_pointer)
                if process == 0xFFFFFFFF and 0 < requested <= 0x1000000:
                    mapped = (requested + 4095) & ~4095
                    model.mem_map(alloc_next, mapped, unicorn.UC_PROT_ALL)
                    model.mem_write(base_pointer, struct.pack('<I', alloc_next))
                    model.mem_write(size_pointer, struct.pack('<I', mapped))
                    event['assumption'] = 'bounded current-process allocation succeeds in emulator memory only'
                    event['synthetic_allocation'] = {'address': hex(alloc_next), 'bytes': mapped}
                    alloc_next += mapped
                    return_from_call(0, 6)
                    return
                if process == 0xFFFFFFFF and requested == 0x2DBFF000:
                    reservation = {'base': 0x50100000, 'bytes': requested,
                                   'pages': set(), 'limit': 32 * 1024 * 1024}
                    sparse_reservations.append(reservation)
                    model.mem_write(base_pointer, struct.pack('<I', reservation['base']))
                    event['assumption'] = 'large allocation succeeds with bounded, zero-filled sparse child backing; execution is forbidden'
                    event['synthetic_allocation'] = {'address': hex(reservation['base']),
                                                     'virtual_bytes': requested,
                                                     'backing_limit': reservation['limit']}
                    return_from_call(0, 6)
                    return
            if name in ('NtQueryVirtualMemory', 'ZwQueryVirtualMemory'):
                address, output = arguments[1], arguments[3]
                region = next(((start, end) for start, end, _ in model.mem_regions()
                               if start <= address <= end), None)
                if region is not None:
                    start, end = region
                    model.mem_write(output, struct.pack('<7I', start, start, 0x40,
                                                        end - start + 1, 0x1000, 0x40, 0x20000))
                    event['assumption'] = 'MemoryBasicInformation describes the matching synthetic child mapping'
                    event['queried_address'] = hex(address)
                    return_from_call(0, 6)
                    return
                next_start = min((start for start, _, _ in model.mem_regions() if start > address),
                                 default=0x80000000)
                base = address & ~0xFFF
                model.mem_write(output, struct.pack('<7I', base, 0, 0,
                                                    next_start - base, 0x10000, 0, 0))
                event['assumption'] = 'MemoryBasicInformation reports an unmapped synthetic child interval as MEM_FREE'
                event['queried_address'] = hex(address)
                return_from_call(0, 6)
                return
            if name == 'NtProtectVirtualMemory':
                base_pointer, size_pointer, old_pointer = arguments[1], arguments[2], arguments[4]
                address, length = read32(base_pointer), read32(size_pointer)
                if any(start <= address and address + length <= end + 1
                       for start, end, _ in model.mem_regions()):
                    model.mem_write(old_pointer, struct.pack('<I', 0x20))
                    event['assumption'] = 'protection request succeeds on an existing synthetic child mapping'
                    return_from_call(0, 5)
                    return
            if name == 'EnumWindows':
                callback, parameter = arguments[:2]
                if CHILD_STAGE <= callback < CHILD_STAGE + 0x20000:
                    event['assumption'] = 'EnumWindows supplies 12 synthetic handles and executes the original callback in the CPU model'
                    window_call = {'stack': current_sp, 'callback': callback,
                                   'parameter': parameter, 'completed': 0}
                    model.mem_write(current_sp - 12,
                                    struct.pack('<III', window_return, 0x70000, parameter))
                    model.reg_write(UC_X86_REG_ESP, current_sp - 12)
                    model.reg_write(UC_X86_REG_EIP, callback)
                    return
            if name == 'NtSetInformationThread' and arguments[:4] == [0xFFFFFFFE, 0x11, 0, 0]:
                event['assumption'] = 'current-thread information class 0x11 succeeds in the synthetic child only'
                return_from_call(0, 4)
                return
            if name == 'NtQueryInformationProcess' and arguments[:2] == [0xFFFFFFFF, 7] and arguments[3:5] == [4, 0]:
                model.mem_write(arguments[2], struct.pack('<I', 0))
                event['assumption'] = 'current-process ProcessDebugPort query succeeds and returns zero in the child model'
                return_from_call(0, 5)
                return
            stop['reason'] = 'API stop: ' + name
            model.emu_stop()
            return
        opcode = bytes(model.mem_read(address, min(size, 15)))
        if opcode and opcode[0] in (15, 102, 242, 243, 228, 229, 230, 231,
                                    236, 237, 238, 239, 250, 251, 244):
            instruction = next(decoder.disasm(opcode, address, count=1), None)
            if instruction is not None and instruction.mnemonic in PRIVILEGED:
                raise PrivilegedFault(instruction.mnemonic)
        if address == RETURN_SENTINEL:
            stop['reason'] = 'returned to synthetic BaseThreadInitThunk caller'
            model.emu_stop()
        elif not COPY_BASE <= address < COPY_BASE + COPY_BYTES:
            stop['reason'] = f'control outside copied region: {address:#x}'
            model.emu_stop()
        elif count >= instruction_limit:
            stop['reason'] = 'instruction budget'
            model.emu_stop()
        elif time.monotonic() - started > seconds:
            stop['reason'] = 'wall-clock budget'
            model.emu_stop()

    invalid = []
    def invalid_hook(model, access, address, size, value, user):
        invalid.append({'access': access, 'address': hex(address), 'size': size,
                        'eip': hex(model.reg_read(UC_X86_REG_EIP))})
        if access in (unicorn.UC_MEM_READ_UNMAPPED, unicorn.UC_MEM_WRITE_UNMAPPED):
            for reservation in sparse_reservations:
                if reservation['base'] <= address < address + size <= reservation['base'] + reservation['bytes']:
                    pages = set(range(address & ~4095, (address + size + 4095) & ~4095, 4096))
                    pages -= reservation['pages']
                    if (len(reservation['pages']) + len(pages)) * 4096 > reservation['limit']:
                        return False
                    for page in sorted(pages):
                        model.mem_map(page, 4096, unicorn.UC_PROT_READ | unicorn.UC_PROT_WRITE)
                        reservation['pages'].add(page)
                    return True
        return False

    def low_write_hook(model, access, address, size, value, user):
        if len(low_writes) < 128:
            low_writes.append({'address': hex(address), 'size': size, 'value': hex(value),
                               'eip': hex(model.reg_read(UC_X86_REG_EIP)),
                               'stage_offset': hex(model.reg_read(UC_X86_REG_EIP) - CHILD_STAGE)})

    def low_access_hook(model, access, address, size, value, user):
        if access == unicorn.UC_MEM_READ:
            pc = model.reg_read(UC_X86_REG_EIP)
            if address in (0x18, 0x30, 0xC0) and size == 4 and bytes(model.mem_read(pc, 1)) == b'\x64':
                return
        raise ModeledLowFault(f'modeled inaccessible low address {address:#x}')

    uc.hook_add(unicorn.UC_HOOK_CODE, code_hook)
    uc.hook_add(unicorn.UC_HOOK_MEM_INVALID, invalid_hook)
    uc.hook_add(unicorn.UC_HOOK_MEM_WRITE, low_write_hook, begin=0, end=4095)
    uc.hook_add(unicorn.UC_HOOK_MEM_READ | unicorn.UC_HOOK_MEM_WRITE,
                low_access_hook, begin=0, end=0xFFFF)
    for _ in range(20000):
        try:
            uc.emu_start(uc.reg_read(UC_X86_REG_EIP), COPY_BASE + COPY_BYTES,
                         timeout=seconds * 1000000, count=max(1, instruction_limit - count))
            if stop['reason'] is None:
                stop['reason'] = 'emulator ended without explicit stop'
            break
        except (unicorn.UcError, ModeledLowFault, PrivilegedFault) as error:
            pc = uc.reg_read(UC_X86_REG_EIP)
            if isinstance(error, unicorn.UcError) and error.errno == unicorn.UC_ERR_EXCEPTION:
                fault_pc = int(recent[-1]['address'], 16)
                if bytes(uc.mem_read(fault_pc, 1)) == b'\xcc':
                    pc = fault_pc
                elif uc.reg_read(UC_X86_REG_EFLAGS) & 0x100:
                    uc.reg_write(UC_X86_REG_EFLAGS, uc.reg_read(UC_X86_REG_EFLAGS) & ~0x100)
                else:
                    stop['reason'] = str(error)
                    break
            if (isinstance(error, unicorn.UcError) and
                    error.errno in (unicorn.UC_ERR_READ_UNMAPPED, unicorn.UC_ERR_WRITE_UNMAPPED) and
                    (not invalid or int(invalid[-1]['address'], 16) > 0x10000)):
                stop['reason'] = 'unmodeled memory access above VEH range: ' + str(error)
                break
            modeled_exception = isinstance(error, (ModeledLowFault, PrivilegedFault)) or (
                isinstance(error, unicorn.UcError) and error.errno in
                (unicorn.UC_ERR_READ_UNMAPPED, unicorn.UC_ERR_WRITE_UNMAPPED,
                 unicorn.UC_ERR_INSN_INVALID, unicorn.UC_ERR_EXCEPTION))
            if not veh or not modeled_exception or not CHILD_STAGE <= pc < CHILD_STAGE + 0x20000:
                stop['reason'] = str(error)
                break
            skip = bytes(uc.mem_read(pc + 20, 1))[0] ^ 25
            if not 0 < skip < 256:
                stop['reason'] = 'invalid modeled VEH skip'
                break
            faults.append({'stage_offset': hex(pc - CHILD_STAGE), 'skip': skip,
                           'error': str(error), 'invalid_memory': invalid[-1:]})
            uc.reg_write(UC_X86_REG_EIP, pc + skip)
    else:
        stop['reason'] = 'exception budget'

    registers = {name: hex(uc.reg_read(register)) for name, register in [
        ('eax', UC_X86_REG_EAX), ('ebx', UC_X86_REG_EBX),
        ('ecx', UC_X86_REG_ECX), ('edx', UC_X86_REG_EDX),
        ('esi', UC_X86_REG_ESI), ('edi', UC_X86_REG_EDI),
        ('esp', UC_X86_REG_ESP), ('ebp', UC_X86_REG_EBP),
        ('eip', UC_X86_REG_EIP), ('eflags', UC_X86_REG_EFLAGS),
    ]}
    return {'case': case, 'reason': stop['reason'], 'instructions': count,
            'unique_instruction_addresses': len(unique), 'invalid_memory': invalid,
            'events': events, 'faults': faults,
            'sparse_reservations': [{'base': hex(item['base']), 'virtual_bytes': item['bytes'],
                                     'backed_pages': len(item['pages'])}
                                    for item in sparse_reservations],
            'exception_chain_head': hex(struct.unpack('<I', uc.mem_read(0, 4))[0]),
            'low_memory_writes': low_writes,
            'registers': registers, 'recent': list(recent),
            'initial': initial, 'milestones': milestones,
            'pointer_overwrite': {'address': hex(THUNK_SLOT),
                                  'parent_read_fixture': '0x30000220',
                                  'value_applied_before_child_entry': hex(ENTRY),
                                  'after_child_trace': hex(struct.unpack('<I', uc.mem_read(THUNK_SLOT, 4))[0])}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--snapshot-dir', type=Path, required=True)
    parser.add_argument('--sample', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--instruction-limit', type=int, default=250000)
    parser.add_argument('--seconds-per-case', type=int, default=15)
    parser.add_argument('--case', choices=['all', 'main-thread-peb'], default='all')
    args = parser.parse_args()
    manifest, pages = load_snapshot(args.snapshot_dir)
    sample = args.sample.read_bytes()
    assert hashlib.sha256(sample).hexdigest() == SAMPLE_SHA256
    pe = pefile.PE(data=sample, fast_load=False)
    assert pe.OPTIONAL_HEADER.ImageBase == 0x400000
    assert pe.OPTIONAL_HEADER.ImageBase + pe.OPTIONAL_HEADER.AddressOfEntryPoint == THREAD_START
    image_data = pe.get_memory_mapped_image(ImageBase=pe.OPTIONAL_HEADER.ImageBase)
    mapped_bytes = (pe.OPTIONAL_HEADER.SizeOfImage + 4095) & ~4095
    assert len(image_data) <= mapped_bytes
    image = {'base': pe.OPTIONAL_HEADER.ImageBase, 'mapped_bytes': mapped_bytes,
             'data': image_data, 'size_of_image': pe.OPTIONAL_HEADER.SizeOfImage}
    cases = [
        {'name': 'main-thread-peb', 'ecx': 0, 'eax': 0, 'argument': 0x50020000},
        {'name': 'non-main-thread-control', 'ecx': 0, 'eax': 0,
         'peb_entry': 0x404000, 'argument': 0x50020000},
        {'name': 'aligned-module-base-control', 'ecx': 0, 'eax': 0,
         'ntdll_base': 0x77000000, 'kernel32_base': 0x76000000,
         'argument': 0x50020000},
        {'name': 'parent-register-control', 'ecx': 0, 'eax': CHILD_STAGE, 'ebx': CHILD_STAGE,
         'esi': 0x786C749A, 'edi': 127004, 'argument': 0x50020000},
        {'name': 'magic-eax-control', 'ecx': 0, 'eax': 0xB2609734, 'argument': 0x50020000},
    ]
    if args.case != 'all':
        cases = [case for case in cases if case['name'] == args.case]
    results = [run_case(pages, image, case, args.instruction_limit, args.seconds_per_case)
               for case in cases]
    report = {
        'method': 'Fresh Unicorn x86 instances replay exact nonzero copy-time pages; omitted copied pages are zero.',
        'limits': ['The BaseThreadInitThunk call context is a documented-shape synthetic ABI fixture; volatile registers are not recovered.',
                   'The child TEB/PEB, original thread start, argument, return address and overwritten ntdll slot are synthetic.',
                   'No native sample, DLL, process, thread or API executes.'],
        'snapshot': {'sha256': manifest['source_sha256'],
                     'virtual_bytes': manifest['virtual_bytes'],
                     'nonzero_pages': len(pages)},
        'child_image': {'sha256': SAMPLE_SHA256, 'image_base': hex(image['base']),
                        'size_of_image': hex(image['size_of_image']),
                        'entry_point': hex(THREAD_START)},
        'synthetic_mshtml_mapping': {'base': '0x600000', 'bytes': 0x20000,
                                     'contents': 'zero-filled; actual DLL unavailable'},
        'addresses': {'copied_base': hex(COPY_BASE), 'child_stage': hex(CHILD_STAGE),
                      'loader_entry': hex(ENTRY), 'stage_offset': hex(ENTRY_OFFSET),
                      'thread_init_slot': hex(THUNK_SLOT),
                      'synthetic_image_entry_point': hex(THREAD_START)},
        'cases': results,
    }
    args.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'snapshot': report['snapshot'], 'cases': [
        {'name': item['case']['name'], 'reason': item['reason'],
         'instructions': item['instructions'], 'eip': item['registers']['eip'],
         'invalid_memory': item['invalid_memory'][-1:]}
        for item in results]}, indent=2))
    return report


if __name__ == '__main__':
    main()
