"""Check resource placement, API-name near misses and exact suppressors."""
import argparse
import os
from pathlib import Path
import re
import struct
import subprocess

parser = argparse.ArgumentParser()
parser.add_argument('--cleave', default=os.environ.get('CLEAVE', 'cleave'))
parser.add_argument('--scratch', type=Path, required=True)
args = parser.parse_args()
args.scratch.mkdir(parents=True, exist_ok=True)
root = Path(__file__).resolve().parent


def pe_fixture(path, names, imported=False):
    # A static PE metadata fixture with no executable section or entry point.
    data = bytearray(0x600)
    data[:2] = b'MZ'
    struct.pack_into('<I', data, 0x3c, 0x80)
    data[0x80:0x84] = b'PE\0\0'
    struct.pack_into('<HHIIIHH', data, 0x84, 0x14c, 1, 0, 0, 0, 224, 0x102)
    opt = 0x98
    struct.pack_into('<H', data, opt, 0x10b)
    struct.pack_into('<III', data, opt + 28, 0x400000, 0x1000, 0x200)
    struct.pack_into('<II', data, opt + 56, 0x2000, 0x200)
    struct.pack_into('<H', data, opt + 68, 3)
    struct.pack_into('<I', data, opt + 92, 16)
    struct.pack_into('<8sIIIIIIHHI', data, opt + 224,
                     b'.rdata\0\0', 0x400, 0x1000, 0x400, 0x200,
                     0, 0, 0, 0, 0x40000040)
    if imported:
        struct.pack_into('<II', data, opt + 104, 0x1000, 40)
        struct.pack_into('<IIIII', data, 0x200, 0x1060, 0, 0, 0x1040, 0x1070)
        data[0x240:0x24d] = b'KERNEL32.dll\0'
        struct.pack_into('<III', data, 0x260, 0x1090, 0x10b0, 0x10d0)
        struct.pack_into('<III', data, 0x270, 0x1090, 0x10b0, 0x10d0)
        data[0x292:0x29f] = b'GetTempPathA\0'
        data[0x2b2:0x2c5] = b'GetModuleFileNameA\0'
        data[0x2d2:0x2e5] = b'GetModuleFileNameW\0'
    payload = b'\0'.join(x.encode() for x in names) + b'\0'
    data[0x300:0x300 + len(payload)] = payload
    path.write_bytes(data)


handles = ['micro-behaviors/process/fd/query::get-std-handle',
           'micro-behaviors/process/fd/control::set-std-handle',
           'micro-behaviors/os/console/control::get-console-mode',
           'micro-behaviors/os/console/control::get-console-output-cp']
prefix = 'micro-behaviors/os/sysinfo/directories::'
file_prefix = 'micro-behaviors/fs/temp/file::'
checks = [
    (root / 'stdio-console-temp.c', handles + [prefix + 'win32-temp-path-source-call'],
     [prefix + 'win32-temp-path-name']),
    (root / 'names-only.c', [], handles + [prefix + 'win32-temp-path-source-call']),
]
named = args.scratch / 'named.exe'
pe_fixture(named, ['GetTempPathW', 'GetTempFileNameW'])
checks.append((named, [prefix + x for x in ['win32-temp-path-name',
               'win32-temp-path-rdata', 'win32-temp-path-reference']] +
               [file_prefix + x for x in ['get-temp-file-name', 'temp-path-file-api-primitives']],
               [prefix + 'win32-temp-path-import', file_prefix + 'gettempfilename-rdata-reference']))
imported = args.scratch / 'imported.exe'
pe_fixture(imported, ['GetTempPath2W', 'GetTempFileName', 'https://api.telegram.org/bot123456:TEST/sendMessage'], imported=True)
checks.append((imported, [prefix + x for x in ['win32-temp-path-import',
               'win32-temp-path-reference', 'gettemppath2w-rdata-reference']] +
               ['micro-behaviors/communications/http/services/telegram::telegram-api-host',
                'micro-behaviors/communications/messaging/send::telegram-bot-send-operation'] +
               [file_prefix + x for x in ['gettempfilename-rdata-reference', 'temp-path-and-file-api-references']] +
               ['micro-behaviors/process/info/current::get-module-filename-ansi',
                'micro-behaviors/process/info/current::get-module-filename-wide'],
               [prefix + 'win32-temp-path-name', file_prefix + 'get-temp-file-name',
                'objectives/exfiltration/stealer/system-info/profile::recon-telegram-exfil']))
near = args.scratch / 'prefix-near-miss.exe'
pe_fixture(near, ['GetTempPathology', 'GetTempFileNameWhatever'])
checks.append((near, [], [prefix + 'win32-temp-path-name',
                         prefix + 'win32-temp-path-import', file_prefix + 'get-temp-file-name',
                         file_prefix + 'gettempfilename-rdata-reference']))
for path, yes, no in checks:
    proc = subprocess.run([args.cleave, 'test-rules', str(path), '--rules', ','.join(yes + no)],
                          capture_output=True, text=True)
    output = proc.stdout + proc.stderr
    assert proc.returncode == 0 and 'validation failed' not in output, output
    for ident in yes:
        assert re.search(r'^MATCHED ' + re.escape(ident) + r'\s', output, re.M), output
    for ident in no:
        assert re.search(r'^NOT MATCHED ' + re.escape(ident) + r'\s', output, re.M), output
    print(path.name + ': passed')
print('5 controls passed; all 16 moved rules covered')
