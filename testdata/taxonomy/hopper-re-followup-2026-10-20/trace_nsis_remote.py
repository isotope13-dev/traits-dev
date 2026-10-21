"""Inspect the conditional NSIS child-read path using synthetic DLL metadata.

No Windows APIs or host child processes execute. The optional remote read copies
only a snapshot of the synthetic DLL in emulator memory. Header values describe
the model, not a recovered Windows DLL. Earlier trace assumptions still apply.
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
from unicorn.x86_const import UC_X86_REG_EIP, UC_X86_REG_ESP, UC_X86_REG_EAX


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--audit-root', type=Path, required=True)
    ap.add_argument('--output-dir', type=Path, required=True)
    ap.add_argument('--dll-profile', choices=['incomplete', 'synthetic'], default='incomplete')
    ap.add_argument('--model-remote-read', action='store_true')
    ap.add_argument('--model-child-cleanup', action='store_true')
    ap.add_argument('--model-extra-child', action='store_true')
    ap.add_argument('--model-windir', action='store_true')
    ap.add_argument('--model-image-handles', action='store_true')
    args = ap.parse_args()
    assert not args.model_child_cleanup or args.model_remote_read
    assert not args.model_extra_child or args.model_child_cleanup
    assert not args.model_image_handles or (args.model_extra_child and args.model_windir)
    model = Path(__file__).with_name('trace_nsis_allocation.py')
    sys.argv = [str(model), '--audit-root', str(args.audit_root), '--output-dir',
                str(args.output_dir), '--assume-no-debug-port', '--model-child-creation']
    instructions, header_reads, local_writes = [], [], []
    captures = {}
    decoder = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_32)
    dll_base, dll_size = 0x50080000, 0x4000

    def observe(env, uc, stage):
        if args.model_windir:
            uc.mem_write(0x50094000, 'windir=C:\\Windows\0\0'.encode('utf-16le'))
            env['events'].append({'assumption': 'synthetic environment contains windir=C:\\Windows; not an observed host environment'})
        if args.dll_profile == 'synthetic':
            # Exactly the two missing fields read by the reached routine.
            uc.mem_write(dll_base + 0x138, struct.pack('<I', 0x1000))
            uc.mem_write(dll_base + 0x178, struct.pack('<I', 0x2000))
            env['events'].append({'assumption': 'synthetic 32-bit DLL range metadata: SectionAlignment=0x1000 and export-directory RVA=0x2000; not a real Windows DLL', 'dll_base': hex(dll_base)})
        captures['remote_snapshot'] = bytes(uc.mem_read(dll_base, dll_size))

        def code(uc, address, size, user):
            offset = address - stage
            if offset == 0x1bd55 and 'range_setup' not in captures:
                captures['range_setup'] = bytes(uc.mem_read(stage + 0x1bca7, 0x1bd55 - 0x1bca7))
            if 0x1bc00 <= offset < 0x1c600 and len(instructions) < 8192:
                data = bytes(uc.mem_read(address, min(size, 15)))
                insn = next(decoder.disasm(data, address, count=1), None)
                instructions.append({'offset': hex(offset), 'bytes': data.hex(),
                                     'instruction': None if insn is None else insn.mnemonic + ' ' + insn.op_str})

        def read(uc, access, address, size, value, user):
            if len(header_reads) < 1024:
                header_reads.append({'offset': hex(uc.reg_read(UC_X86_REG_EIP) - stage),
                                     'address': hex(address), 'size': size,
                                     'bytes': bytes(uc.mem_read(address, size)).hex()})

        def write(uc, access, address, size, value, user):
            if len(local_writes) < 1024:
                local_writes.append({'offset': hex(uc.reg_read(UC_X86_REG_EIP) - stage),
                                     'address': hex(address), 'size': size, 'value': hex(value)})

        uc.hook_add(unicorn.UC_HOOK_CODE, code)
        uc.hook_add(unicorn.UC_HOOK_MEM_READ, read, begin=dll_base, end=dll_base + 0xfff)
        uc.hook_add(unicorn.UC_HOOK_MEM_WRITE, write, begin=dll_base, end=dll_base + dll_size - 1)

    driver = runpy.run_path(str(model))
    state = driver['main'](observe)
    env, uc = state['env'], state['uc']
    result = env['res']
    read_boundary = next((event for event in reversed(env['events']) if event.get('api') == 'NtReadVirtualMemory'), None)
    modeled_read = None
    if args.model_remote_read:
        assert args.dll_profile == 'synthetic'
        assert result['reason'] == 'API stop: NtReadVirtualMemory'
        sp = uc.reg_read(UC_X86_REG_ESP)
        values = [env['r32'](sp + 4 + 4 * i) for i in range(5)]
        assert values == [0x61000001, dll_base + 0x1000, dll_base + 0x1000, 0x2000, 0]
        process, source, destination, length, _ = values
        snapshot = captures['remote_snapshot'][source - dll_base:source - dll_base + length]
        assert len(snapshot) == length
        before = bytes(uc.mem_read(destination, length))
        uc.mem_write(destination, snapshot)
        modeled_read = {'assumption': 'NtReadVirtualMemory succeeds using only the pre-captured synthetic DLL snapshot; no remote process exists',
                        'process_handle': hex(process), 'source': hex(source),
                        'destination': hex(destination), 'bytes': length,
                        'snapshot_sha256': hashlib.sha256(snapshot).hexdigest(),
                        'destination_before_sha256': hashlib.sha256(before).hexdigest(),
                        'destination_after_sha256': hashlib.sha256(bytes(uc.mem_read(destination, length))).hexdigest()}
        env['events'].append(modeled_read)
        env['ret'](0, 5)
        env['instruction_limit'] = env['count'] + 5000000
        env['started'] = time.monotonic()
        result = env['run_trace']()
    cleanup, extra_children = [], []
    if args.model_child_cleanup:
        for _ in range(4):
            event = env['events'][-1]
            name = event.get('api')
            if result['reason'] != 'API stop: ' + str(name):
                break
            sp = uc.reg_read(UC_X86_REG_ESP)
            handle = env['r32'](sp + 4)
            if name == 'TerminateProcess':
                assert [handle, env['r32'](sp + 8)] == [0x61000001, 0]
                value, count = 1, 2
            elif name in ('NtClose', 'CloseHandle'):
                assert handle in (0x61000001, 0x61000002)
                value, count = int(name == 'CloseHandle'), 1
            else:
                break
            action = {'assumption': 'successful cleanup of synthetic child only; no host process or handle exists',
                      'api': name, 'handle': hex(handle)}
            cleanup.append(action)
            env['events'].append(action)
            env['ret'](value, count)
            env['started'] = time.monotonic()
            result = env['run_trace']()
    pending_child = driver['capture_process_creation'](env, uc, state['stage'])
    if pending_child is not None and args.model_extra_child:
        sp = uc.reg_read(UC_X86_REG_ESP)
        pointer = int(pending_child['process_info_pointer'], 16)
        uc.mem_write(pointer, struct.pack('<4I', 0x61000003, 0x61000004, 1236, 1237))
        extra = {**pending_child, 'assumption': 'one additional synthetic suspended child succeeds; no host process exists',
                 'process_handle': '0x61000003', 'thread_handle': '0x61000004'}
        extra_children.append(extra)
        env['events'].append(extra)
        uc.reg_write(UC_X86_REG_ESP, sp + 56)
        uc.reg_write(UC_X86_REG_EAX, 1)
        uc.reg_write(UC_X86_REG_EIP, state['stage'] + 0x1da93)
        env['started'] = time.monotonic()
        result = env['run_trace']()
        pending_child = driver['capture_process_creation'](env, uc, state['stage'])
    file_open, image_handles = None, []
    if result['reason'] == 'API stop: NtOpenFile':
        sp = uc.reg_read(UC_X86_REG_ESP)
        values = [env['r32'](sp + 4 + 4 * i) for i in range(6)]
        attributes = [env['r32'](values[2] + 4 * i) for i in range(6)]
        length, maximum, pointer = struct.unpack('<HHI', uc.mem_read(attributes[2], 8))
        assert attributes[0] == 24 and 0 < length <= maximum <= 2048 and length % 2 == 0
        file_open = {'api': 'NtOpenFile', 'args': [hex(value) for value in values],
                     'object_attributes': [hex(value) for value in attributes],
                     'unicode_string': {'length': length, 'maximum': maximum, 'pointer': hex(pointer),
                                        'value': bytes(uc.mem_read(pointer, length)).decode('utf-16le')}}
        if args.model_image_handles:
            assert file_open['unicode_string']['value'] == r'\??\C:\Windows\SysWOW64\mshtml.dll'
            assert values[1] == 1 and values[4:] == [1, 0]
            uc.mem_write(values[0], struct.pack('<I', 0x62000001))
            uc.mem_write(values[3], struct.pack('<II', 0, 0))
            action = {'assumption': 'NtOpenFile returns a synthetic read-only mshtml.dll handle; no host file is opened', 'handle': '0x62000001'}
            image_handles.append(action)
            env['events'].append(action)
            env['ret'](0, 6)
            env['instruction_limit'] = env['count'] + 5000000
            env['started'] = time.monotonic()
            result = env['run_trace']()
            assert result['reason'] == 'API stop: NtCreateSection'
            sp = uc.reg_read(UC_X86_REG_ESP)
            values = [env['r32'](sp + 4 + 4 * i) for i in range(7)]
            assert values[1:] == [0xf001f, 0, 0, 2, 0x1000000, 0x62000001]
            uc.mem_write(values[0], struct.pack('<I', 0x62000002))
            action = {'assumption': 'NtCreateSection returns only an opaque synthetic SEC_IMAGE handle; no image bytes supplied', 'handle': '0x62000002'}
            image_handles.append(action)
            env['events'].append(action)
            env['ret'](0, 7)
            env['started'] = time.monotonic()
            result = env['run_trace']()
    mapping = None
    if result['reason'] == 'API stop: NtMapViewOfSection':
        sp = uc.reg_read(UC_X86_REG_ESP)
        values = [env['r32'](sp + 4 + 4 * i) for i in range(10)]
        mapping = {'api': 'NtMapViewOfSection', 'args': [hex(value) for value in values],
                   'requested_base': hex(env['r32'](values[2])),
                   'requested_view_bytes': env['r32'](values[6])}
    setup = captures['range_setup']
    report = {'stage_sha256': hashlib.sha256(env['code']).hexdigest(),
              'dll_profile': args.dll_profile, 'model_windir': args.model_windir,
              'read_boundary': read_boundary,
              'modeled_read': modeled_read, 'modeled_cleanup': cleanup,
              'extra_children': extra_children, 'pending_process_creation': pending_child,
              'file_open': file_open, 'image_handles': image_handles, 'image_mapping': mapping,
              'range_setup': {'offset': '0x1bca7', 'end': '0x1bd55', 'hex': setup.hex(),
                              'sha256': hashlib.sha256(setup).hexdigest()},
              'header_reads': header_reads, 'local_writes': local_writes,
              'executed_instructions': instructions, 'trace': result}
    if state['reservation'] is not None:
        reservation = state['reservation']
        report['sparse_memory'] = {'virtual_bytes': reservation.size,
                                  'backed_bytes': len(reservation.pages) * 4096,
                                  'pages': [hex(page) for page in sorted(reservation.pages)]}
        for page in sorted(reservation.pages):
            (args.output_dir / f'sparse-page-{page:08x}.bin').write_bytes(bytes(uc.mem_read(page, 4096)))
    (args.output_dir / 'stage-at-remote-stop.bin').write_bytes(bytes(uc.mem_read(state['stage'], len(env['code']))))
    (args.output_dir / 'remote-continuation.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'reason': result['reason'], 'instructions': result['instructions'],
                      'read_boundary': read_boundary, 'modeled_read': modeled_read}, indent=2))
    state['remote_report'] = report
    return state


if __name__ == '__main__':
    state = main()
