#!/usr/bin/env python3
"""Build sanitized shortcut controls and check their behavior findings."""
import json
import os
from pathlib import Path
import struct
import subprocess
import tempfile
import zipfile

COMMANDS = 'micro-behaviors/process/create/shell/command-flag::lnk-headless-extract-copy-batch-commands'
LOCAL_ICON = 'objectives/evasion/masquerade/file/lure::lnk-browser-icon-local-batch-commands'
REMOTE_ICON = 'objectives/evasion/masquerade/file/lure::lnk-browser-icon-remote-command-lure'
STARTUP = 'micro-behaviors/fs/write/content::batch-startup-script-redirect-block'
COPY = 'micro-behaviors/fs/file/copy::batch-quoted-startup-copy-destination'
INVENTORY = 'objectives/discovery/host/security::batch-tasklist-av-name-filter'
OLD = {
    'objectives/execution/lnk/proxy::headless-conhost-argument-batch-carrier',
    'objectives/execution/payload/file-exec::lnk-headless-archive-config-batch',
    'objectives/command-and-control/dropper/lnk/script-chain::lnk-script-chain-dropper',
    'objectives/command-and-control/dropper/lnk/conhost-curl::temp-exe-download',
    'objectives/command-and-control/dropper/lnk/conhost-curl::working-directory-system32',
}


def shortcut(arguments, target=None, icon=None):
    header = bytearray(76)
    struct.pack_into('<I', header, 0, 76)
    header[4:20] = bytes.fromhex('0114020000000000c000000000000046')
    struct.pack_into('<I', header, 20, 0xa0 | (2 if target else 0) | (64 if icon else 0))
    link_info = b''
    if target:
        # Local LinkInfo with a fixed disk, an empty volume label and suffix.
        path = target.encode('ascii') + b'\0'
        volume = struct.pack('<IIII', 17, 3, 0, 16) + b'\0'
        link_info = struct.pack('<IIIIIII', 46 + len(path), 28, 1, 28, 45, 0, 45 + len(path))
        link_info += volume + path + b'\0'
    strings = struct.pack('<H', len(arguments)) + arguments.encode('utf-16le')
    if icon:
        strings += struct.pack('<H', len(icon)) + icon.encode('utf-16le')
    return header + link_info + strings + bytes(4)


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
        'different-config-source.lnk': (prefix + chain.replace('copy "%TEMP%\\settings.ini"', 'copy "%TEMP%\\other.ini"'), True),
        'different-batch-sink.lnk': (prefix + chain.replace('&& "%TEMP%\\runner.bat"', '&& "%TEMP%\\other.bat"'), True),
        'real-target.lnk': (prefix + chain, True),
        'local-browser-icon.lnk': (prefix + chain, True),
        'targetless-browser-icon.lnk': (prefix + chain, True),
        'browser-icon-only.lnk': ('/c echo Ready', False),
        'slash-c-only.lnk': ('/c echo Ready', False),
        'no-slash-c.lnk': ('-NoProfile -Command Get-Date', False),
        'normal-window.lnk': ('/c echo Ready', False),
    }
    with tempfile.TemporaryDirectory(prefix='shortcut-review-') as temporary:
        folder = Path(temporary)
        for name, (arguments, expected) in cases.items():
            target = r'C:\Windows\System32\cmd.exe' if name in {'real-target.lnk', 'local-browser-icon.lnk', 'browser-icon-only.lnk'} else None
            icon = r'C:\Program Files\Browser\msedge.exe' if 'browser-icon' in name else None
            content = shortcut(arguments, target, icon)
            if name == 'normal-window.lnk':
                content = bytearray(content)
                struct.pack_into('<I', content, 60, 1)
            (folder / name).write_bytes(content)
        no_arguments = bytearray(shortcut(''))
        struct.pack_into('<I', no_arguments, 20, 0x80)
        del no_arguments[76:78]
        (folder / 'no-arguments.lnk').write_bytes(no_arguments)
        cases['no-arguments.lnk'] = ('', False)
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
        with zipfile.ZipFile(folder / 'no-shortcut.zip', 'w') as archive:
            archive.writestr('stage.txt', '@echo off\r\n')
        cases['no-shortcut.zip'] = ('', False)
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
            target = targets.get(name, STARTUP if name.endswith('.bat') else COMMANDS)
            assert (target in ids) == expected, (name, target, expected, sorted(ids))
            assert not ids.intersection(OLD), (name, ids.intersection(OLD))
            if not name.endswith('.bat'):
                assert REMOTE_ICON not in ids, (name, 'local commands misreported as remote')
                assert (LOCAL_ICON in ids) == (name == 'local-browser-icon.lnk'), (name, sorted(ids))
                for file in files:
                    for trait in file.get('traits', []):
                        if trait['id'] == COMMANDS:
                            assert trait['crit'] in (3, 'notable'), (name, trait)
            if name == 'slash-c-only.lnk':
                assert 'micro-behaviors/process/argument/option::lnk-slash-c-switch' in ids
            if name == 'profile-option.lnk':
                assert 'micro-behaviors/process/argument/file::lnk-batch-file-argument' not in ids
            if name == 'no-slash-c.lnk':
                assert 'micro-behaviors/process/argument/option::lnk-slash-c-switch' not in ids
            if name == 'no-arguments.lnk':
                assert 'metadata/file/profile/field-presence::lnk-has-arguments' not in ids
            if name.endswith('.zip'):
                member = 'metadata/file/archive::archive-shortcut-member'
                assert (member in ids) == (name != 'no-shortcut.zip'), (name, sorted(ids))
            if name in {'normal-window.lnk', 'slash-c-only.lnk'}:
                hidden = 'micro-behaviors/ui/window/state::lnk-hidden-window'
                assert (hidden in ids) == (name == 'slash-c-only.lnk'), (name, sorted(ids))
            seen.add(name)
            print('PASS', name)
        assert seen == set(cases), ('missing cases', set(cases) - seen)


if __name__ == '__main__':
    main()
