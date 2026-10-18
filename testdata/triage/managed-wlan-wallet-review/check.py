"""Static matcher controls. Generated PE fixtures must never be executed."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import runpy
import subprocess

ROOT = Path(__file__).resolve().parents[3]
WIFI = 'objectives/credential-access/wifi::managed-keylogger-plaintext-wlan-query'
WALLET = 'objectives/credential-access/wallet/desktop::managed-keylogger-wallet-file-records'
POLL = 'objectives/collection/keylog/polling::dotnet-persisted-polling-keylog-recording'
LOOP = 'micro-behaviors/data/control-flow/branch::cil-high-bit-byte-limit-checks'
SERVICE = 'micro-behaviors/communications/url/host/name::security-update-telemetry-service-references'
THREAT = 'micro-behaviors/communications/url/host/name::threat-intel-domain'


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--work-dir', type=Path, required=True)
    ap.add_argument('--samples', type=Path)
    ap.add_argument('--cleave', default='cleave')
    a = ap.parse_args()
    a.work_dir.mkdir(parents=True, exist_ok=True)
    helper = runpy.run_path(str(ROOT / 'testdata/managed-records-review/verify.py'))
    build = helper['build_pe']
    recorder = helper['KEYLOG_MARKERS']
    cases = []

    def add(name, data, expected):
        path = a.work_dir / (name + '.exe')
        path.write_bytes(data)
        cases.append((path, expected))

    query = ['wlan show profiles', 'wlan show profile "', '" key=clear',
             'set_RedirectStandardOutput']
    wallet = ['wallet.dat', 'WALLET:', 'ReadAllBytes', 'ToBase64String']
    add('admin-wlan-query', build(query), {WIFI: False})
    add('wallet-backup', build(wallet), {WALLET: False})
    add('recording-wlan-query', build(recorder + query), {WIFI: True, WALLET: False})
    add('recording-wallet-read', build(recorder + wallet), {WALLET: True, WIFI: False})
    for marker in ['" key=clear', 'set_RedirectStandardOutput']:
        add('wlan-without-' + marker.strip('" ').replace('=', '-'),
            build(recorder + [m for m in query if m != marker]), {WIFI: False})
    for marker in wallet:
        add('wallet-without-' + marker.replace(':', ''),
            build(recorder + [m for m in wallet if m != marker]), {WALLET: False})
    # GetAsyncKeyState beside an unrelated recording buffer is insufficient.
    polling = recorder + ['GetAsyncKeyState',
                          'Software\\Microsoft\\Windows\\CurrentVersion\\Run']
    add('hotkey-beside-recorder', build(polling), {POLL: False})
    start = bytes.fromhex('06 28 05 00 00 06 20 00 80 00 00 5f 16 fe 01')
    end = bytes.fromhex('06 20 ff 00 00 00 fe 02 16 fe 01 0b 07 2d 00')
    for gap in [40, 100]:
        add('polling-loop-gap-' + str(gap), build(polling, start + b'\0' * gap + end),
            {POLL: True, LOOP: True})
    add('non-key-high-bit', build(polling, start.replace(b'\x00\x80', b'\x00\x40')
                                + b'\0' * 40 + end), {POLL: False, LOOP: False})
    add('service-references', build(['virustotal.com', 'any.run']),
        {SERVICE: True, THREAT: True, WIFI: False, WALLET: False})
    add('service-near-miss', build(['licensesUpdated', 'ordinary.example']),
        {SERVICE: False, THREAT: False})
    if a.samples:
        for sha, name, wifi, wallet, poll in [
            ('5d29693dee66', 'b-a-r-f.com_ransome.exe', True, False, False),
            ('3c33a829339d', 'michaelboltoncharities.com_chrome.exe', False, False, True),
            ('a7cedc0890fb', 'michaelboltoncharities.com_nano.exe', True, True, True),
        ]:
            cases.append((a.samples / sha / name, {WIFI: wifi, WALLET: wallet, POLL: poll}))

    def check(case):
        path, expected = case
        result = subprocess.run([a.cleave, '--traits-dir', str(ROOT), '--disable',
                                 'third-party', 'test-rules', str(path), '--rules',
                                 ','.join(expected)], capture_output=True, text=True)
        output = result.stdout + result.stderr
        assert result.returncode == 0 and 'Warning: Rule ' not in output, output
        actual = {rule: any(l.startswith('MATCHED ' + rule + ' ')
                           for l in output.splitlines()) for rule in expected}
        assert actual == expected, (path.name, expected, actual, output)
        (a.work_dir / (path.name + '.trace')).write_text(output)
        return {'case': path.name, 'expected': expected, 'actual': actual}

    with ThreadPoolExecutor(max_workers=3) as pool:
        results = list(pool.map(check, cases))
    (a.work_dir / 'results.json').write_text(json.dumps(results, indent=2) + '\n')
    print('%d static controls passed' % len(results))


if __name__ == '__main__':
    main()
