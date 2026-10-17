"""Offline controls; never execute specimens or fetch their endpoints.

Usage: python3 check.py EUPDATE_A STORM EUPDATE_B SCRATCH
Generated binary controls stay in SCRATCH, outside the trait repository.
"""
import json
import os
from pathlib import Path
import struct
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
FLOOD = 'objectives/impact/dos/attack/flood::native-raw-udp-burst-flood'
IMPLANT = 'well-known/malware/botnet/stormattack::stormattack-packet-tasked-ddos-implant'
RECORD = 'micro-behaviors/communications/socket/receive::x86-recv-copied-record-dispatch'
LAYOUT = 'metadata/binary/section/header::small-pe-modified-stub-writable-entry-padding'
ROTATION = 'micro-behaviors/fs/write/file/executable::self-hash-rotation-relaunch'


def inert_pe(data):
    """Non-launchable PE with a writable data section and trailing padding."""
    buf = bytearray(1024 + max(16384, ((len(data) + 511) // 512) * 512))
    buf[:2] = b'MZ'
    struct.pack_into('<I', buf, 0x3c, 0x80)
    buf[0x80:0x84] = b'PE\0\0'
    struct.pack_into('<HHIIIHH', buf, 0x84, 0x14c, 1, 0, 0, 0, 224, 0x102)
    opt = 0x98
    struct.pack_into('<H', buf, opt, 0x10b)
    struct.pack_into('<II', buf, opt + 16, 0x1000, 0x1000)
    struct.pack_into('<I', buf, opt + 28, 0x400000)
    struct.pack_into('<II', buf, opt + 32, 0x1000, 0x200)
    struct.pack_into('<II', buf, opt + 56, 0x8000, 0x400)
    struct.pack_into('<H', buf, opt + 68, 2)
    struct.pack_into('<I', buf, opt + 92, 16)
    sec = opt + 224
    buf[sec:sec + 8] = b'.data\0\0\0'
    struct.pack_into('<IIII', buf, sec + 8, len(data), 0x1000, len(buf) - 1024, 1024)
    struct.pack_into('<I', buf, sec + 36, 0xc0000040)
    buf[1024:1024 + len(data)] = data
    return bytes(buf) + bytes(1024)


def main():
    first, outer, second = [Path(p).read_bytes() for p in sys.argv[1:4]]
    work = Path(sys.argv[4]) / 'controls'
    work.mkdir(parents=True, exist_ok=True)
    assert outer[0x8060:0x8062] == b'MZ'
    dll = outer[0x8060:]
    assert first[0x400:0x21c00] == second[0x400:0x21c00]

    def replace_once(data, old, new):
        assert len(old) == len(new) and data.count(old) == 1
        return data.replace(old, new)

    raw = bytes.fromhex('53 53 53 6a 11 6a 03 6a 02')
    burst = bytes.fromhex('6a 0c 5e 8d 45 e8 6a 10')
    record = bytes.fromhex('56 68 28 05 00 00 ff 75 fc 53 ff 15')
    renamed = first.replace('Eupdate Helper'.encode('utf-16le'),
                            'Routine Helper'.encode('utf-16le'))
    renamed = renamed.replace(b'47.108.48.69', b'93.184.216.3')
    readonly = bytearray(inert_pe(b'\xc3ordinary application data\0'))
    struct.pack_into('<I', readonly, 0x19c, 0x40000040)
    cases = {
        'eupdate-a.exe': first,
        'eupdate-b.exe': second,
        'renamed-updater.exe': renamed,
        'storm-original.dll': dll,
        'storm-no-raw.dll': replace_once(dll, raw, raw[:4] + b'\x06' + raw[5:]),
        'storm-no-burst.dll': replace_once(dll, burst, b'\x6a\x01' + burst[2:]),
        'storm-no-record.dll': replace_once(dll, record, b'\x56\x68\x24' + record[3:]),
        'storm-renamed-version.dll': dll.replace('Storm Ser DLL'.encode('utf-16le'),
                                                'Plain Ser DLL'.encode('utf-16le')),
        'inert-layout.exe': inert_pe(b'\xc3ordinary application data\0'),
        'inert-strings.exe': inert_pe(b'wsock32.dll\0StormServer.dll\0' +
                                     'Storm Ser DLL'.encode('utf-16le') + b'\0\0'),
        'inert-record.exe': inert_pe(dll[0x5f3b:0x5fac]),
        'inert-readonly.exe': bytes(readonly),
    }
    paths = []
    for name, data in cases.items():
        path = work / name
        path.write_bytes(data)
        paths.append(str(path))
    result = subprocess.run([os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
                             '--format', 'json', *paths], capture_output=True, text=True,
                            check=True)
    (work / 'reports.jsonl').write_text(result.stdout)
    (work / 'stderr.txt').write_text(result.stderr)
    decoder = json.JSONDecoder()
    remaining = result.stdout.strip()
    reports = []
    while remaining:
        report, stop = decoder.raw_decode(remaining)
        reports.append(report)
        remaining = remaining[stop:].strip()
    observed = {Path(f['path']).name: {t['id']: t for t in f['traits']}
                for report in reports for f in report['files']}
    summary = []
    for name in cases:
        traits = observed[name]
        hostile = sorted(k for k, v in traits.items() if v['crit'] == 5)
        suspicious = sorted(k for k, v in traits.items() if v['crit'] == 4)
        if 'updater' in name or name.startswith('eupdate-'):
            assert not hostile and suspicious == [ROTATION], (name, hostile, suspicious)
        elif name.startswith('inert-'):
            assert not hostile and not suspicious, (name, hostile, suspicious)
            assert (LAYOUT in traits) == (name != 'inert-readonly.exe'), name
        else:
            assert (FLOOD in traits) == (name not in ['storm-no-raw.dll', 'storm-no-burst.dll']), name
            assert (IMPLANT in traits) == (name == 'storm-original.dll'), name
            assert (RECORD in traits) == (name != 'storm-no-record.dll'), name
            assert LAYOUT in traits, name
            assert 'objectives/anti-static/pack/overlay::tiny-writable-entry-stub-with-overlay' not in traits
        summary.append(dict(case=name, hostile=hostile, suspicious=suspicious))
    print(json.dumps({'cases': len(cases), 'failures': [], 'results': summary}, indent=2))


if __name__ == '__main__':
    main()
