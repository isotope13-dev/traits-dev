"""Inert PE near misses and schema controls; never execute generated files."""
import json
import os
import struct
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CODEC = 'micro-behaviors/data/codec::x64-progressive-add-byte-decoder'
CHANNEL = 'objectives/command-and-control/channel/http/transport::concealed-browser-profile-control'
FIELDS = 'micro-behaviors/data/serialize/schema-object::compiled-app-profile-file-fields'
OLD_DECODER = bytes.fromhex(
    '40 b5 97 45 31 f6 42 8a 04 37 40 00 e8 0f b6 d0 48 89 d9 '
    'e8 00 00 00 00 49 ff c6 40 80 c5 03 4c 39 f6 75 e1')
UTF8_DECODER = bytes.fromhex(
    '40 b5 f5 45 31 ff 4c 8b 63 10 46 8a 2c 3f 45 31 f6 89 e8 44 00 e8 '
    '41 0f 98 c6 49 ff c6 48 89 d9 4c 89 f2 e8 12 9a 01 00 41 00 ed '
    '48 8b 44 24 28 48 8b 4c 24 30 79 15 44 89 ea c0 ea 06 41 80 e5 bf '
    '80 ca c0 44 88 6c 08 01 41 89 d5 44 88 2c 08 4d 01 f4 4c 89 64 24 30 '
    '49 ff c7 40 80 c5 f7 4c 39 fe 75 a6')
FEEDBACK = bytes.fromhex(
    '44 89 c1 80 e1 18 41 89 d2 41 d3 ea 44 30 c8 44 30 d0 42 32 04 0e '
    '42 88 04 0e 49 ff c1 41 83 c0 08 eb 01 89 d0 45 31 c0 4d 39 c7 '
    '74 01 42 8d 0c 00 42 d2 04 06 49 ff c0 eb 01')
VOCAB = [
    b'appIdpnsFilebprFile',
    b'OffsetEMOffsetEAOffsetLSOffsetTNSSAPSAC',
    b'reqwest-0.12.0', b'taskkill.exe/PID/F', b'--user-data-dir=',
]


def image(code=b'', literals=()):
    b = bytearray(0x4400)
    b[:2] = b'MZ'
    struct.pack_into('<I', b, 0x3c, 0x80)
    b[0x80:0x84] = b'PE\0\0'
    struct.pack_into('<HHIIIHH', b, 0x84, 0x8664, 2, 1700000000, 0, 0, 240, 0x22)
    opt = 0x98
    struct.pack_into('<H', b, opt, 0x20b)
    for off, val in {4:0x2000, 8:0x2000, 16:0x1000, 20:0x1000,
                     32:0x1000, 36:0x200, 56:0x5000, 60:0x400, 108:16}.items():
        struct.pack_into('<I', b, opt+off, val)
    struct.pack_into('<Q', b, opt+24, 0x140000000)
    struct.pack_into('<HH', b, opt+40, 6, 0)
    struct.pack_into('<H', b, opt+68, 2)
    for i, (name, va, raw, flags) in enumerate([
        (b'.text', 0x1000, 0x400, 0x60000020),
        (b'.rdata', 0x3000, 0x2400, 0x40000040),
    ]):
        struct.pack_into('<8sIIIIIIHHI', b, opt+240+40*i,
                         name, 0x2000, va, 0x2000, raw, 0, 0, 0, 0, flags)
    b[0x400] = 0xc3  # The entry returns; snippets below are unreachable.
    b[0x500:0x500+len(code)] = code
    data = b'\0'.join(literals)+b'\0'
    b[0x2400:0x2400+len(data)] = data
    return b


def main():
    with tempfile.TemporaryDirectory(prefix='native-viewer-controls-') as temp:
        td = Path(temp)
        cases = {}
        def pe(name, code, vocabulary, required=(), forbidden=()):
            path = td/(name+'.exe')
            path.write_bytes(image(code, vocabulary))
            cases[path] = (set(required), set(forbidden))
        pe('old-decoder', OLD_DECODER, [], [CODEC], [CHANNEL])
        pe('utf8-decoder', UTF8_DECODER, [], [CODEC], [CHANNEL])
        pe('wrong-add-operation', UTF8_DECODER.replace(b'\x41\x00\xed', b'\x41\x30\xed'),
           [], [], [CODEC, CHANNEL])
        pe('fields-alone', b'', VOCAB, [FIELDS], [CHANNEL])
        pe('profile-module', UTF8_DECODER+FEEDBACK, VOCAB, [CODEC, FIELDS, CHANNEL])
        pe('profile-order-variant', UTF8_DECODER+FEEDBACK,
           [b'appIdpnsFilerFilebp']+VOCAB[1:], [FIELDS, CHANNEL])
        for n in range(5):
            pe(f'missing-role-{n}', UTF8_DECODER+FEEDBACK,
               VOCAB[:n]+VOCAB[n+1:], [], [CHANNEL])
        pe('no-feedback-codec', UTF8_DECODER, VOCAB, [], [CHANNEL])
        # Fifteen unrelated lengths exhaust the broad decoder and its 2x
        # bucket before the Windows path. The exact-length candidate preserves it.
        strings = [bytes([65+n])*n for n in range(0x21, 0x30)]
        targets = [
            b'LOCALAPPDATA', b'python.exe',
            b'https://www.python.org/ftp/python/3.12.7/python-3.12.7-embed-amd64.zip',
            b'Microsoft\\Windows\\NtProfileIndex']
        expected = [
            'micro-behaviors/os/env/read::xor16-localappdata-name',
            'micro-behaviors/fs/path/application/interpreter::xor16-python-executable-name',
            'micro-behaviors/communications/http/download/helper::xor16-official-python-release-url',
            'micro-behaviors/fs/path/os/identity::xor16-microsoft-windows-relative-path']
        code, payload = bytearray(), bytearray()
        for text in strings+targets:
            start = 0x1100+len(code)
            source = 0x3000+len(payload)
            keypos = source+len(text)
            key=bytes((k*17+43)&255 for k in range(16))
            payload.extend(bytes(v^key[n%16] for n,v in enumerate(text))+key)
            code.extend(b'\x48\x8d\x0d'+struct.pack('<i',source-start-7))
            code.extend(b'\x48\x8d\x15'+struct.pack('<i',keypos-start-14))
            code.extend(b'\x48\x83\xf8'+bytes([len(text)])+b'\x74\x1c')
            code.extend(bytes.fromhex('41 89 c0 41 83 e0 0f 45 8a 04 10 44 32 04 08'))
            code.extend(b'\x90'*8)
        path=td/'late-xor-targets.exe'
        b=image(code)
        b[0x2400:0x2400+len(payload)]=payload
        path.write_bytes(b)
        cases[path]=(set(expected), {CHANNEL})
        path=td/'plaintext-decoder-near-miss.exe'
        path.write_bytes(image(b'',targets))
        cases[path]=(set(),set(expected))
        guid = '11111111-2222-3333-4444-555555555555'
        api = 'micro-behaviors/data/serialize/schema-object::api-id-guid-value'
        client = 'micro-behaviors/data/serialize/schema-object::client-app-guid-value'
        for name, data, required, forbidden in [
            ('direct', {'APIId':guid, 'ClientAppId':guid}, [api, client], []),
            ('properties', [{'Name':'APIId','Value':guid},
                            {'Name':'ClientAppId','Value':guid}], [api, client], []),
            ('wrong-property', {'Name':'APIIds','Value':guid}, [], [api, client]),
            ('short-guid', {'APIId':'1234', 'ClientAppId':'1234'}, [], [api, client]),
        ]:
            path=td/(name+'.json')
            path.write_text(json.dumps(data))
            cases[path]=(set(required),set(forbidden))
        run = subprocess.run(
            [os.environ.get('CLEAVE','cleave'), '--traits-dir', str(ROOT), '--format',
             'json', 'analyze', *map(str, cases)], capture_output=True, text=True)
        if run.returncode:
            raise RuntimeError(run.stderr)
        decoder = json.JSONDecoder()
        rest = run.stdout.lstrip()
        reports = []
        while rest:
            report, length = decoder.raw_decode(rest)
            reports.extend(report['files'])
            rest = rest[length:].lstrip()
        report = {'files': reports}
        for file in report['files']:
            path=Path(file['path'])
            required, forbidden=cases[path]
            ids={t['id'] for t in file.get('traits', [])}
            assert required <= ids, (path.name, 'missing', required-ids)
            assert not forbidden & ids, (path.name, 'unexpected', forbidden & ids)
            print(path.name, 'PASS')
        assert len(report['files']) == len(cases)

if __name__ == '__main__':
    main()
