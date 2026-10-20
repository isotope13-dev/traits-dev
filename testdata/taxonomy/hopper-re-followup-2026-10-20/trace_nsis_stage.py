"""Bounded CPU trace with synthetic module/API returns; no host API execution.

Requires Unicorn and Capstone. Only the exact hash-checked Signs member is read.
Module and API lookup are modeled, not executed. Allocation affects emulator
memory only. By default all other APIs stop the trace; the explicitly selected
mapped-memory model adds query/protection responses and an absent-module branch. Limits: 5 million instructions,
120 seconds, 20,000 exception transitions, 32 MiB of modeled allocations.
The optional no-marker branch is an explicit assumption, not observed behavior.
Instruction-byte reads are capped at 15: Unicorn can report sentinel sizes
for unsupported privileged opcodes.
Breakpoint EIP normalization and single-step flag clearing are corroborated by:
https://github.com/wine-mirror/wine/blob/master/dlls/ntdll/unix/signal_i386.c
"""
import argparse, hashlib, json, collections, struct, time
from pathlib import Path
import unicorn, capstone
from unicorn.x86_const import *
ap = argparse.ArgumentParser(description=__doc__)
ap.add_argument('--audit-root', type=Path, required=True)
ap.add_argument('--output-dir', type=Path, required=True)
ap.add_argument('--model-mapped-memory', action='store_true', help='Conditional synthetic memory-query/protection model and absent optional module; used by the mixed-mode driver.')
ap.add_argument('--assume-no-memory-marker', action='store_true', help='Explore a conditional path; explicitly assumes the memory-marker scan returns no match.')
args = ap.parse_args()
assume_no_marker = args.assume_no_memory_marker
root = args.audit_root / 're/nsis'
output = args.output_dir
output.mkdir(parents=True, exist_ok=True)
d = (root / 'Signs').read_bytes()
assert hashlib.sha256(d).hexdigest() == '1fa1c481c9bc28824a93dee673a5a5afeb4f0497cc4758120938cf7b5ec546a3'
key = struct.pack('<I', 2020373658)
code = bytes((c ^ key[i % 4] for i, c in enumerate(d[17411:144415])))
assert hashlib.sha256(code).hexdigest() == 'd87c43e225824a6aae3bb4613a448c66669e6b363d91b4fe144464fb67effc3b'
base = 268435456
stage = base + 17411 + 18185861
u = unicorn.Uc(unicorn.UC_ARCH_X86, unicorn.UC_MODE_32)
u.mem_map(base, 67108864)
u.mem_write(base, d)
u.mem_write(stage, code)
u.mem_map(536870912, 2097152)
sp = 537919488
u.mem_write(sp, (base + 17227).to_bytes(4, 'little'))
u.reg_write(UC_X86_REG_ESP, sp)
u.mem_map(805306368, 65536)
for r, v in [(UC_X86_REG_EAX, stage), (UC_X86_REG_EBX, stage), (UC_X86_REG_ESI, 2020373658), (UC_X86_REG_EDI, 127004), (UC_X86_REG_EDX, 127004)]:
    u.reg_write(r, v)
last = collections.deque(maxlen=40)
count = 0
events = []
stubs = {}
faults = []
bad_memory = None
veh = False
alloc_next = 1073741824
names = {}

def hashname(s):
    x = 5381
    for c in s.encode():
        x = (x * 33 + c ^ 1547477174) & 4294967295
    return x
for name in ['ExitProcess', 'NtGetContextThread', 'NtSetContextThread', 'ZwGetContextThread', 'ZwSetContextThread', 'NtQueryInformationThread', 'ZwQueryInformationThread', 'RtlRestoreContext', 'LdrInitializeThunk', 'NtRaiseException', 'RtlRaiseException', 'TerminateProcess', 'MessageBoxA', 'RtlAddVectoredExceptionHandler', 'RtlRemoveVectoredExceptionHandler', 'RtlAddVectoredContinueHandler', 'NtProtectVirtualMemory', 'NtAllocateVirtualMemory', 'NtQueryVirtualMemory', 'NtContinue', 'NtSetInformationProcess', 'RtlMoveMemory', 'RtlFillMemory', 'RtlZeroMemory', 'NtCreateSection', 'NtMapViewOfSection', 'LdrLoadDll', 'LdrGetProcedureAddress', 'RtlGetVersion', 'NtQueryInformationProcess', 'RtlExitUserThread', 'KiUserExceptionDispatcher', 'NtFreeVirtualMemory', 'NtFlushInstructionCache']:
    names[hashname(name)] = name
    if name.startswith('Nt'):
        names[hashname('Zw' + name[2:])] = 'Zw' + name[2:]

class Stop(Exception):
    pass

class PrivilegedFault(Exception):
    errno = unicorn.UC_ERR_INSN_INVALID
privileged_names = {'lldt', 'ltr', 'mwait', 'monitor', 'lgdt', 'lidt', 'lmsw', 'clts', 'invlpg', 'wbinvd', 'invd', 'vmptrld', 'vmclear', 'vmxon', 'vmlaunch', 'vmresume', 'vmcall', 'in', 'out', 'insb', 'insd', 'outsb', 'outsd', 'cli', 'sti', 'hlt', 'rdmsr', 'wrmsr'}
dis = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
started = time.monotonic()

def r32(addr):
    return struct.unpack('<I', u.mem_read(addr, 4))[0]

def ret(value, n=0):
    sp = u.reg_read(UC_X86_REG_ESP)
    target = r32(sp)
    u.reg_write(UC_X86_REG_EAX, value)
    u.reg_write(UC_X86_REG_ESP, sp + 4 + 4 * n)
    u.reg_write(UC_X86_REG_EIP, target)

def stub(h):
    name = names.get(h, hex(h))
    addr = 805306368 + len(stubs) * 16
    for a, (old, _) in stubs.items():
        if old == h:
            return a
    stubs[addr] = (h, name)
    return addr

def hook(uc, addr, size, user):
    global count, veh, alloc_next
    count += 1
    last.append(addr - stage)
    if count >= 5000000 or time.monotonic() - started > 120:
        raise Stop('Trace budget')
    sp = u.reg_read(UC_X86_REG_ESP)
    if addr == stage + 119611 and assume_no_marker:
        events.append({'assumption': 'process-memory marker scan returns no match', 'function': '0x1d33b', 'return': hex(r32(sp) - stage)})
        ret(0)
        return
    if addr == stage + 110931:
        h = r32(sp + 4)
        if args.model_mapped_memory and h == 0xf125414c:
            events.append({'assumption': 'unidentified optional module is absent', 'module': hex(h)})
            u.reg_write(UC_X86_REG_EBX, 0)
            ret(0, 1)
            return
        events.append({'module': hex(h), 'return': hex(r32(sp) - stage)})
        u.reg_write(UC_X86_REG_EBX, 805339136)
        ret(805339136, 1)
        return
    if addr == stage + 108601:
        h = u.reg_read(UC_X86_REG_EDX)
        events.append({'resolve': names.get(h, hex(h)), 'hash': hex(h), 'return': hex(r32(sp) - stage)})
        ret(stub(h))
        return
    if addr in stubs:
        h, name = stubs[addr]
        api_args = [hex(r32(sp + 4 + 4 * i)) for i in range(8)]
        events.append({'api': name, 'args': api_args, 'return': hex(r32(sp) - stage)})
        if name == 'RtlAddVectoredExceptionHandler':
            veh = True
            ret(1, 2)
            return
        if name == 'RtlRemoveVectoredExceptionHandler':
            ret(1, 1)
            return
        if name == 'NtAllocateVirtualMemory':
            out = r32(sp + 8)
            szptr = r32(sp + 16)
            n = r32(szptr)
            if not 0 < n <= 16777216:
                raise Stop('Allocation bound')
            mapped = n + 4095 & ~4095
            if alloc_next + mapped > 1107296256:
                raise Stop('Total allocation bound')
            u.mem_map(alloc_next, mapped)
            u.mem_write(out, struct.pack('<I', alloc_next))
            u.mem_write(szptr, struct.pack('<I', mapped))
            events[-1]['synthetic_allocation'] = {'address': hex(alloc_next), 'requested': n, 'mapped': mapped}
            alloc_next += mapped
            ret(0, 6)
            return
        if args.model_mapped_memory and name == 'ZwQueryVirtualMemory':
            address=r32(sp+8);out=r32(sp+16)
            region=next(((a,b) for a,b,_ in u.mem_regions() if a<=address<=b),None)
            if region is None: raise Stop('Query outside modeled memory')
            start,end=region
            u.mem_write(out,struct.pack('<7I',start,start,0x40,end-start+1,0x1000,0x40,0x20000))
            events[-1]['assumption']='MemoryBasicInformation describes the synthetic mapped region'
            ret(0,6)
            return
        if args.model_mapped_memory and name == 'NtProtectVirtualMemory':
            baseptr, sizeptr, oldptr = r32(sp+8), r32(sp+12), r32(sp+20)
            address, length = r32(baseptr), r32(sizeptr)
            if not any(start <= address and address+length <= end+1 for start,end,perm in u.mem_regions()):
                raise Stop('protection request outside synthetic mappings')
            u.mem_write(oldptr,struct.pack('<I',0x20))
            events[-1]['assumption']='protection request succeeds on a synthetic mapped region'
            ret(0,5)
            return
        raise Stop('API stop: ' + name)
    if not stage <= addr < stage + len(code):
        raise Stop(f'Control outside stage: {addr:x}')
    op = bytes(uc.mem_read(addr, min(size, 15)))
    if op[0] in [15, 102, 242, 243, 228, 229, 230, 231, 236, 237, 238, 239, 250, 251, 244]:
        insn = next(dis.disasm(op, addr, count=1), None)
        if insn and insn.mnemonic in privileged_names:
            raise PrivilegedFault(insn.mnemonic)
    if op[:1] == b'\xcd' or op[:2] in [b'\x0f\x05', b'\x0f4']:
        raise Stop('System instruction')
u.hook_add(unicorn.UC_HOOK_CODE, hook)

def invalid_mem(uc, access, addr, size, value, user):
    global bad_memory
    bad_memory = (access, addr, size)
    return False
u.hook_add(unicorn.UC_HOOK_MEM_INVALID, invalid_mem)
def run_trace():
    global bad_memory, res
    try:
        for attempt in range(20000):
            bad_memory = None
            try:
                u.emu_start(u.reg_read(UC_X86_REG_EIP) or stage, stage + len(code), timeout=20000000, count=max(1, 5000000 - count))
                reason = 'budget or end'
                break
            except (unicorn.UcError, PrivilegedFault) as e:
                pc = u.reg_read(UC_X86_REG_EIP)
                if not veh or not stage <= pc < stage + len(code) - 21:
                    raise
                insn = next(capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32).disasm(bytes(u.mem_read(pc, 16)), pc, count=1), None)
                privileged = insn is not None and insn.mnemonic in privileged_names
                if e.errno in [unicorn.UC_ERR_READ_UNMAPPED, unicorn.UC_ERR_WRITE_UNMAPPED]:
                    if not privileged and (bad_memory is None or bad_memory[1] > 65536):
                        raise
                elif e.errno == unicorn.UC_ERR_EXCEPTION:
                    fault_pc = stage + last[-1]
                    if bytes(u.mem_read(fault_pc, 1)) == b'\xcc':
                        pc = fault_pc
                    elif u.reg_read(UC_X86_REG_EFLAGS) & 256:
                        u.reg_write(UC_X86_REG_EFLAGS, u.reg_read(UC_X86_REG_EFLAGS) & ~256)
                    else:
                        raise
                elif e.errno != unicorn.UC_ERR_INSN_INVALID:
                    raise
                skip = bytes(u.mem_read(pc + 20, 1))[0] ^ 25
                if not 0 < skip < 256:
                    raise
                faults.append({'offset': hex(pc - stage), 'skip': skip, 'error': str(e), 'memory': bad_memory})
                u.reg_write(UC_X86_REG_EIP, pc + skip)
            if count >= 5000000:
                raise Stop('Instruction budget')
        else:
            reason = 'exception budget'
    except Exception as e:
        reason = str(e)
    res = {'reason': reason, 'instructions': count, 'events': events, 'faults': faults, 'last': [hex(x) for x in last], 'eip': hex(u.reg_read(UC_X86_REG_EIP) - stage), 'bad_memory': bad_memory, 'registers': {name: hex(u.reg_read(reg)) for name, reg in [('eax', UC_X86_REG_EAX), ('ebx', UC_X86_REG_EBX), ('ecx', UC_X86_REG_ECX), ('edx', UC_X86_REG_EDX), ('esi', UC_X86_REG_ESI), ('edi', UC_X86_REG_EDI), ('esp', UC_X86_REG_ESP), ('ebp', UC_X86_REG_EBP)]}}
    (output / ('probe-assumed.json' if assume_no_marker else 'probe-veh.json')).write_text(json.dumps(res, indent=2))
    (output / ('probe-assumed-stack.bin' if assume_no_marker else 'probe-veh-stack.bin')).write_bytes(bytes(u.mem_read(536870912, 2097152)))
    if alloc_next > 1073741824:
        (output / ('probe-assumed-allocation.bin' if assume_no_marker else 'probe-veh-allocation.bin')).write_bytes(bytes(u.mem_read(1073741824, alloc_next - 1073741824)))
    print(json.dumps({k: v for k, v in res.items() if k not in ['last', 'faults']}, indent=2))

    return res

run_trace()
