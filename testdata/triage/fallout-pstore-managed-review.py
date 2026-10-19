"""Static positive and near-miss controls; never execute the PE inputs.

python3 testdata/triage/fallout-pstore-managed-review.py --samples PATH --work-dir PATH
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]
XOR = 'micro-behaviors/data/encoding/xor::x86-indexed-byte-xor-stack-key-loop'
HTTP_PROFILE = 'micro-behaviors/communications/http/client/managed::managed-keyboard-recording-webclient-references'
GET = 'micro-behaviors/communications/http/get::getasync'
POST = 'micro-behaviors/communications/http/post::postasync'
SAMPLES = [
    'b67f41c05838/2026-10-17_6d2548bec993f9f8a2f083cf6c9d7004_elex_wannacry',
    '91d52fd5c36f/2026-10-17_6d2e43c6893295f5f41940087b260d7f_destroyer_elex_glassworm_ngrbot_wannacry',
    'a332a60d2aff/socolivetv.ca_hyber.exe',
]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--samples', type=Path, required=True)
    ap.add_argument('--work-dir', type=Path, required=True)
    ap.add_argument('--cleave', default='cleave')
    a = ap.parse_args()
    a.work_dir.mkdir(parents=True, exist_ok=True)
    data = [(a.samples / p).read_bytes() for p in SAMPLES]
    cases = []

    def add(name, content, expected):
        path = a.work_dir / name
        path.write_bytes(content if isinstance(content, bytes) else content.encode())
        cases.append((path, expected))

    add('native.exe', data[0], {XOR: True, HTTP_PROFILE: False})
    add('buffered.exe', data[1], {HTTP_PROFILE: True})
    add('file-logger.exe', data[2], {HTTP_PROFILE: False, GET: True, POST: True})
    signature = bytes.fromhex('8B 55 08 03 55 FC 0F BE 02 33 45 0C 8B 4D 08 03 4D FC 88 01 EB D2')
    assert data[0].count(signature) == 1
    for name, offset, value in [('no-xor', 9, 3), ('different-store', 19, 2),
                                ('forward-branch', 21, 32)]:
        patch = bytearray(signature)
        patch[offset] = value
        add(name + '.exe', data[0].replace(signature, bytes(patch)), {XOR: False})
    for name, token in [('no-upload', b'UploadString\0'),
                        ('no-recording', b'Append\0'),
                        ('no-webclient', b'WebClient\0')]:
        assert token in data[1]
        add(name + '.exe', data[1].replace(token, b'X' * (len(token) - 1) + b'\0'),
            {HTTP_PROFILE: False})
    assert b'HttpClient\0' in data[2]
    add('no-httpclient.exe', data[2].replace(b'HttpClient\0', b'X' * 10 + b'\0'),
        {GET: False, POST: False})
    add('http.cs', '''using System.Net.Http;
class Example { async void Send() {
var client = new HttpClient();
await client.GetAsync("https://example.com/data");
await client.PostAsync("https://example.com/data", null);
} }
''', {GET: True, POST: True, HTTP_PROFILE: False})
    add('cache.cs', '''class Example { async void Read(dynamic cache) {
await cache.GetAsync("entry"); await cache.PostAsync("entry");
} }
''', {GET: False, POST: False, HTTP_PROFILE: False})
    add('reference-only.cs', '''using System.Net.Http;
class Example { string[] methods = { "GetAsync", "PostAsync" };
HttpClient client = new HttpClient(); }
''', {GET: True, POST: True, HTTP_PROFILE: False})

    def check(case):
        path, expected = case
        proc = subprocess.run([a.cleave, '--traits-dir', str(ROOT),
                               '--disable', 'radare2,third-party', 'test-rules',
                               str(path), '--rules', ','.join(expected)],
                              capture_output=True, text=True)
        output = proc.stdout + proc.stderr
        (a.work_dir / (path.name + '.trace')).write_text(output)
        assert proc.returncode == 0 and 'Warning: Rule ' not in output, output
        actual = {rule: any(line.startswith('MATCHED ' + rule + ' ')
                            for line in output.splitlines()) for rule in expected}
        assert actual == expected, (path.name, expected, actual, output)
        return {'case': path.name, 'expected': expected, 'actual': actual}

    with ThreadPoolExecutor(max_workers=3) as pool:
        results = list(pool.map(check, cases))
    (a.work_dir / 'results.json').write_text(json.dumps(results, indent=2) + '\n')
    print('%d static positive and near-miss controls passed' % len(results))


if __name__ == '__main__':
    main()
