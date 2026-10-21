"""Continue the hash-checked NSIS model through one large allocation.

The successful scenario reserves virtual addresses but maps only pages touched
by modeled data accesses. At most 32 MiB is backed; execute access is forbidden.
All earlier conditional assumptions remain in force. No host APIs are called.
"""
import argparse
import hashlib
import json
import runpy
import struct
import sys
import time
from pathlib import Path

import unicorn
from unicorn.x86_const import UC_X86_REG_ESP, UC_X86_REG_EAX, UC_X86_REG_EIP


class SparseReservation:
    def __init__(self, uc, base, size, max_backed=32 * 1024 * 1024):
        assert base % 4096 == size % 4096 == 0 and size > 0
        assert base + size <= 0x80000000
        assert max_backed >= 4096 and max_backed % 4096 == 0
        assert all(base + size <= start or base > end for start, end, _ in uc.mem_regions())
        self.uc, self.base, self.size = uc, base, size
        self.max_backed = max_backed
        self.pages = set()
        self.limit_reached = False
        self.hook = uc.hook_add(unicorn.UC_HOOK_MEM_INVALID, self.fault)

    def fault(self, uc, access, address, size, value, user):
        if access not in (unicorn.UC_MEM_READ_UNMAPPED, unicorn.UC_MEM_WRITE_UNMAPPED):
            return False
        if not self.base <= address < address + size <= self.base + self.size:
            return False
        pages = set(range(address & ~4095, (address + size + 4095) & ~4095, 4096)) - self.pages
        if (len(self.pages) + len(pages)) * 4096 > self.max_backed:
            self.limit_reached = True
            return False
        for page in sorted(pages):
            uc.mem_map(page, 4096, unicorn.UC_PROT_READ | unicorn.UC_PROT_WRITE)
            self.pages.add(page)
        return True


def capture_process_creation(env, uc, stage):
    entry = next((address for address, (_, name) in env['stubs'].items()
                  if name == 'CreateProcessInternalW'), None)
    if entry is None or uc.reg_read(UC_X86_REG_EIP) != entry + 5:
        return None
    sp, r32 = uc.reg_read(UC_X86_REG_ESP), env['r32']
    words = [r32(sp + 4 * i) for i in range(14)]
    assert words[0] == 0x1000 and words[8] == 4
    thunk = bytes(uc.mem_read(words[1], 6))
    assert thunk[0] == 0x68 and thunk[5] == 0xc3
    assert struct.unpack('<I', thunk[1:5])[0] == stage + 0x1da93

    def read_wide(pointer):
        text = bytearray()
        for offset in range(0, 2048, 2):
            pair = bytes(uc.mem_read(pointer + offset, 2))
            if pair == b'\0\0':
                return text.decode('utf-16le')
            text.extend(pair)
        raise ValueError('unterminated process-creation string')

    assert r32(words[11]) == 68
    return {'api': 'CreateProcessInternalW', 'entry_adjustment': 5,
            'application': read_wide(words[3]), 'command_line': read_wide(words[4]),
            'creation_flags': hex(words[8]), 'startup_info_cb': r32(words[11]),
            'process_info_pointer': hex(words[12]), 'return_thunk': thunk.hex(),
            'stack_words': [hex(word) for word in words]}


def main(continuation_observer=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--audit-root', type=Path, required=True)
    ap.add_argument('--output-dir', type=Path, required=True)
    ap.add_argument('--allocation-result', choices=['sparse-success', 'no-memory'], default='sparse-success')
    ap.add_argument('--model-internet-session', action='store_true')
    ap.add_argument('--assume-no-debug-port', action='store_true')
    ap.add_argument('--model-child-creation', action='store_true')
    args = ap.parse_args()
    model = Path(__file__).with_name('trace_nsis_mixed.py')
    sys.argv = [str(model), '--audit-root', str(args.audit_root), '--output-dir', str(args.output_dir), '--model-window-count', '12', '--assume-thread-hide-success']
    mixed = runpy.run_path(str(model))
    env = mixed['env']
    uc, stage = mixed['old'], mixed['stage']
    assert env['res']['reason'] == 'Allocation bound'
    sp = uc.reg_read(UC_X86_REG_ESP)
    r32 = env['r32']
    assert r32(sp) == stage + 0x204a
    assert [r32(sp + 4 + 4 * i) for i in range(6)] == [0xffffffff, 0x200ffd68, 0, 0x200ffd64, 0x3000, 4]
    requested = r32(r32(sp + 16))
    assert requested == 0x2dbff000 and r32(r32(sp + 8)) == 0
    reservation = None
    if args.allocation_result == 'sparse-success':
        reservation = SparseReservation(uc, 0x50100000, requested)
        uc.mem_write(r32(sp + 8), struct.pack('<I', reservation.base))
        env['events'].append({'assumption': 'large allocation succeeds with zero-initialized sparse backing; data pages materialize on access, bounded to 32 MiB; execution is forbidden', 'address': hex(reservation.base), 'virtual_bytes': requested})
        env['ret'](0, 6)
    else:
        env['events'].append({'assumption': 'large allocation fails with STATUS_NO_MEMORY; output pointers remain unchanged'})
        env['ret'](0xc0000017, 6)
    env['args'].model_internet_session = args.model_internet_session
    env['args'].assume_no_debug_port = args.assume_no_debug_port
    env['instruction_limit'] = env['count'] + 5000000
    env['events'].append({'continuation_instruction_budget':5000000,'cumulative_instruction_limit':env['instruction_limit']})
    if continuation_observer is not None:
        continuation_observer(env, uc, stage)
    recent = []
    writes = []
    network_code = []
    network_entry = []
    def trace_code(uc, address, size, user):
        if 0xd900 <= address-stage < 0xeb00 and len(network_code)<12000:
            from unicorn.x86_const import UC_X86_REG_EAX, UC_X86_REG_EBX, UC_X86_REG_ECX, UC_X86_REG_EDX, UC_X86_REG_ESI, UC_X86_REG_EDI
            network_code.append({'pc':hex(address-stage),'bytes':bytes(uc.mem_read(address,min(size,15))).hex(),'registers':{n:hex(uc.reg_read(r)) for n,r in [('eax',UC_X86_REG_EAX),('ebx',UC_X86_REG_EBX),('ecx',UC_X86_REG_ECX),('edx',UC_X86_REG_EDX),('esi',UC_X86_REG_ESI),('edi',UC_X86_REG_EDI)]}})
        if 0xd900 <= address-stage < 0xde00 and not network_entry:
            sp=uc.reg_read(UC_X86_REG_ESP)
            network_entry.append({'pc':hex(address-stage),'previous':[hex(x) for x in recent[-40:]],'sp':hex(sp),'stack':[hex(struct.unpack('<I',uc.mem_read(sp+4*i,4))[0]) for i in range(12)]})
        recent.append(address-stage)
        if len(recent)>8192: del recent[:4096]
    def trace_write(uc, access, address, size, value, user):
        if 0x30008100 <= address < 0x30009100 and len(writes)<2048:
            from unicorn.x86_const import UC_X86_REG_EIP, UC_X86_REG_ESI, UC_X86_REG_EDI, UC_X86_REG_ECX
            writes.append({'pc':hex(uc.reg_read(UC_X86_REG_EIP)-stage),'address':hex(address),'size':size,'value':hex(value),'esi':hex(uc.reg_read(UC_X86_REG_ESI)),'edi':hex(uc.reg_read(UC_X86_REG_EDI)),'ecx':hex(uc.reg_read(UC_X86_REG_ECX))})
    uc.hook_add(unicorn.UC_HOOK_CODE, trace_code)
    uc.hook_add(unicorn.UC_HOOK_MEM_WRITE, trace_write)
    env['started'] = time.monotonic()
    result = env['run_trace']()
    creation = capture_process_creation(env, uc, stage)
    if creation is not None:
        sp=uc.reg_read(UC_X86_REG_ESP)
        words=[r32(sp+4*i) for i in range(14)]
        if args.model_child_creation:
            uc.mem_write(words[12],struct.pack('<4I',0x61000001,0x61000002,1234,1235))
            env['events'].append({**creation,'assumption':'successful creation of synthetic suspended child; no host process exists','process_handle':'0x61000001','thread_handle':'0x61000002'})
            uc.reg_write(UC_X86_REG_ESP,sp+56)
            uc.reg_write(UC_X86_REG_EAX,1)
            uc.reg_write(UC_X86_REG_EIP,stage+0x1da93)
            env['started']=time.monotonic()
            result=env['run_trace']()
    report = {'process_creation':creation,'scenario': args.allocation_result, 'requested_bytes': requested, 'trace': result, 'temporary_export_buffer_writes':writes, 'recent_offsets':[hex(x) for x in recent], 'executed_network_code':network_code, 'network_entry':network_entry}
    if reservation:
        pages = sorted(reservation.pages)
        report['sparse_memory'] = {'base': hex(reservation.base), 'virtual_bytes': requested, 'backed_bytes': len(pages)*4096, 'backing_limit': reservation.max_backed, 'limit_reached': reservation.limit_reached, 'pages': [hex(p) for p in pages]}
        for i, page in enumerate(pages):
            data = bytes(uc.mem_read(page, 4096))
            if any(data):
                (args.output_dir / f'sparse-page-{page:08x}.bin').write_bytes(data)
    code = bytes(uc.mem_read(stage, len(env['code'])))
    (args.output_dir/'stage-at-allocation-stop.bin').write_bytes(code)
    report['stage_memory_sha256'] = hashlib.sha256(code).hexdigest()
    (args.output_dir/'allocation-continuation.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({k: v for k, v in report.items() if k in ('scenario','requested_bytes','sparse_memory','stage_memory_sha256')}, indent=2))
    return {'env':env,'uc':uc,'stage':stage,'reservation':reservation,'args':args}


if __name__ == '__main__':
    state = main()
