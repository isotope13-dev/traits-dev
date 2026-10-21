"""Conditional NSIS .data-pointer search after a symbolic child image mapping.

Both DLL metadata and remote image mapping are synthetic. No native processes,
host DLL loading, or remote-memory APIs execute. A pointer-match fixture is an
explicit branch control, not a recovered Windows global or payload.
"""
import argparse
import hashlib
import json
import runpy
import struct
import sys
import time
from pathlib import Path

import capstone
import unicorn
from unicorn.x86_const import UC_X86_REG_EAX, UC_X86_REG_EIP, UC_X86_REG_ESP


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--audit-root', type=Path, required=True)
    ap.add_argument('--output-dir', type=Path, required=True)
    ap.add_argument('--data-profile', choices=['zero', 'pointer-match'], default='zero')
    ap.add_argument('--model-remote-allocation', action='store_true')
    ap.add_argument('--model-region-copy', action='store_true')
    ap.add_argument('--snapshot-copied-region', action='store_true')
    ap.add_argument('--assume-resume-success', action='store_true')
    ap.add_argument('--assume-child-thunk-initialized', action='store_true')
    ap.add_argument('--model-pointer-overwrite', action='store_true')
    args = ap.parse_args()
    assert not args.model_region_copy or args.model_remote_allocation
    assert not args.snapshot_copied_region or args.model_region_copy
    assert not args.assume_resume_success or args.model_region_copy
    assert not args.assume_child_thunk_initialized or args.assume_resume_success
    assert not args.model_pointer_overwrite or args.assume_child_thunk_initialized
    model = Path(__file__).with_name('trace_nsis_remote.py')
    sys.argv = [str(model), '--audit-root', str(args.audit_root), '--output-dir', str(args.output_dir),
                '--dll-profile', 'synthetic', '--model-remote-read', '--model-child-cleanup',
                '--model-extra-child', '--model-windir', '--model-image-handles']
    state = runpy.run_path(str(model))['main']()
    env, uc, stage = state['env'], state['uc'], state['stage']
    assert env['res']['reason'] == 'API stop: NtMapViewOfSection'
    sp = uc.reg_read(UC_X86_REG_ESP)
    values = [env['r32'](sp + 4 + 4 * i) for i in range(10)]
    assert values[:2] == [0x62000002, 0x61000003]
    assert values[3:6] == [6, 0, 0] and values[7:] == [2, 0, 4]
    uc.mem_write(values[2], struct.pack('<I', 0x600000))
    uc.mem_write(values[6], struct.pack('<I', 0x20000))
    env['events'].append({'assumption': 'symbolic remote-only image base 0x600000 and extent 0x20000 succeed; no mshtml.dll bytes or local image backing are supplied'})
    data_base, data_size = 0x50083000, 0x40
    uc.mem_write(0x50080220, struct.pack('<8s8I', b'.data', data_size, 0x3000, data_size, 0x2000, 0, 0, 0, 0xc0000040))
    env['events'].append({'assumption': 'synthetic ntdll section table contains a .data section at RVA 0x3000 with VirtualSize/SizeOfRawData=0x40 and zero-filled contents'})
    records, accesses, fixtures = [], [], []
    decoder = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)

    def code(uc, address, size, user):
        offset = address - stage
        if offset == 0xbc10 and not fixtures:
            pointer = uc.reg_read(UC_X86_REG_EAX)
            assert env['stubs'][pointer] == (0x8bfb3ee0, 'BaseThreadInitThunk')
            fixture = {'resolved_name': 'BaseThreadInitThunk', 'hash': '0x8bfb3ee0',
                       'synthetic_export': hex(pointer), 'profile': args.data_profile}
            if args.data_profile == 'pointer-match':
                uc.mem_write(data_base + 0x20, struct.pack('<I', pointer))
                fixture['seed_address'] = hex(data_base + 0x20)
                env['events'].append({'assumption': 'synthetic .data slot at offset 0x20 initially equals the synthetic BaseThreadInitThunk export pointer'})
            fixtures.append(fixture)
        if 0xbb00 <= offset < 0xc800 and len(records) < 8192:
            data = bytes(uc.mem_read(address, min(size, 15)))
            insn = next(decoder.disasm(data, address, count=1), None)
            records.append({'offset': hex(offset), 'bytes': data.hex(),
                            'instruction': None if insn is None else insn.mnemonic + ' ' + insn.op_str})

    def access(uc, kind, address, size, value, user):
        if len(accesses) < 1024:
            accesses.append({'offset': hex(uc.reg_read(UC_X86_REG_EIP) - stage),
                             'kind': 'write' if kind == unicorn.UC_MEM_WRITE else 'read',
                             'address': hex(address), 'size': size, 'value': hex(value),
                             'bytes_before': bytes(uc.mem_read(address, size)).hex()})

    uc.hook_add(unicorn.UC_HOOK_CODE, code)
    uc.hook_add(unicorn.UC_HOOK_MEM_READ | unicorn.UC_HOOK_MEM_WRITE, access,
                begin=data_base, end=data_base + 0xfff)
    env['ret'](0, 10)
    env['instruction_limit'] = env['count'] + 2000000
    env['started'] = time.monotonic()
    result = env['run_trace']()
    remote_allocation = None
    if result['reason'] == 'Remote allocation boundary':
        sp = uc.reg_read(UC_X86_REG_ESP)
        values = [env['r32'](sp + 4 + 4 * i) for i in range(6)]
        remote_allocation = {'args': [hex(value) for value in values],
                             'requested_base': hex(env['r32'](values[1])),
                             'requested_bytes': env['r32'](values[3])}
        if args.model_remote_allocation:
            assert args.data_profile == 'pointer-match'
            assert values == [0x61000003, 0x200ffe04, 0, 0x200ffe00, 0x1000, 0x40]
            assert remote_allocation['requested_base'] == '0x0'
            assert remote_allocation['requested_bytes'] == 0x4000000
            uc.mem_write(values[1], struct.pack('<I', 0x70000000))
            remote_allocation['synthetic_base'] = '0x70000000'
            env['events'].append({'assumption': '64 MiB executable allocation succeeds symbolically in the second synthetic child at 0x70000000; no parent or host memory is allocated'})
            env['ret'](0, 6)
            env['started'] = time.monotonic()
            result = env['run_trace']()
    region_copy = None
    if args.model_region_copy:
        assert result['reason'] == 'API stop: NtWriteVirtualMemory'
        sp = uc.reg_read(UC_X86_REG_ESP)
        values = [env['r32'](sp + 4 + 4 * i) for i in range(5)]
        assert values == [0x61000003, 0x70000000, 0x10000000, 0x4000000, 0x200ffe00]
        digest = hashlib.sha256()
        nonzero_pages = 0
        copied_pages = []
        copied_page_dir = args.output_dir / 'copied-region-pages'
        if args.snapshot_copied_region:
            copied_page_dir.mkdir(parents=True, exist_ok=True)
        for offset in range(0, values[3], 0x10000):
            data = bytes(uc.mem_read(values[2] + offset, 0x10000))
            digest.update(data)
            for page in range(0, len(data), 4096):
                page_data = data[page:page + 4096]
                if not any(page_data):
                    continue
                nonzero_pages += 1
                source_address = values[2] + offset + page
                destination_address = values[1] + source_address - values[2]
                item = {'source': hex(source_address), 'destination': hex(destination_address),
                        'sha256': hashlib.sha256(page_data).hexdigest()}
                copied_pages.append(item)
                if args.snapshot_copied_region:
                    (copied_page_dir / f'{destination_address:08x}.bin').write_bytes(page_data)
        region_copy = {'assumption': 'remote write succeeds symbolically; source bytes are streamed for hashing only, with no host or remote-process write',
                       'args': [hex(value) for value in values], 'source_sha256': digest.hexdigest(),
                       'nonzero_source_pages': nonzero_pages,
                       'size_limit': '64 MiB equals the synthetic parent mapping extent; this is not a recovered payload size.'}
        if args.snapshot_copied_region:
            manifest = {'source_base': hex(values[2]), 'destination_base': hex(values[1]),
                        'virtual_bytes': values[3], 'source_sha256': digest.hexdigest(),
                        'nonzero_pages': copied_pages,
                        'zero_page_semantics': 'All omitted pages are zero because the entire 64 MiB region is copied.'}
            (args.output_dir / 'copied-region-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
            region_copy['snapshot_manifest'] = 'copied-region-manifest.json'
        entry_source = stage + 0xaf
        region_copy['loader_entry'] = {'source': hex(entry_source),
                                       'destination': hex(values[1] + entry_source - values[2]),
                                       'stage_offset': '0xaf',
                                       'copied_prefix_hex': bytes(uc.mem_read(entry_source, 96)).hex()}
        uc.mem_write(values[4], struct.pack('<I', values[3]))
        env['events'].append(region_copy)
        env['ret'](0, 5)
        env['started'] = time.monotonic()
        result = env['run_trace']()
    resumed_thread = None
    if args.assume_resume_success:
        assert result['reason'] == 'API stop: NtResumeThread'
        sp = uc.reg_read(UC_X86_REG_ESP)
        values = [env['r32'](sp + 4 + 4 * i) for i in range(2)]
        assert values == [0x61000004, 0]
        resumed_thread = {'assumption': 'NtResumeThread succeeds for the second synthetic child thread; no child instructions execute',
                          'args': [hex(value) for value in values]}
        env['events'].append(resumed_thread)
        env['ret'](0, 2)
        env['started'] = time.monotonic()
        result = env['run_trace']()
    child_thunk_read = None
    if args.assume_child_thunk_initialized:
        assert result['reason'] == 'API stop: NtReadVirtualMemory'
        sp = uc.reg_read(UC_X86_REG_ESP)
        values = [env['r32'](sp + 4 + 4 * i) for i in range(5)]
        assert values == [0x61000003, data_base + 0x20, 0x200ffd9c, 4, 0]
        pointer = int(fixtures[0]['synthetic_export'], 16)
        uc.mem_write(values[2], struct.pack('<I', pointer))
        child_thunk_read = {'assumption': 'second synthetic child .data global is initialized to the same synthetic BaseThreadInitThunk pointer; no child instructions or actual remote read execute',
                            'args': [hex(value) for value in values], 'returned_pointer': hex(pointer)}
        env['events'].append(child_thunk_read)
        env['ret'](0, 5)
        env['started'] = time.monotonic()
        result = env['run_trace']()
    cleanup = []
    for _ in range(4):
        if result['reason'] != 'API stop: NtClose':
            break
        sp = uc.reg_read(UC_X86_REG_ESP)
        handle = env['r32'](sp + 4)
        assert handle in (0x62000001, 0x62000002)
        action = {'assumption': 'synthetic image file/section handle closes successfully', 'handle': hex(handle)}
        cleanup.append(action)
        env['events'].append(action)
        env['ret'](0, 1)
        env['started'] = time.monotonic()
        result = env['run_trace']()
    pending_write = None
    modeled_pointer_write = None
    if result['reason'] == 'API stop: NtWriteVirtualMemory':
        sp = uc.reg_read(UC_X86_REG_ESP)
        values = [env['r32'](sp + 4 + 4 * i) for i in range(5)]
        pending_write = {'args': [hex(value) for value in values]}
        if values[3] <= 0x10000:
            pending_write['source_hex'] = bytes(uc.mem_read(values[2], values[3])).hex()
        if args.model_pointer_overwrite:
            assert values == [0x61000003, data_base + 0x20, 0x200ffe04, 4, 0x200ffe00]
            replacement = env['r32'](values[2])
            assert replacement == 0x70000000 + stage + 0xaf - 0x10000000
            uc.mem_write(values[4], struct.pack('<I', 4))
            modeled_pointer_write = {
                'assumption': 'the pending four-byte write succeeds only in the symbolic second child; parent .data remains unchanged',
                'process_handle': hex(values[0]), 'child_address': hex(values[1]),
                'replacement': hex(replacement), 'bytes': 4,
            }
            env['events'].append(modeled_pointer_write)
            env['ret'](0, 5)
            env['started'] = time.monotonic()
            result = env['run_trace']()
    report = {'stage_sha256': hashlib.sha256(env['code']).hexdigest(), 'data_profile': args.data_profile,
              'data_section': {'base': hex(data_base), 'virtual_bytes': data_size,
                               'final_hex': bytes(uc.mem_read(data_base, data_size)).hex()},
              'fixtures': fixtures, 'data_accesses': accesses, 'executed_instructions': records,
              'cleanup': cleanup, 'remote_allocation': remote_allocation,
              'region_copy': region_copy, 'pending_write': pending_write,
              'modeled_pointer_write': modeled_pointer_write,
              'resumed_thread': resumed_thread, 'child_thunk_read': child_thunk_read, 'trace': result}
    (args.output_dir / 'section-continuation.json').write_text(json.dumps(report, indent=2) + '\n')
    (args.output_dir / 'stage-at-section-stop.bin').write_bytes(bytes(uc.mem_read(stage, len(env['code']))))
    print(json.dumps({'reason': result['reason'], 'instructions': result['instructions'],
                      'fixture': fixtures, 'last_event': env['events'][-1]}, indent=2))
    state['section_report'] = report
    return state


if __name__ == '__main__':
    state = main()
