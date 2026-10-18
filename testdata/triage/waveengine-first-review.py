"""Static role-removal controls; never execute the PE inputs or copies.

python3 testdata/triage/waveengine-first-review.py --samples PATH --work-dir PATH
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]
BROWSER = 'objectives/credential-access/browser/chromium::managed-keylogger-browser-store-read-references'
CRITICAL = 'objectives/impact/system/crash::managed-keylogger-termination-critical-enable'
OLD = 'objectives/collection/keylog/hook::dotnet-hook-keylogger-browser-store-references'


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--samples', type=Path, required=True)
    ap.add_argument('--work-dir', type=Path, required=True)
    ap.add_argument('--cleave', default='cleave')
    a = ap.parse_args()
    a.work_dir.mkdir(parents=True, exist_ok=True)
    cases = []

    def add(name, data, browser, critical):
        path = a.work_dir / (name + '.exe')
        path.write_bytes(data)
        cases.append((path, {BROWSER: browser, CRITICAL: critical}))

    for sha, name in [('8f2802713d02', 'waveengine.net_new.exe'),
                      ('0fb6e37f5847', 'waveengine.net_ransome.exe')]:
        data = (a.samples / sha / name).read_bytes()
        add(sha + '-positive', data, True, True)
        for label, token, browser, critical in [
            ('no-store', 'Login Data'.encode('utf-16le'), False, True),
            ('no-read', b'ReadAllBytes\0', False, True),
            ('no-recording', b'Append\0', False, False),
            ('no-critical-api', b'NtSetInformationProcess\0', True, False),
        ]:
            assert token in data, (name, label)
            add(sha + '-' + label, data.replace(token, b'X' * len(token)), browser, critical)
        # Disable the enable flag while preserving APIs and all keylog evidence.
        # The two builds have the same short-local and getter-chain encoding.
        start = bytes.fromhex('17 13 13 28')
        offsets = [i for i in range(len(data)) if data.startswith(start, i)
                   and data[i + 13:i + 15] == b'\x1f\x1d']
        assert len(offsets) == 1, (name, offsets)
        altered = bytearray(data)
        altered[offsets[0]] = 0x16
        add(sha + '-critical-disabled', altered, True, False)

    def check(case):
        path, expected = case
        p = subprocess.run([a.cleave, '--traits-dir', str(ROOT),
                            '--disable', 'radare2,third-party', 'test-rules',
                            str(path), '--rules', ','.join(expected)],
                           capture_output=True, text=True)
        output = p.stdout + p.stderr
        assert p.returncode == 0 and 'Warning: Rule ' not in output, output
        actual = {rule: any(line.startswith('MATCHED ' + rule + ' ')
                            for line in output.splitlines()) for rule in expected}
        assert actual == expected, (path.name, expected, actual, output)
        (a.work_dir / (path.name + '.trace')).write_text(output)
        return {'case': path.name, 'expected': expected, 'actual': actual}

    assert OLD not in '\n'.join(p.read_text() for p in ROOT.glob('objectives/**/*.yaml'))
    with ThreadPoolExecutor(max_workers=3) as pool:
        results = list(pool.map(check, cases))
    (a.work_dir / 'results.json').write_text(json.dumps(results, indent=2) + '\n')
    print('%d static role-removal controls passed' % len(results))


if __name__ == '__main__':
    main()
