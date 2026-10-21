"""Static regression controls. Read and mutate PE bytes; never execute them."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
import importlib.util
import struct
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[3]
PATH = 'micro-behaviors/fs/path/password-store::managed-microsoft-credentials-path-components'
COPY = 'objectives/credential-access/credential-manager/store-api::managed-keylogger-credential-directory-copy-references'
RC4 = 'micro-behaviors/crypto/symmetric/stream/rc4::x64-stack-index-prga-buffer-xor'
TLS = 'micro-behaviors/communications/tls/verify/disable::x64-winhttp-certificate-ignore-call-setup'
HTTP = 'micro-behaviors/communications/http/direct-socket::winsock-json-close-header-references'
OLD_UAC = 'objectives/privilege-escalation/elevation-control/uac-bypass/library::uac-bypass-pattern'
OLD_HTTP = 'objectives/command-and-control/channel/http-beacon::raw-tcp-http-cluster'


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--managed', type=Path, required=True)
    ap.add_argument('--ghost', type=Path, required=True)
    ap.add_argument('--work-dir', type=Path, required=True)
    ap.add_argument('--cleave', default='cleave')
    args = ap.parse_args()
    args.work_dir.mkdir(parents=True, exist_ok=True)
    managed, ghost = args.managed.read_bytes(), args.ghost.read_bytes()
    cases = []

    def add(name, data, expected):
        path = args.work_dir / (name + '.exe')
        path.write_bytes(data)
        cases.append((path, expected))

    def patch(data, old, new):
        assert len(old) == len(new) and old in data
        return data.replace(old, new)

    # Independent inert PE controls: the entry point only returns zero.
    spec = importlib.util.spec_from_file_location(
        'pe_controls', ROOT / 'testdata/managed-records-review/verify.py')
    stub = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(stub)

    def native_stub(markers):
        data = stub.build_pe(markers)
        struct.pack_into('<II', data, 0x98 + 96 + 14 * 8, 0, 0)
        data[0x210:0x258] = bytes(72)
        data[0x280:0x2a0] = bytes(32)
        return data

    add('elevation-status-only', native_stub([
        'High (elevated/UAC bypassed)', 'Medium (not elevated; needs UAC bypass)']),
        {PATH: False, TLS: False, HTTP: False})
    add('ordinary-http-header-references', native_stub([
        'connect', 'Content-Type: application/json', 'Connection: close']),
        {HTTP: True, TLS: False, RC4: False})
    add('http-missing-connect-reference', native_stub([
        'Content-Type: application/json', 'Connection: close']), {HTTP: False})
    add('split-clr-heap', managed, {PATH: True, COPY: True})
    # The words remain in the heap, but the ldstr no longer names Credentials.
    sequence = bytes.fromhex('1f 1c 28 09 00 00 0a 72 5e 12 00 70 72 ae 20 00 70')
    add('unrelated-clr-arguments', patch(managed, sequence, sequence[:-4] + sequence[8:12]),
        {PATH: False, COPY: False})
    add('wrong-special-folder', patch(managed, sequence, b'\x1f\x1a' + sequence[2:]),
        {PATH: False, COPY: False})
    add('no-credential-directory', patch(managed, 'Credentials'.encode('utf-16le'),
                                        'Xredentials'.encode('utf-16le')),
        {PATH: False, COPY: False})
    add('no-copy-member', patch(managed, b'\0Copy\0', b'\0Xopy\0'),
        {PATH: True, COPY: False})
    add('native-crypto-http', ghost, {RC4: True, TLS: True, HTTP: True})
    loop = bytes.fromhex('0f b6 04 04 41 30 01 49 83 c1 01 4c 39 cb 75 c4')
    add('no-rc4-output-xor', patch(ghost, loop, loop[:5] + b'\x00' + loop[6:]),
        {RC4: False, TLS: True})
    relax = bytes.fromhex('41 b9 04 00 00 00 4c 8d 44 24 64 ba 1f 00 00 00 48 89 d9 c7 44 24 64 00 33 00 00 41 ff d4')
    add('tls-protocol-option-only', patch(ghost, relax, relax[:12]+b'\x54'+relax[13:]),
        {TLS: False})
    add('tls-no-ignore-flags', patch(ghost, relax, relax[:23]+b'\0'*4+relax[27:]),
        {TLS: False})
    add('tls-different-local', patch(ghost, relax, relax[:22]+b'\x60'+relax[23:]),
        {TLS: False})
    add('tls-wrong-import-slot', patch(ghost, b'WinHttpSetOption\0', b'WinHttpXetOption\0'),
        {TLS: False})
    add('http-no-close-header', patch(ghost, b'Connection: close', b'Connection: other'),
        {HTTP: False})

    def check(case):
        path, expected = case
        result = subprocess.run([args.cleave, '--traits-dir', str(ROOT),
                                 '--disable', 'radare2,third-party', '--format', 'json',
                                 'analyze', str(path)], capture_output=True, text=True,
                                check=True, timeout=120)
        report = json.loads(result.stdout)
        traits = {t['id']: t for f in report['files'] for t in f.get('traits', [])}
        actual = {rule: rule in traits for rule in expected}
        assert actual == expected, (path.name, expected, actual, result.stderr)
        assert OLD_UAC not in traits and OLD_HTTP not in traits
        if path.name in {'elevation-status-only.exe', 'ordinary-http-header-references.exe'}:
            assert not any(t['crit'] >= 4 for t in traits.values()), path.name
        if HTTP in traits:
            assert traits[HTTP]['crit'] == 3
        return {'case': path.name, 'expected': expected, 'actual': actual}

    with ThreadPoolExecutor(max_workers=3) as pool:
        results = list(pool.map(check, cases))
    (args.work_dir / 'results.json').write_text(json.dumps(results, indent=2)+'\n')
    print(f'{len(results)} static positive and near-miss controls passed')


if __name__ == '__main__':
    main()
