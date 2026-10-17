"""Check neutral relocations; optionally check the three reviewed specimens.

Usage: python3 check.py [dotnet-sample infected-idm-sample pstore-worm-sample]
Only static analysis is used. Specimen mutations stay in a temporary directory.
"""
import json
from pathlib import Path
import struct
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[3]
MICRO = 'micro-behaviors/'
INPUT = 'objectives/exfiltration/stealer/input::dotnet-hook-keylogger-http-upload'
FILE = 'objectives/exfiltration/stealer/file::managed-file-record-http-transfer'
SCREEN = 'objectives/exfiltration/stealer/screen::managed-screen-record-http-exfiltration'
USB = 'objectives/lateral-movement/usb-worm/autorun::managed-stealer-removable-autorun-replication'
POLL = 'objectives/collection/keylog/polling::dotnet-persisted-polling-keylog-recording'
HOOK = 'objectives/collection/keylog/hook::windows-hook-chain-recording-keylogger'


def minimal_pe(strings):
    """Data-only PE for name-reference controls, with no executable routine."""
    payload = b'\0'.join(x.encode() for x in strings) + b'\0'
    raw_size = (len(payload) + 511) & ~511
    data = bytearray(512 + raw_size)
    data[:2] = b'MZ'
    struct.pack_into('<I', data, 60, 128)
    data[128:132] = b'PE\0\0'
    struct.pack_into('<HHIIIHH', data, 132, 0x14c, 1, 0, 0, 0, 224, 0x102)
    opt = 152
    struct.pack_into('<H', data, opt, 0x10b)
    for off, value in [(28, 0x400000), (32, 4096), (36, 512),
                       (56, 8192), (60, 512), (92, 16)]:
        struct.pack_into('<I', data, opt + off, value)
    struct.pack_into('<H', data, opt + 68, 2)
    struct.pack_into('<8sIIIIIIHHI', data, 376, b'.rdata\0\0',
                     len(payload), 4096, raw_size, 512, 0, 0, 0, 0, 0x40000040)
    data[512:512 + len(payload)] = payload
    return bytes(data)


def reports(stdout):
    decoder = json.JSONDecoder()
    while stdout.strip():
        stdout = stdout.lstrip()
        report, end = decoder.raw_decode(stdout)
        yield from report['files']
        stdout = stdout[end:]


with tempfile.TemporaryDirectory(prefix='trait-review-') as tmp:
    tmp = Path(tmp)
    cases = []

    def case(name, data, present=(), absent=()):
        path = tmp / (name + '.exe')
        path.write_bytes(data)
        cases.append((path, set(present), set(absent)))

    names = ['audiodg', 'wininit', 'taskhost', 'fontdrvhost']
    tools = ['procmon', 'procexp', 'apimonitor', 'cheatengine', 'pestudio', 'peid', 'processhacker2']
    name_ids = {MICRO + 'process/info/name::' + name + '-name' for name in names}
    tool_ids = {MICRO + 'process/debug/tool-markers::' + name + '-tool-name-reference'
                for name in ['procmon', 'procexp', 'cheatengine', 'pestudio', 'peid']}
    tool_ids |= {MICRO + 'process/debug/tool-markers::api-monitor-tool-name-reference',
                 MICRO + 'process/debug/tool-markers::process-hacker-executable-name-reference'}
    policy_ids = {MICRO + 'os/registry/value-name::explorer-value-no-drives',
                  MICRO + 'os/registry/value-name::dialog-value-no-back-button'}
    getter = MICRO + 'data/property/access::dotnet-headers-getter-reference'
    case('neutral-references', minimal_pe([n + '.exe' for n in names + tools] +
                                        ['NoDrives', 'NoBackButton', 'get_Headers']),
         name_ids | tool_ids | policy_ids | {getter},
         {HOOK, INPUT, FILE, SCREEN, USB,
          MICRO + 'communications/http/server/managed::http-headers-getter'})
    case('near-miss-names', minimal_pe(['wininitializer.exe', 'mytaskhost.exe',
                                      'fontdrvhosting.exe', 'audiodg_helper.exe',
                                      'get_HeaderSize', 'NoDriveCount', 'NoBackButtons']),
         (), name_ids | policy_ids | {getter})

    if len(sys.argv) > 1:
        assert len(sys.argv) == 4, 'Pass all three specimen paths, in listed order'
        dotnet, idm, worm = (Path(p) for p in sys.argv[1:])
        cases += [(dotnet, {INPUT, FILE, SCREEN, USB, POLL},
                   {'objectives/evasion/process/injection/runtime::dotnet-pinvoke-process-injection',
                    'objectives/impact/ransom/encrypt-dotnet::dotnet-ransomware-encryptor'}),
                  (idm, {'well-known/malware/virus/floxif::floxif-file-infector'}, {HOOK, INPUT}),
                  (worm, {'objectives/credential-access/keychain/extract::pstore-password-report-acquisition',
                          'objectives/exfiltration/stealer/keychain::pstore-password-report-form-post-exfil',
                          'objectives/lateral-movement/usb-worm/autorun::compiled-linewise-autorun-self-copy-worm'},
                   {'objectives/evasion/masquerade/process/name::wininit-name',
                    'objectives/evasion/masquerade/process/name::taskhost-name'})]
        original = dotnet.read_bytes()
        for name, substitutions, present, absent in [
            ('no-file-record', [('FILE:', 'DATA:')], {INPUT, SCREEN, USB}, {FILE}),
            ('no-screen-record', [('SCREEN:', 'IMAGES:')], {INPUT, FILE, USB}, {SCREEN}),
            ('no-autorun-directive', [('open=', 'noop=')], {INPUT, FILE, SCREEN}, {USB}),
            ('no-keylog-record', [('KEYLOG:', 'STATUS:'), ('KEYLOG_BULK:', 'STATUS_BULK:')],
             (), {INPUT, FILE, SCREEN, USB, POLL}),
        ]:
            data = original
            for old, new in substitutions:
                data = data.replace(old.encode('utf-16le'), new.encode('utf-16le'))
            assert data != original and len(data) == len(original)
            case(name, data, present, absent)

    result = subprocess.run(['cleave', '--traits-dir', str(ROOT), '--format', 'json',
                             *(str(c[0]) for c in cases)],
                            check=True, capture_output=True, text=True)
    observed = {str(Path(f['path'])): {t['id'] for t in f.get('traits', [])}
                for f in reports(result.stdout)}
    assertions = 0
    for path, present, absent in cases:
        actual = observed[str(path)]
        assert present <= actual, (path.name, 'missing', sorted(present - actual))
        assert not absent & actual, (path.name, 'unexpected', sorted(absent & actual))
        assertions += len(present) + len(absent)
    print(f'{len(cases)} cases, {assertions} trait assertions passed')
