"""Inert PE controls for neutral reference placement and field precision."""
import argparse
import importlib.util
import json
import re
import struct
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location('pe_fixture', ROOT / 'testdata/triage-sighted/build_pe_fixtures.py')
fixture = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fixture)


def block(key, value=b'', children=b'', kind=1):
    key = (key + '\0').encode('utf-16le')
    data = bytearray(struct.pack('<HHH', 0, len(value)//2 if kind else len(value), kind) + key)
    data += b'\0' * (-len(data) % 4)
    data += value
    data += b'\0' * (-len(data) % 4)
    data += children
    struct.pack_into('<H', data, 0, len(data))
    return bytes(data)


def version_image(name):
    leaf = block('OriginalFilename', (name+'\0').encode('utf-16le'))
    version = block('VS_VERSION_INFO', struct.pack('<13I', 0xFEEF04BD, 0x10000, *([0]*11)),
                    block('StringFileInfo', children=block('040904B0', children=leaf)), kind=0)
    image = bytearray(fixture.image(b'.rsrc', b'', 1100000))
    resource = bytearray(88)
    for off in [0, 24, 48]:
        struct.pack_into('<H', resource, off+14, 1)
    struct.pack_into('<II', resource, 16, 16, 0x80000018)
    struct.pack_into('<II', resource, 40, 1, 0x80000030)
    struct.pack_into('<II', resource, 64, 0x409, 72)
    struct.pack_into('<IIII', resource, 72, 0x1058, len(version), 0, 0)
    resource += version
    image[0x200:0x200+len(resource)] = resource
    struct.pack_into('<II', image, 0x98+96+16, 0x1000, len(resource))
    return bytes(image)


def export_image(names=('OpenSSL_version', 'EVP_EncryptInit')):
    image = bytearray(fixture.image(b'.rdata', b'', 0x1000))
    section = bytearray(0x400)
    count = len(names)
    struct.pack_into('<IIHHIIIIIII', section, 0, 0, 0, 0, 0, 0x10e0, 1, count, count, 0x1040, 0x1050, 0x1060)
    pos = 0x70
    for i, name in enumerate(names):
        raw = name.encode()+b'\0'
        struct.pack_into('<I', section, 0x40+i*4, 0x1200+i*16)
        struct.pack_into('<I', section, 0x50+i*4, 0x1000+pos)
        struct.pack_into('<H', section, 0x60+i*2, i)
        section[pos:pos+len(raw)] = raw
        section[0x200+i*16] = 0xc3
        pos += len(raw)
    section[0xe0:0xe8] = b'test.dll'
    image[0x200:0x600] = section
    struct.pack_into('<II', image, 0x98+96, 0x1000, 0x200)
    return bytes(image)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--work-dir', type=Path, required=True)
    parser.add_argument('--cleave', default='cleave')
    args = parser.parse_args()
    args.work_dir.mkdir(parents=True, exist_ok=True)
    positives = b'C:\\Windows\\explorer.exe\0TypeLib\\{11111111-1111-1111-1111-111111111111}\0\\System Volume Information\\\0'
    cases = {
        'pyinstaller-entries.exe': fixture.image(b'.rdata', b'mpyimod01_archive\0spyiboot01_bootstrap\0', 0x1000),
        'pyinstaller-one-entry.exe': fixture.image(b'.rdata', b'mpyimod01_archive\0', 0x1000),
        'ipc-exports.exe': export_image(('OpenEventW', 'OpenFileMappingW', 'SetEvent')),
        'ipc-one-api.exe': export_image(('SetEvent',)),
        'crypto-exports.exe': export_image(),
        'crypto-string-only.exe': fixture.image(b'.rdata', b'EVP_EncryptInit\0OpenSSL_version\0', 0x1000),
        'blowfish-reference.py': b'cipher_name = \"Blowfish\"\n',
        'blowfish-near-miss.py': b'cipher_name = \"Blowfisher\"\n',
        'references.exe': fixture.image(b'.rdata', positives, 0x1000),
        'reference-near-misses.exe': fixture.image(b'.rdata', b'explorer.executable\0TypeLibrary\\{11111111-1111-1111-1111-111111111111}\0\\System Volume Information.exe\\\0', 0x1000),
        'adobe-resource.exe': fixture.image(b'.rsrc', b'Adobe Reader\0', 0x1000),
        'adobe-wrong-section.exe': fixture.image(b'.rdata', b'Adobe Reader\0', 0x1000),
        'collabsync-field.exe': version_image('AdobeCollabSync.exe'),
        'collabsync-near-field.exe': version_image('Other.exe'),
        'collabsync-mention.exe': fixture.image(b'.rdata', b'AdobeCollabSync.exe\0', 1100000),
    }
    # A mention and an unrelated field must not stand in for OriginalFilename.
    mention = bytearray(cases['collabsync-near-field.exe'])
    mention[0x1000:0x1014] = b'AdobeCollabSync.exe\0\0'
    cases['collabsync-near-field.exe'] = bytes(mention)
    ids = [
        'micro-behaviors/fs/path/application/executable::explorer-executable-reference',
        'micro-behaviors/os/registry/keys/execution::typelib-registry-path',
        'micro-behaviors/fs/path/metadata-store::system-volume-information-path',
        'metadata/binary/resource/identity::adobe-reader-resource-text',
        'metadata/binary/provenance/version-info::adobe-collabsync-original-filename',
        'micro-behaviors/crypto/symmetric/blowfish::blowfish-keyword',
        'micro-behaviors/crypto/encrypt::openssl-evp-encrypt-init',
        'well-known/lib/crypto/openssl::openssl-version-symbol',
        'metadata/build/bundler/runtime::pyinstaller-pe-bundle-markers',
        'micro-behaviors/communications/ipc/file-mapping::mapping-event-api-set',
    ]
    expected = {'pyinstaller-entries.exe': [ids[8]], 'ipc-exports.exe': [ids[9]], 'crypto-exports.exe': ids[6:8], 'blowfish-reference.py': [ids[5]], 'references.exe': ids[:3], 'adobe-resource.exe': [ids[3]], 'collabsync-field.exe': [ids[4]]}
    results = {}
    for name, data in cases.items():
        path = args.work_dir / name
        path.write_bytes(data)
        proc = subprocess.run([args.cleave, '--traits-dir', str(ROOT), 'test-rules', str(path), '--rules', ','.join(ids)], capture_output=True, text=True, check=True)
        (args.work_dir / (name+'.trace.txt')).write_text(proc.stdout+proc.stderr)
        output = proc.stdout + proc.stderr
        assert 'not found' not in output and 'validation failed' not in output, output
        matched = set(re.findall(r'^MATCHED ([^ ]+)', output, re.M))
        assert matched == set(expected.get(name, [])), (name, matched, expected.get(name, []), output)
        results[name] = {'expected': expected.get(name, []), 'matched': sorted(matched), 'trace': str(path)+'.trace.txt'}
    (args.work_dir/'cases.json').write_text(json.dumps(results, indent=2)+'\n')
    print(json.dumps(results, indent=2))
