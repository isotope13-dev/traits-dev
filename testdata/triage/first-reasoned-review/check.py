#!/usr/bin/env python3
"""Build sanitized shortcut controls and check their behavior findings."""
import json
import os
from pathlib import Path
import struct
import subprocess
import tempfile
import zipfile

PAYLOAD = 'objectives/execution/payload/file-exec::lnk-headless-archive-config-batch'
STARTUP = 'micro-behaviors/fs/write/content::batch-startup-script-redirect-block'
COPY = 'micro-behaviors/fs/file/copy::batch-quoted-startup-copy-destination'
INVENTORY = 'objectives/discovery/host/security::batch-tasklist-av-name-filter'
OLD = {
    'objectives/command-and-control/dropper/lnk/script-chain::lnk-script-chain-dropper',
    'objectives/command-and-control/dropper/lnk/conhost-curl::temp-exe-download',
    'objectives/command-and-control/dropper/lnk/conhost-curl::working-directory-system32',
}


def shortcut(arguments):
    header = bytearray(76)
    struct.pack_into('<I', header, 0, 76)
    header[4:20] = bytes.fromhex('0114020000000000c000000000000046')
    struct.pack_into('<I', header, 20, 0xa0)  # Unicode argument field
    return header + struct.pack('<H', len(arguments)) + arguments.encode('utf-16le') + bytes(4)


def main():
    atomscan = os.environ.get('ATOMSCAN', 'atomscan')
    prefix = '/c conhost --headless cmd /c '
    chain = ('tar -xf "%TEMP%\\inner.zip" -C "%TEMP%" settings.ini && '
             'copy "%TEMP%\\settings.ini" "%TEMP%\\runner.bat" /y >nul && '
             '"%TEMP%\\runner.bat"')
    cases = {
        'renamed.lnk': (prefix + chain, True),
        'alternate-config.lnk': (prefix + chain.replace('.ini', '.cfg').replace('.bat', '.cmd'), True),
        'profile-option.lnk': ('/c powershell -nop -c Get-Date', False),
        'temp-references.lnk': ('/c powershell -nop -c Write-Output "%TEMP%\\one.txt %TEMP%\\two.txt"', False),
        'without-headless.lnk': ('/c ' + chain, False),
        'without-invocation.lnk': (prefix + chain.rsplit(' && ', 1)[0], False),
        'without-copy.lnk': (prefix + chain.split(' && ')[0] + ' && "%TEMP%\\runner.bat"', False),
    }
    with tempfile.TemporaryDirectory(prefix='shortcut-review-') as temporary:
        folder = Path(temporary)
        for name, (arguments, expected) in cases.items():
            (folder / name).write_bytes(shortcut(arguments))
        startup = '> "%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\StartUp\\agent.bat" (\r\necho @echo off\r\n)\r\n'
        for name, lnk, content, expected in [
            ('persistent.zip', 'renamed.lnk', startup, True),
            ('ordinary-startup.zip', 'profile-option.lnk', startup, False),
            ('without-startup.zip', 'renamed.lnk', '@echo off\r\n', True),
        ]:
            with zipfile.ZipFile(folder / name, 'w') as archive:
                archive.writestr('launch.lnk', (folder / lnk).read_bytes())
                archive.writestr('stage.txt', content)
            cases[name] = ('', expected)
        (folder / 'startup-block.bat').write_text(startup)
        (folder / 'startup-reference.bat').write_text('echo Startup\\agent.bat\n')
        cases['startup-block.bat'] = ('', True)
        cases['startup-reference.bat'] = ('', False)
        (folder / 'copy-into-startup.bat').write_text('copy "%~f0" "%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\StartUp\\agent.bat"\n')
        (folder / 'unrelated-copy.bat').write_text('copy "%~f0" "%LOCALAPPDATA%\\cache.bat"\necho "%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\StartUp\\agent.bat"\n')
        (folder / 'antivirus-inventory.bat').write_text('tasklist /fo csv /nh | findstr /i "avast.exe"\n')
        cases['copy-into-startup.bat'] = ('', True)
        cases['unrelated-copy.bat'] = ('', False)
        cases['antivirus-inventory.bat'] = ('', True)
        targets = {'copy-into-startup.bat': COPY, 'unrelated-copy.bat': COPY, 'antivirus-inventory.bat': INVENTORY}
        result = subprocess.run([atomscan, '--no-update', '--follow=none', '-f', 'json', str(folder)],
                                text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        assert result.returncode in (0, 1) and result.stdout.strip(), result.stderr
        seen = set()
        for line in result.stdout.splitlines():
            raw = json.loads(line)['raw']
            files = raw.get('files', [])
            if not files:
                continue
            name = Path(files[0]['path']).name
            if name not in cases:
                continue
            expected = cases[name][1]
            ids = {trait['id'] for file in files for trait in file.get('traits', [])}
            target = targets.get(name, STARTUP if name.endswith('.bat') else PAYLOAD)
            assert (target in ids) == expected, (name, target, expected, sorted(ids))
            assert not ids.intersection(OLD), (name, ids.intersection(OLD))
            seen.add(name)
            print('PASS', name)
        assert seen == set(cases), ('missing cases', set(cases) - seen)


if __name__ == '__main__':
    main()
