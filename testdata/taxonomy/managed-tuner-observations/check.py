"""Static positive/near-miss controls; inert PE entry points contain only RET.

Pass an existing scratch directory. No generated artifact is executed.
"""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import json
import os
import re
import struct
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
SHA = 'micro-behaviors/crypto/hash/digest::sha256-code-name-reference'
INVOKE = 'metadata/lang/source/syntax/call/invocation::invoke-member-call-text'
HOST = 'micro-behaviors/process/interpreter/powershell/host::dotnet-powershell-host'
PIPE = 'micro-behaviors/process/deploy/script-eval::pe-irm-iex-pipeline-text'
DNS = 'micro-behaviors/network/dns::powershell-set-dns-server-address-text'
HOOK = 'micro-behaviors/ui/window/hook::set-win-event-hook-declaration'


def pe(code=b'', resource=b'', overlay=b''):
    data = bytearray(0x600)
    data[:2] = b'MZ'
    struct.pack_into('<I', data, 0x3c, 0x80)
    data[0x80:0x84] = b'PE\0\0'
    struct.pack_into('<HHIIIHH', data, 0x84, 0x14c, 2, 1600000000, 0, 0, 224, 0x102)
    opt = 0x98
    struct.pack_into('<H', data, opt, 0x10b)
    for off, value in {4:512, 8:512, 16:0x1000, 20:0x1000, 24:0x2000,
                       28:0x400000, 32:0x1000, 36:0x200, 56:0x3000, 60:0x200,
                       72:0x100000, 76:0x1000, 80:0x100000, 84:0x1000, 92:16}.items():
        struct.pack_into('<I', data, opt + off, value)
    struct.pack_into('<HH', data, opt + 40, 6, 0)
    struct.pack_into('<H', data, opt + 68, 3)
    for i, (name, rva, raw, flags) in enumerate([
        (b'.text', 0x1000, 0x200, 0x60000020),
        (b'.rsrc', 0x2000, 0x400, 0x40000040),
    ]):
        struct.pack_into('<8sIIIIIIHHI', data, opt + 224 + i * 40,
                         name, 512, rva, 512, raw, 0, 0, 0, 0, flags)
    assert len(code) < 500 and len(resource) < 500
    data[0x200] = 0xc3
    data[0x210:0x210+len(code)] = code
    data[0x410:0x410+len(resource)] = resource
    return bytes(data) + overlay


def main():
    scratch = Path(sys.argv[1])
    scratch.mkdir(parents=True, exist_ok=True)
    cases = [
        ('clr-sha256.exe', pe(b'SHA256\0'), {SHA}, set()),
        ('clr-provider.exe', pe(b'SHA256CryptoServiceProvider\0'), {SHA}, set()),
        ('certificate-label.exe', pe(overlay=b'DigiCert RSA4096 SHA256 Timestamp Responder\0'), set(), {SHA}),
        ('resource-label.exe', pe(resource=b'SHA256\0'), set(), {SHA}),
        ('sha-source.cs', b'class Hash { object Create() => SHA256.Create(); }', {'micro-behaviors/crypto/hash/digest::csharp-sha256-operation'}, {SHA}),
        ('gui-invoke.cs', b'using System.Management.Automation; class Gui { void Paint() { dispatcher.Invoke(() => Update()); } }', {INVOKE}, {HOST}),
        ('runspace.exe', pe(b'System.Management.Automation\0CreateRunspace\0'), {HOST}, set()),
        ('pipeline.exe', pe(b'irm $ScriptUrl | iex\0'), {PIPE}, set()),
        ('dns-set.exe', pe(b'Set-DnsClientServerAddress -InterfaceAlias $nic -ServerAddresses ("1.1.1.1")\0'), {DNS}, set()),
        ('dns-query.exe', pe(b'Get-DnsClientServerAddress -InterfaceAlias $nic\0'), set(), {DNS}),
        ('event-hook.exe', pe(b'static extern IntPtr SetWinEventHook(uint min, uint max);\0'), {HOOK}, set()),
        ('event-method.exe', pe(b'static IntPtr SetWinEventHook(uint min, uint max) { return value; }\0'), set(), {HOOK}),
    ]

    def check(case):
        name, data, present, absent = case
        path = scratch / name
        path.write_bytes(data)
        result = subprocess.run([
            os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
            'test-rules', str(path), '--rules', ','.join(sorted(present | absent))
        ], check=True, capture_output=True, text=True)
        matched = set(re.findall(r'^MATCHED (\S+)', result.stdout, re.MULTILINE))
        missing, unexpected = present - matched, absent & matched
        assert not missing and not unexpected, (name, missing, unexpected, result.stdout)
        return {'case': name, 'passed': True}

    with ThreadPoolExecutor(max_workers=3) as pool:
        print(json.dumps(list(pool.map(check, cases)), indent=2))


if __name__ == '__main__':
    main()
