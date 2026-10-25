"""Inert PE controls for executor identity, API context, and type-name placement."""
import json
import os
from pathlib import Path
import runpy
import subprocess
import struct

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[2]
image = runpy.run_path(str(ROOT.parents[1] / 'triage-sighted/build_pe_fixtures.py'))['image']
identity = 'well-known/game/cheat::velocity-script-executor'
profile = 'micro-behaviors/process/inject/runtime/call::game-executor-remote-memory-api-profile'
api = 'micro-behaviors/metaprogramming/reflection::script-runtime-introspection-api-names'
plugin = 'metadata/binary/symbols/name/qualified::dotnet-plugin-type-name'
brand = b'https://getvelocity.llc/socket/global_announcement\0'
runtime = b'getscriptbytecode\0RobloxPlayerBeta.exe\0'
memory = b'VirtualAllocEx\0WriteProcessMemory\0'
cases = {
    'executor': (brand + runtime + memory, [identity, profile, api], []),
    'api-only': (runtime + memory, [profile, api], [identity]),
    'domain-only': (brand + memory, [], [identity, profile, api]),
    'no-memory': (brand + runtime, [identity, api], [profile]),
    'managed-type': (b'Plugin.Plugin\0', [plugin], []),
    'other-type': (b'Plugin.Host\0', [], [plugin]),
}
vm = 'micro-behaviors/process/interpreter/vm::x64-relative-opcode-dispatch'
native64 = runpy.run_path(str(ROOT.parents[1] / 'native-first-review-2026-10-17/build_controls.py'))['image']
dispatch = bytes.fromhex('42 0f b6 44 25 00 49 ff c4 4d 8b 4c c5 00 4d 01 e9 41 ff e1')
cases['vm-dispatch'] = (dispatch, [vm], [])
cases['no-relative-handler'] = (dispatch.replace(bytes.fromhex('4d01e9'), bytes.fromhex('4d31e9')), [], [vm])
for name, (strings, required, forbidden) in cases.items():
    path = ROOT / (name + '.exe')
    if name in ['vm-dispatch', 'no-relative-handler']:
        data = native64('inert')
        data[0x200:] = bytes(len(data) - 0x200)
        struct.pack_into('<II', data, 0x98 + 120, 0, 0)
        data[0x200] = 0xc3
        data[0x240:0x240 + len(strings)] = strings
        path.write_bytes(data)
    else:
        path.write_bytes(image(b'.text', strings, 0x800))
    result = subprocess.run([os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(REPO),
                             '--format', 'json', str(path)], check=True, capture_output=True, text=True)
    report = json.loads(result.stdout)
    traits = {t['id']: t for f in report['files'] for t in f['traits']}
    assert all(t in traits for t in required), (name, 'missing', required, list(traits))
    assert not any(t in traits for t in forbidden), (name, 'unexpected', forbidden)
    assert not any(t['crit'] == 5 for t in traits.values()), (name, 'hostile')
    assert all(traits[t]['crit'] == 3 for t in required), (name, 'severity')
    print(name + ': passed')
