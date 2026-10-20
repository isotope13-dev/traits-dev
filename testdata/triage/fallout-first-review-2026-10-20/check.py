#!/usr/bin/env python3
"""Static mutation controls; never run the supplied Windows executable."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
RULE = 'objectives/anti-analysis/debugger-detect/check::managed-dual-debugger-check-exit-layout'
RETIRED = 'objectives/command-and-control/backdoor/loader/download::confuserex-managed-http-dropper-hidden-launch'
CAPABILITIES = {
    'micro-behaviors/communications/http/client/managed::httpwebrequest',
    'micro-behaviors/communications/http/client/managed::getresponsestream',
    'micro-behaviors/fs/write/file/full::dotnet-writeallbytes-token',
    'micro-behaviors/process/create/hidden::dotnet-create-no-window',
}


def collect_ids(value):
    found = set()
    if isinstance(value, dict):
        if isinstance(value.get('id'), str):
            found.add(value['id'])
        for child in value.values():
            found.update(collect_ids(child))
    elif isinstance(value, list):
        for child in value:
            found.update(collect_ids(child))
    return found


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('sample', type=Path)
    parser.add_argument('--cleave', default='cleave')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    import dnfile
    from dncil.cil.body.reader import read_method_body_from_bytes
    pe = dnfile.dnPE(str(args.sample))
    entry_rid = pe.net.struct.EntryPointTokenOrRva & 0xffffff
    method = pe.net.mdtables.MethodDef.rows[entry_rid - 1]
    body = read_method_body_from_bytes(pe.get_data(method.Rva, 20000))
    check = next(ins for ins in body.instructions
                 if ins.opcode.name == 'call'
                 and getattr(ins.operand, 'table', None) == 6
                 and str(pe.net.mdtables.MethodDef.rows[ins.operand.rid - 1].Name)
                 == 'IsDebuggerPresent')
    code_offset = pe.get_offset_from_rva(method.Rva) + check.offset
    original = args.sample.read_bytes()
    assert original[code_offset + 5] == 0x2d
    cases = {'original': (original, True)}
    altered = bytearray(original)
    altered[code_offset + 5] = 0x00
    cases['references_without_short_circuit'] = (bytes(altered), False)
    for name in [b'IsDebuggerPresent', b'get_IsAttached', b'Debugger', b'Exit']:
        needle = b'\0' + name + b'\0'
        assert needle in original
        cases['without_' + name.decode()] = (
            original.replace(needle, b'\0' + b'Z' * len(name) + b'\0'), False)
    altered = bytearray(original)
    gate_length = 31
    gate = original[code_offset:code_offset + gate_length]
    altered[code_offset:code_offset + gate_length] = b'\0' * gate_length
    altered.extend(gate)
    cases['gate_only_in_overlay'] = (bytes(altered), False)
    rows = []
    with tempfile.TemporaryDirectory(prefix='fallout-static-controls-') as tmp:
        for name, (data, expected) in cases.items():
            path = Path(tmp) / (name + '.exe')
            path.write_bytes(data)
            result = subprocess.run(
                [args.cleave, '--traits-dir', str(ROOT), '--format', 'json', str(path)],
                capture_output=True, text=True,
                env={**os.environ, 'CLEAVE_NO_UPDATE_CHECK': '1'})
            assert result.returncode == 0, result.stderr
            ids = collect_ids(json.loads(result.stdout))
            assert (RULE in ids) == expected, name
            assert RETIRED not in ids, name
            assert CAPABILITIES <= ids, (name, CAPABILITIES - ids)
            rows.append({'case': name, 'anti_debug': RULE in ids,
                         'neutral_capabilities_retained': True,
                         'false_dropper_absent': True})
    output = json.dumps(rows, indent=2) + '\n'
    if args.output:
        args.output.write_text(output)
    print(output, end='')


if __name__ == '__main__':
    main()
