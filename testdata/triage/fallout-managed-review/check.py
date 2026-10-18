"""Static matcher controls. Never execute the specimens or modified copies."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[3]
RUN = 'objectives/persistence/login/registry/run-key::dotnet-run-key-autostart-persistence'
FILES = 'objectives/collection/file-targeting/enumeration::managed-keylogger-file-targeting-records'
USB = 'objectives/lateral-movement/usb-worm/autorun::dotnet-autorun-drive-worm'
KILL = 'objectives/impact/degrade/process::managed-keylogger-process-tool-kill-references'
SUFFIX = 'micro-behaviors/fs/path/extension::dot-encrypted-suffix-reference'
WIFI = 'micro-behaviors/hardware/wireless/network::wlan-plaintext-key-query-arguments'
CHECK = 'micro-behaviors/fs/path/extension::source-executable-extension-check'


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--samples', type=Path, required=True)
    ap.add_argument('--work-dir', type=Path, required=True)
    ap.add_argument('--cleave', default='cleave')
    a = ap.parse_args()
    a.work_dir.mkdir(parents=True, exist_ok=True)
    cases = []

    def add(name, data, expected, suffix='.exe'):
        path = a.work_dir / (name + suffix)
        path.write_bytes(data)
        cases.append((path, expected))

    def erase(data, *tokens):
        for token in tokens:
            assert token in data, token
            data = data.replace(token, b'X' * len(token))
        return data

    names = [
        ('671396d0cd03', 'mikechen.io_new.exe'),
        ('edba0aca8f9c', 'lumbinirestaurant.com2026_chrome.exe'),
        ('4ea4dc29d007', 'lumbinirestaurant.com2026_nano.exe'),
    ]
    for i, (sha, name) in enumerate(names):
        data = (a.samples / sha / name).read_bytes()
        expected = {RUN: True, FILES: True, USB: i > 0, KILL: i > 0,
                    SUFFIX: i > 0, WIFI: i == 0}
        add(sha + '-positive', data, expected)
        # No recording: common file/process/registry APIs cannot convict.
        add(sha + '-no-recording', erase(data, b'Append\0'),
            {RUN: False, FILES: False, USB: False, KILL: False})
        add(sha + '-no-file-record', erase(data, 'FILE:'.encode('utf-16le')),
            {FILES: False, RUN: True})
        add(sha + '-no-file-enumeration', erase(data, b'GetFiles\0'),
            {FILES: False, RUN: True})
        tokens = [b'get_Location\0', b'GetEntryAssembly\0']
        if i:
            tokens.append(b'get_ExecutablePath\0')
        add(sha + '-no-self-path', erase(data, *tokens), {RUN: False})
        if i:
            add(sha + '-no-drive-type', erase(data, b'get_DriveType\0'), {USB: False})
            add(sha + '-no-process-kill', erase(data, b'Kill\0'), {KILL: False})
        else:
            # Collection must survive changing or removing the HTTP stack.
            add(sha + '-no-http-client', erase(data, b'HttpWebRequest\0'),
                {FILES: True, RUN: True})

    # No specimen-derived names: neutral observations and consolidation controls.
    build = __import__('runpy').run_path(
        str(ROOT / 'testdata/managed-records-review/verify.py'))['build_pe']
    add('neutral-suffix', build(['.encrypted']), {SUFFIX: True, FILES: False, KILL: False})
    add('neutral-wlan-query', build(['wlan show profile name key=clear']),
        {WIFI: True, RUN: False, KILL: False})
    add('plain-wlan-query', build(['wlan show profiles']), {WIFI: False})
    add('js-exe-check', b"const selected = files.filter(p => p.endsWith('.exe'));\n",
        {CHECK: True}, '.js')
    add('js-no-suffix-check', b"const selected = files.filter(p => p.includes('exe'));\n",
        {CHECK: False}, '.js')

    def check(case):
        path, expected = case
        proc = subprocess.run([a.cleave, '--traits-dir', str(ROOT), 'test-rules',
                               str(path), '--rules', ','.join(expected)],
                              capture_output=True, text=True)
        output = proc.stdout + proc.stderr
        assert proc.returncode == 0 and 'Warning: Rule ' not in output, output
        actual = {rule: any(line.startswith('MATCHED ' + rule + ' ')
                           for line in output.splitlines()) for rule in expected}
        assert actual == expected, (path.name, expected, actual, output)
        (a.work_dir / (path.name + '.trace')).write_text(output)
        return {'case': path.name, 'expected': expected, 'actual': actual}

    with ThreadPoolExecutor(max_workers=3) as pool:
        results = list(pool.map(check, cases))
    (a.work_dir / 'results.json').write_text(json.dumps(results, indent=2) + '\n')
    print('%d static controls passed' % len(results))


if __name__ == '__main__':
    main()
