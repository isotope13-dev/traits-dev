#!/usr/bin/env python3
"""Check NuGet finding accuracy and new capability coverage without running code."""
import argparse
import json
from pathlib import Path
import struct
import subprocess
import tempfile


def pe(text):
    data = bytearray(65536)
    data[:2] = b'MZ'
    struct.pack_into('<I', data, 0x3c, 0x80)
    data[0x80:0x84] = b'PE\0\0'
    struct.pack_into('<HHIIIHH', data, 0x84, 0x14c, 1, 0, 0, 0, 224, 0x102)
    opt = 0x98
    struct.pack_into('<H', data, opt, 0x10b)
    struct.pack_into('<I', data, opt + 16, 0x1000)
    struct.pack_into('<I', data, opt + 28, 0x400000)
    struct.pack_into('<II', data, opt + 32, 0x1000, 0x200)
    struct.pack_into('<II', data, opt + 56, 0x11000, 0x200)
    struct.pack_into('<H', data, opt + 68, 3)
    sec = opt + 224
    data[sec:sec + 8] = b'.text\0\0\0'
    struct.pack_into('<IIII', data, sec + 8, 0xfe00, 0x1000, 0xfe00, 0x200)
    struct.pack_into('<I', data, sec + 36, 0x60000020)
    data[0x200:0x200 + len(text)] = text
    return bytes(data)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cleave', default='../cleave/target/release/cleave')
    parser.add_argument('--helper-assembly', type=Path)
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[2]
    engine = str((repo / args.cleave).resolve())
    init = 'micro-behaviors/process/lifecycle/auto-exec::dotnet-source-module-initializer'
    add = 'micro-behaviors/os/kernel/driver::powershell-pnputil-add-driver'
    update = 'micro-behaviors/os/kernel/driver::powershell-pnputil-update-device'
    discord = 'micro-behaviors/data/parse/vocabulary::managed-discord-token-scan-routines-reference'
    telegram = 'micro-behaviors/data/parse/vocabulary::managed-telegram-session-capture-routines-reference'
    irc = 'objectives/command-and-control/channel/irc/bot::irc-process-control-command-set'
    client = 'metadata/lang/source/naming/record::clientinfo-name-binary'
    memory = 'well-known/lib/native/memory-module::memorymodule-name-reference'
    focus = {init, add, update, discord, telegram, irc, client, memory}
    cases = {}
    for i, attribute in enumerate(['ModuleInitializer', 'ModuleInitializerAttribute',
            'System.Runtime.CompilerServices.ModuleInitializer',
            'global::System.Runtime.CompilerServices.ModuleInitializerAttribute']):
        cases[f'initializer-{i}.cs'] = ('using System.Runtime.CompilerServices; class Startup { [' + attribute + '] internal static void Init() {} }', {init})
    cases.update({
        'initializer-comment.cs': ('// [ModuleInitializer]\nclass Startup {}', set()),
        'initializer-string.cs': ('class Startup { string Help = "[ModuleInitializer]"; }', set()),
        'initializer-other.cs': ('class Startup { [Other.ModuleInitializer] static void Init() {} }', set()),
        'initializer-variable.cs': ('class Startup { int ModuleInitializer; }', set()),
        'driver.ps1': ('pnputil /add-driver $inf.FullName /install\npnputil /update-device $id /install\n', {add, update}),
        'driver-exe.ps1': ('& pnputil.exe /add-driver $path /install\n', {add}),
        'driver-comment.ps1': ('# pnputil /add-driver driver.inf /install\n', set()),
        'driver-help.ps1': ('Write-Host "pnputil /add-driver driver.inf /install"\n', set()),
        'driver-enumerate.ps1': ('pnputil /enum-drivers\n', set()),
        'driver-unrelated-argument.ps1': ('Write-Host /add-driver\npnputil /enum-drivers\n', set()),
        'generic-routines.exe': (pe(b'AddToken\0CaptureDirectory\0'), set()),
        'messaging-routines.exe': (pe(b'ScanDiscordDesktop\0EnumerateTelegramFiles\0'), {discord, telegram}),
        'irc-control.exe': (pe(b'PRIVMSG\0NICK\0QUIT\0EXECUTE\0KILLPROCESS\0'), {irc}),
        'irc-with-execute.exe': (pe(b'PRIVMSG\0NICK\0QUIT\0EXECUTE\0'), set()),
        'irc-with-kill.exe': (pe(b'PRIVMSG\0NICK\0QUIT\0KILLPROCESS\0'), set()),
        'process-words.exe': (pe(b'EXECUTE\0KILLPROCESS\0'), set()),
        'client-record.exe': (pe(b'ClientInfo\0'), {client}),
        'client-record-near.exe': (pe(b'ClientInformation\0'), set()),
        'loader-name.exe': (pe(b'MemoryModule\0'), {memory}),
        'loader-name-near.exe': (pe(b'ModuleMemory\0'), set()),
    })
    with tempfile.TemporaryDirectory(prefix='nupkg-improve-controls-') as directory:
        work = Path(directory)
        for name, (data, _) in cases.items():
            (work / name).write_bytes(data if isinstance(data, bytes) else data.encode())
        result = subprocess.run([engine, '--traits-dir', str(repo), '--format', 'json', str(work)], check=True, capture_output=True, text=True)
        found = {}
        for line in result.stdout.strip().split('\n'):
            for file in json.loads(line)['files']:
                found[Path(file['path']).name] = {t['id'] for t in file.get('traits', [])}
        for name, (_, expected) in cases.items():
            assert found.get(name, set()) & focus == expected, (name, found.get(name, set()) & focus, expected)
    if args.helper_assembly:
        targets = {
            'GetFunctionPointer': 'micro-behaviors/metaprogramming/reflection/inspect/member::dotnet-runtime-method-pointer-call',
            'get_IsAttached': 'micro-behaviors/process/debug/detect::dotnet-debugger-attached-call',
        }
        with tempfile.TemporaryDirectory(prefix='managed-api-controls-') as directory:
            work = Path(directory)
            original = args.helper_assembly.read_bytes()
            (work / 'original.dll').write_bytes(original)
            for method in targets:
                assert method.encode() in original
                (work / (method + '.dll')).write_bytes(original.replace(method.encode(), b'X' * len(method)))
            result = subprocess.run([engine, '--traits-dir', str(repo), '--format', 'json', str(work)], check=True, capture_output=True, text=True)
            for line in result.stdout.strip().split('\n'):
                file = json.loads(line)['files'][0]
                ids = {t['id'] for t in file.get('traits', [])}
                for method, trait in targets.items():
                    assert (trait in ids) == (Path(file['path']).stem != method), (file['path'], trait)
    print(f'NuGet improve controls passed ({len(cases)} cases)')


if __name__ == '__main__':
    main()
