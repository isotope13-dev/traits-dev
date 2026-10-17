#!/usr/bin/env python3
"""Precision controls: content/API references must not become attack findings."""
import json
from pathlib import Path
import struct
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
HOSTS = 'micro-behaviors/network/dns::'
CONTEXT = 'micro-behaviors/process/inject/runtime/thread-context::'
CLIP = 'micro-behaviors/os/clipboard/reference::dynamic-clipboard-readwrite-hook-api-set'
ADS = 'objectives/evasion/file-hiding/system::native-script-stream-payload-stager'


def pe(text):
    """Inert PE32: a RET instruction and a separate read-only data section."""
    b = bytearray(0x2400)
    b[:2] = b'MZ'
    struct.pack_into('<I', b, 0x3c, 0x80)
    b[0x80:0x84] = b'PE\0\0'
    struct.pack_into('<HHIIIHH', b, 0x84, 332, 2, 0, 0, 0, 224, 0x102)
    opt = 0x98
    struct.pack_into('<H', b, opt, 0x10b)
    for off, value in [(16, 0x1000), (20, 0x1000), (24, 0x2000),
                       (28, 0x400000), (32, 0x1000), (36, 0x200),
                       (56, 0x4000), (60, 0x200), (92, 16)]:
        struct.pack_into('<I', b, opt + off, value)
    struct.pack_into('<H', b, opt + 68, 3)
    for i, (name, va, raw, size, flags) in enumerate([
        (b'.text', 0x1000, 0x200, 0x200, 0x60000020),
        (b'.rdata', 0x2000, 0x400, 0x2000, 0x40000040)]):
        struct.pack_into('<8sIIIIIIHHI', b, opt + 224 + i * 40,
                         name, size, va, size, raw, 0, 0, 0, 0, flags)
    b[0x200] = 0xc3
    payload = text.encode() + b'\0'
    assert len(payload) < 0x2000
    b[0x400:0x400 + len(payload)] = payload
    return b


def scan(path):
    result = subprocess.run(['cleave', '--traits-dir', str(ROOT), '--format', 'json', str(path)],
                            capture_output=True, text=True, check=True)
    report = json.loads(result.stdout)
    files = report.get('files', report.get('raw', {}).get('files', []))
    return {t['id']: t['crit'] for f in files for t in f.get('traits', [])}


def main():
    cases = [
        ('public-hosts.js', 'const p = "/etc/hosts";\n'
         'const entry = "45.67.89.123 resolver.example.net";\n',
         [HOSTS + 'external-ip-hosts-name-entry', HOSTS + 'hosts-path-public-ip-entry'], []),
        ('local-aliases.ps1', '\n'.join(f'127.0.0.1 service{i}.example.net' for i in range(5))
         + '\n# ' + 'padding ' * 180,
         [HOSTS + 'multiple-loopback-hosts-entries'], []),
        ('context-names.exe', 'VirtualAllocEx\0WriteProcessMemory\0GetThreadContext\0'
         'SetThreadContext\0ResumeThread\0CreateProcessA\0',
         [CONTEXT + 'importless-remote-context-api-set', CONTEXT + 'importless-context-loader-api-profile'], []),
        ('clipboard-names.exe', 'GetClipboardData\0SetClipboardData\0EmptyClipboard\0'
         'GetProcAddress\0GetKeyboardState\0', [CLIP], []),
        ('mining-help.exe', 'cpuminer 2.3.2\0Usage: minerd [OPTIONS]\0'
         '-O, --userpass=U:P    username:password pair for mining server\0'
         'Stratum notify: invalid Merkle branch\0User-Agent: cpuminer/2.3.2\0',
         ['well-known/tool/sysadmin/cpuminer::cpuminer-command-line-miner'], []),
        ('stream-command-only.exe', 'C:\\Windows\\System32\\WScript.exe '
         'C:\\Windows\\logs\\report.txt:runner.js\0',
         ['micro-behaviors/fs/path/stream::script-host-ads-command'], [ADS]),
        ('ordinary-script-command.exe', 'C:\\Windows\\System32\\WScript.exe '
         'C:\\Windows\\logs\\runner.js\0', [],
         ['micro-behaviors/fs/path/stream::script-host-ads-command', ADS]),
        ('loopback-connect.c', 'int connect(int,void*,int); int main(){const char *ip="127.0.0.1"; return connect(0,0,0);}',
         ['micro-behaviors/communications/socket/connect::loopback-address'], []),
        ('loopback-only.c', 'const char *ip="127.0.0.1";', [],
         ['micro-behaviors/communications/socket/connect::loopback-address']),
        ('connect-only.c', 'int connect(int,void*,int); int main(){return connect(0,0,0);}', [],
         ['micro-behaviors/communications/socket/connect::loopback-address']),
    ]
    with tempfile.TemporaryDirectory(prefix='native-payload-controls-') as tmp:
        for name, content, yes, no in cases:
            path = Path(tmp) / name
            path.write_bytes(pe(content) if name.endswith('.exe') else content.encode())
            found = scan(path)
            assert all(x in found for x in yes), (name, 'missing', set(yes) - found.keys(), found)
            assert all(x not in found for x in no), (name, 'unexpected', set(no) & found.keys())
            assert all(v not in (4, 5, 'suspicious', 'hostile') for v in found.values()), (name, found)
            print(name, 'PASS')


if __name__ == '__main__':
    main()
