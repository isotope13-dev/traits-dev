"""Static controls; optionally pass the three original sample paths in order."""
import json
import os
from pathlib import Path
import struct
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[3]
XOR = 'micro-behaviors/data/codec::x86-indexed-inplace-xor-buffer-loop'
RETIRED = 'objectives/exfiltration/http/upload::post-exfil-c2-bho-removal'
PREFIX = bytes.fromhex('55 8b ec 51 c7 45 fc 00 00 00 00 eb 09 8b 45 fc 83 c0 01 89 45 fc')
BODY = bytes.fromhex('8b 55 08 03 55 fc 0f be 02 33 45')
TAIL = bytes.fromhex('8b 4d 08 03 4d fc 88 01 eb')
RET = bytes.fromhex('8b 45 08 8b e5 5d c3')
COUNTED = PREFIX + bytes.fromhex('8b 4d fc 3b 4d 0c 7d 16') + BODY + b'\x10' + TAIL + b'\xd9' + RET
STRING = PREFIX + bytes.fromhex('8b 4d 08 51 ff 15 00 30 40 00 39 45 fc 7d 16') + BODY + b'\x0c' + TAIL + b'\xd2' + RET


def pe(payload, section=b'.text'):
    raw_size = (len(payload) + 511) & ~511
    data = bytearray(512 + raw_size)
    data[:2] = b'MZ'
    struct.pack_into('<I', data, 60, 128)
    data[128:132] = b'PE\0\0'
    struct.pack_into('<HHIIIHH', data, 132, 0x14c, 1, 0, 0, 0, 224, 0x102)
    struct.pack_into('<H', data, 152, 0x10b)
    for off, value in [(16, 4096), (28, 0x400000), (32, 4096), (36, 512),
                       (56, 8192), (60, 512), (92, 16)]:
        struct.pack_into('<I', data, 152 + off, value)
    struct.pack_into('<H', data, 152 + 68, 2)
    struct.pack_into('<8sIIIIIIHHI', data, 376, section,
                     len(payload), 4096, raw_size, 512, 0, 0, 0, 0, 0x60000020)
    data[512:512 + len(payload)] = payload
    return bytes(data)


with tempfile.TemporaryDirectory(prefix='xor-post-review-') as tmp:
    cases = []

    def case(name, data, present=(), absent=(XOR, RETIRED)):
        path = Path(tmp) / (name + '.exe')
        path.write_bytes(data)
        cases.append((path, set(present), set(absent)))

    case('counted-xor', pe(COUNTED), (XOR,), (RETIRED,))
    case('string-xor', pe(STRING), (XOR,), (RETIRED,))
    case('unpacked-section', pe(COUNTED, b'UPX0'), (XOR,), (RETIRED,))
    case('different-call-address', pe(STRING.replace(bytes.fromhex('00 30 40 00'),
                                                    bytes.fromhex('20 50 60 00'))),
         (XOR,), (RETIRED,))
    case('addition', pe(COUNTED.replace(b'\x33\x45\x10', b'\x03\x45\x10')))
    case('no-write', pe(COUNTED.replace(b'\x88\x01', b'\x8a\x01')))
    case('no-back-edge', pe(COUNTED.replace(b'\xeb\xd9', b'\x90\x90')))
    case('empty', pe(b'\xc3'))
    # A maintenance/cleanup utility can carry all three references. They do
    # not establish that any data source is collected or sent to an attacker.
    case('post-url-bho-only', pe(b'\xc3\0http://cleanup.vendor.test/\0'
         b'POST %s HTTP/1.1\r\nHost: %s\r\n'
         b'Content-Type: application/x-www-form-urlencoded\r\n'
         b'Content-length: %d\r\n\r\n%s\0'
         b'reg delete "HKLM\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Browser Helper Objects" /f\0'))

    if len(sys.argv) > 1:
        assert len(sys.argv) == 4, 'Pass injector, resource injector, PStore worm'
        injector = {
            'objectives/evasion/self-delete/process::native-dll-injector-shell-cleanup',
            'objectives/persistence/login/registry/autostart::active-setup-service-dll-injector',
            'objectives/persistence/system/service/loader::lanmanserver-resource-injection-hijack',
            'well-known/malware/botnet/stormattack::stormattack-service-dll-injector'}
        cases.extend((Path(path), injector, {XOR, RETIRED}) for path in sys.argv[1:3])
        cases.append((Path(sys.argv[3]), {
            XOR, 'objectives/credential-access/keychain/extract::pstore-password-report-acquisition',
            'objectives/exfiltration/stealer/keychain::pstore-password-report-form-post-exfil',
            'objectives/lateral-movement/usb-worm/autorun::compiled-linewise-autorun-self-copy-worm'}, {RETIRED}))

    result = subprocess.run([os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
                             '--format', 'json', *(str(c[0]) for c in cases)],
                            check=True, capture_output=True, text=True)
    decoder = json.JSONDecoder()
    remaining = result.stdout.strip()
    files = []
    while remaining:
        report, end = decoder.raw_decode(remaining)
        files.extend(report['files'])
        remaining = remaining[end:].lstrip()
    observed = {f['path']: f.get('traits', []) for f in files}
    assertions = 0
    for path, present, absent in cases:
        traits = observed[str(path)]
        actual = {t['id'] for t in traits}
        assert present <= actual, (path.name, 'missing', present - actual)
        assert not absent & actual, (path.name, 'unexpected', absent & actual)
        assertions += len(present) + len(absent)
        if path.parent == Path(tmp):
            assert not [t['id'] for t in traits if t.get('crit') == 5], path.name
            assertions += 1
    # Make the regression fixture prove all three original evidence legs.
    control = observed[str(Path(tmp) / 'post-url-bho-only.exe')]
    assert {t['id'] for t in control} >= {
        'micro-behaviors/communications/http/url/domain::http-url-binary',
        'micro-behaviors/communications/http/post::form-urlencoded-post-template',
        'micro-behaviors/os/registry/delete::bho-delete-command'}
    print(f'{len(cases)} cases, {assertions + 3} trait assertions passed')
