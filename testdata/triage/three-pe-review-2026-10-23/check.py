"""Static regression controls; never execute specimens or generated PEs.

python3 check.py --sample /path/to/zip-final.exe --work-dir /path/to/scratch
"""
import argparse
import json
from pathlib import Path
import runpy
import struct
import subprocess

ROOT = Path(__file__).resolve().parents[3]
SWAP = 'objectives/impact/crypto-manipulation/clipboard::managed-wallet-regex-clipboard-replacement'
CLIPPER = 'objectives/impact/crypto-manipulation/clipboard::managed-backdoor-wallet-clipboard-replacement'
RUN = 'objectives/persistence/login/registry/run-key::managed-plugin-backdoor-run-key-references'
CLAIM = 'objectives/evasion/masquerade/version-resource/claim::microsoft-company-claim-with-urlmon-reference'
LABEL = 'metadata/binary/resource/identity::microsoft-exact-string-rsrc'


def version_block(key, value=b'', children=(), kind=1):
    data = bytearray(struct.pack('<HHH', 0, len(value) // 2 if kind else len(value), kind))
    data += key.encode('utf-16le') + b'\0\0'
    data += bytes(-len(data) % 4)
    data += value
    for child in children:
        data += bytes(-len(data) % 4) + child
    struct.pack_into('<H', data, 0, len(data))
    return data


def make_version_control(company, urlmon=True):
    image = runpy.run_path(str(ROOT / 'testdata/triage/first-review/build_pe_fixtures.py'))['image']
    data = bytearray(image(imports=False, overlay=False, rwx=False))
    reference = b'URLDownloadToFileW\0' if urlmon else b'ordinary file reader\0'
    data[0x220:0x220 + len(reference)] = reference
    struct.pack_into('<II', data, 0x98 + 112, 0x3000, 0x1000)
    for offset in [0x600, 0x618, 0x630]:
        struct.pack_into('<IIHHHH', data, offset, 0, 0, 0, 0, 0, 1)
    for offset, key, target in [(0x610, 16, 0x80000018),
                                (0x628, 1, 0x80000030), (0x640, 0x409, 0x48)]:
        struct.pack_into('<II', data, offset, key, target)
    children = [] if company is None else [version_block('CompanyName', company.encode('utf-16le') + b'\0\0')]
    fixed = struct.pack('<13I', 0xfeef04bd, 0x10000, 0x10000, 0, 0x10000,
                        0, 0x3f, 0, 0x40004, 1, 0, 0, 0)
    version = version_block('VS_VERSION_INFO', fixed, [version_block('StringFileInfo', children=[
        version_block('040904B0', children=children)])], kind=0)
    struct.pack_into('<IIII', data, 0x648, 0x3100, len(version), 0, 0)
    data[0x700:0x700 + len(version)] = version
    # Independent resource label models a vendor name inside a preserved host.
    data[0xd00:0xd0a] = b'Microsoft\0'
    return data


def documents(text):
    decoder = json.JSONDecoder()
    text = text.lstrip()
    while text:
        value, end = decoder.raw_decode(text)
        yield value
        text = text[end:].lstrip()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sample', type=Path, required=True)
    parser.add_argument('--work-dir', type=Path, required=True)
    parser.add_argument('--cleave', default='cleave')
    args = parser.parse_args()
    args.work_dir.mkdir(parents=True, exist_ok=True)
    expected = {}

    def add(name, data, rules):
        path = args.work_dir / name
        path.write_bytes(data)
        expected[str(path)] = rules

    for name, company, urlmon, match in [
        ('claim-short.exe', 'Microsoft', True, True),
        ('claim-corp.exe', 'Microsoft Corporation', True, True),
        ('microsoft-forged.exe', 'Microsoft', True, True),
        ('renamed-claim.exe', 'Microsoft', True, True),
        ('other-company.exe', 'Example Utility', True, False),
        ('no-company.exe', None, True, False),
        ('no-urlmon.exe', 'Microsoft', False, False),
    ]:
        add(name, make_version_control(company, urlmon), {CLAIM: match, LABEL: True})

    raw = args.sample.read_bytes()
    starts = [raw.find(bytes.fromhex('7e360000047e' + field + '0000046fd900000a'))
              for field in ['11', '12', '13']]
    assert all(offset >= 0 for offset in starts), starts
    add('clipper-original.exe', raw, {SWAP: True, CLIPPER: True, RUN: True})
    for name, position, replacement in [
        ('different-source.exe', 23, bytes.fromhex('feff0004')),
        ('different-target.exe', 28, bytes.fromhex('feff0004')),
        ('different-result.exe', 38, b'\x09'),
        ('no-conditional.exe', 15, b'\x26'),
    ]:
        data = bytearray(raw)
        for offset in starts:
            data[offset + position:offset + position + len(replacement)] = replacement
        add(name, data, {SWAP: False, CLIPPER: False, RUN: True})
    data = raw
    for token in [r'\b(bc1|[13])', r'\b(0x)']:
        encoded = token.encode('utf-16le')
        assert encoded in data
        data = data.replace(encoded, b'X' * len(encoded))
    add('no-wallet-regex.exe', data, {SWAP: False, CLIPPER: False})
    token = b'AddClipboardFormatListener\0'
    assert token in raw
    add('no-listener.exe', raw.replace(token, b'X' * (len(token) - 1) + b'\0'),
        {SWAP: False, CLIPPER: False})
    data = raw.replace(b'Clipper\0', b'Changed\0').replace(b'NotificationForm\0', b'AlteredFormNames\0')
    assert len(data) == len(raw)
    add('renamed-types.exe', data, {SWAP: True, CLIPPER: True})
    token = 'SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run'.encode('utf-16le')
    assert token in raw
    add('no-run-key.exe', raw.replace(token, b'X' * len(token)), {RUN: False, SWAP: True})
    token = b'SetValue\0'
    assert token in raw
    add('no-registry-setter.exe', raw.replace(token, b'X' * (len(token) - 1) + b'\0'),
        {RUN: False, SWAP: True})

    result = subprocess.run([args.cleave, '--traits-dir', str(ROOT), '--disable',
                             'radare2,third-party', '--format', 'json', *expected],
                            capture_output=True, text=True)
    (args.work_dir / 'scan.json').write_text(result.stdout)
    (args.work_dir / 'scan.log').write_text(result.stderr)
    assert result.returncode == 0, result.stderr
    actual = {file['path']: {trait['id'] for trait in file.get('traits', [])}
              for doc in documents(result.stdout) for file in doc['files']}
    results = []
    for path, rules in expected.items():
        found = {rule: rule in actual[path] for rule in rules}
        assert found == rules, (path, rules, found)
        results.append({'case': Path(path).name, 'expected': rules, 'actual': found})
    (args.work_dir / 'results.json').write_text(json.dumps(results, indent=2) + '\n')
    print('%d static positive and near-miss controls passed' % len(results))


if __name__ == '__main__':
    main()
