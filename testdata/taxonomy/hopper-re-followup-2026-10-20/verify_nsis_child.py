#!/usr/bin/env python3
"""Verify the persisted NSIS copied-image and child-trace controls."""
import argparse
import hashlib
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('snapshot_dir', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    manifest = json.loads((args.snapshot_dir / 'copied-region-manifest.json').read_text())
    trace = json.loads((args.snapshot_dir / 'child-entry-trace.json').read_text())
    assert manifest['source_sha256'] == 'bc9dd6f399e577577b54bc708ee930c60d29db1563fba917060c03789e740339'
    assert manifest['virtual_bytes'] == 0x4000000
    assert len(manifest['nonzero_pages']) == 70
    digest = hashlib.sha256()
    listed = {int(item['destination'], 16): item for item in manifest['nonzero_pages']}
    for address in range(0x70000000, 0x74000000, 4096):
        item = listed.get(address)
        if item is None:
            data = bytes(4096)
        else:
            data = (args.snapshot_dir / 'copied-region-pages' / f'{address:08x}.bin').read_bytes()
            assert len(data) == 4096 and any(data)
            assert hashlib.sha256(data).hexdigest() == item['sha256']
        digest.update(data)
    assert digest.hexdigest() == manifest['source_sha256']

    cases = {item['case']['name']: item for item in trace['cases']}
    assert set(cases) == {'main-thread-peb', 'non-main-thread-control',
                          'aligned-module-base-control', 'parent-register-control',
                          'magic-eax-control'}
    non_main = cases['non-main-thread-control']
    assert non_main['instructions'] == 42
    assert non_main['reason'] == 'control outside copied region: 0x30000220'
    assert non_main['pointer_overwrite']['after_child_trace'] == '0x7115c337'
    for name in ('main-thread-peb', 'aligned-module-base-control', 'parent-register-control'):
        case = cases[name]
        assert case['instructions'] == 4716743
        assert case['pointer_overwrite']['after_child_trace'] == '0x30000220'
        assert case['invalid_memory'][-1]['address'] == '0x5fffff'
        assert case['registers']['eip'] == '0x71166228'
    magic = cases['magic-eax-control']
    assert magic['instructions'] == 4716710
    assert magic['pointer_overwrite']['after_child_trace'] == '0x7115c337'
    assert magic['invalid_memory'][-1]['address'] == '0x5fffff'

    main_case = cases['main-thread-peb']
    apis = [event for event in main_case['events'] if 'api' in event]
    assert not any(event['api'].startswith('Internet') for event in apis)
    assert any(event['api'] == 'NtQueryInformationProcess' and event['args'][:2] == ['0xffffffff', '0x7'] for event in apis)
    protect = next(event for event in reversed(apis) if event['api'] == 'NtProtectVirtualMemory')
    assert protect['args'][:5] == ['0xffffffff', '0x200ffe00', '0x200ffdfc', '0x4', '0x200ffd98']
    large = next(event for event in apis
                 if event['api'] == 'NtAllocateVirtualMemory' and
                 event.get('synthetic_allocation', {}).get('virtual_bytes') == 0x2DBFF000)
    assert large['synthetic_allocation']['address'] == '0x50100000'
    report = {'verified': ['64 MiB sparse snapshot hash and 70 nonzero pages',
                           'non-main-thread tail-call control',
                           'three ordinary main-thread convergence controls',
                           'magic-EAX slot-restoration control',
                           'no corrected-path Internet API calls',
                           '0x2dbff000 sparse allocation request',
                           'ProcessDebugPort zero model',
                           'mshtml protection and base-minus-one boundary']}
    if args.output:
        args.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
