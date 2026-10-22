"""Inert PE controls for Beacon review; never executes machine code."""
import argparse
import importlib.util
import json
from pathlib import Path
import struct
import subprocess

ROOT = Path(__file__).resolve().parents[3]
HEADER = bytes.fromhex(
    '8b45088b4d0803483c894df88b55f8c7020000000033c08b4d086689018b5508c7423c00000000'
)
XOR = bytes.fromhex('80b0205003102e403bc77cf4')
STACK = bytes.fromhex('6a40506affff1500a10210')
INDIRECT = bytes.fromhex('8b3500a10210ffd6')
FOLD = bytes(range(33, 127)).lower()
ERASE = 'objectives/evasion/indicator-removal/structure::x86-erase-pe-dos-signatures'
LOOP = 'micro-behaviors/data/encoding/xor::x86-register-bounded-constant-xor-loop'
STACK_ID = 'metadata/binary/instruction/operand::x86-40-minus-one-indirect-call'
PROFILE = 'micro-behaviors/mem/combined::x86-protectex-indirect-call-profile'
ROUTE = 'micro-behaviors/communications/http/url/telemetry::versioned-telemetry-route'
V1 = 'micro-behaviors/communications/http/url/telemetry::api-v1-telemetry-path'
USER = 'micro-behaviors/os/user/lookup::get-user-name-ansi-text'
OLD = 'objectives/anti-static/obfuscation/payload/encoded/exec::x86-rwx-obfuscated-memory-dispatch'


def image(header=HEADER, loop=XOR, route=b'/api/v1/telemetry', header_in_data=False):
    spec = importlib.util.spec_from_file_location(
        'beacon_fixture', ROOT / 'testdata/triage/beacon-malformed-dns/check.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    data = bytearray(module.fixture(omit=('one', 'four', 'control', 'dns', 'reflective', 'generic')))
    data[:60] = bytes(60)
    data[:2] = b'MZ'
    # Use identical raw offsets/RVAs so proximity uses one coordinate system.
    # Entry point returns; snippets near the IAT are unreachable test data.
    struct.pack_into('<IIII', data, 384, 0x1000, 0x1000, 0x1000, 0x1000)
    struct.pack_into('<II', data, 424, 0x1000, 0x2000)
    struct.pack_into('<II', data, 432, 0x1000, 0x2000)
    struct.pack_into('<II', data, 152 + 104, 0x2200, 40)
    data[0x1000] = 0xc3
    code = b'\xc3' + STACK + INDIRECT + (b'' if header_in_data else header) + loop
    data[0x1f40:0x1f40 + len(code)] = code
    strings = FOLD + b'\0' + route + b'\0'
    if header_in_data:
        strings += header
    data[0x2000:0x2000 + len(strings)] = strings
    struct.pack_into('<IIIII', data, 0x2200, 0x2300, 0, 0, 0x2280, 0x1ff0)
    data[0x2280:0x228d] = b'KERNEL32.dll\0'
    pos = 0x2500
    for index, name in enumerate((b'VirtualProtectEx', b'GetUserNameA')):
        struct.pack_into('<I', data, 0x2300 + index * 4, pos)
        struct.pack_into('<I', data, 0x1ff0 + index * 4, pos)
        value = b'\0\0' + name + b'\0'
        data[pos:pos + len(value)] = value
        pos = (pos + len(value) + 1) & ~1
    return bytes(data)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cleave', default='cleave')
    parser.add_argument('--work-dir', type=Path, required=True)
    args = parser.parse_args()
    args.work_dir.mkdir(parents=True, exist_ok=True)
    fixtures = args.work_dir / 'fixtures'
    fixtures.mkdir(exist_ok=True)
    cases = {
        'complete': (image(), True, True, True, True),
        'non-header-field-cleared': (image(header=HEADER.replace(b'\xc7\x42\x3c', b'\xc7\x42\x38')),
                                     False, True, True, True),
        'header-bytes-only-in-data': (image(header_in_data=True), False, True, True, True),
        'no-backward-xor-branch': (image(loop=XOR[:-1] + b'\0'), True, False, True, True),
        'different-xor-address-key': (image(loop=bytes.fromhex('80b0785634125a403bc67cf4')),
                                      True, True, True, True),
        'crt-and-api-profile-only': (image(header=b'', loop=b''), False, False, True, True),
        'version-two-beacon-path': (image(route=b'/api/v2/beacon'), True, True, True, False),
        'unrelated-api-path': (image(route=b'/api/v1/report'), True, True, False, False),
    }
    for name, (data, *_expected) in cases.items():
        (fixtures / (name + '.dll')).write_bytes(data)
    run = subprocess.run([args.cleave, '--traits-dir', str(ROOT), '--format', 'json', str(fixtures)],
                         capture_output=True, text=True, check=True)
    (args.work_dir / 'report.json').write_text(run.stdout)
    assert not run.stderr.strip(), run.stderr
    # Directory scans can stream adjacent complete report objects.
    decoder = json.JSONDecoder()
    pending = run.stdout
    files = []
    while pending.strip():
        part, length = decoder.raw_decode(pending.lstrip())
        files.extend(part['files'])
        pending = pending.lstrip()[length:]
    results = []
    for file in files:
        name = Path(file['path']).stem
        traits = {t['id']: t for t in file['traits']}
        expected = cases[name][1:]
        actual = tuple(r in traits for r in (ERASE, LOOP, ROUTE, V1))
        assert actual == expected, (name, actual, expected)
        assert STACK_ID in traits and USER in traits, (name, 'lost relocated evidence')
        assert PROFILE in traits and traits[PROFILE]['crit'] == 3, (name, 'neutral API profile')
        assert OLD not in traits, (name, 'unsupported decode-to-execution claim')
        assert not [t for t in file['traits'] if t['crit'] >= 5], (name, 'inert fixture marked hostile')
        if name == 'crt-and-api-profile-only':
            assert 'metadata/binary/instruction/sequence::x86-global-pointer-indirect-call' in traits
            assert FOLD in cases[name][0]  # The old third leg is an ordinary CRT table.
        results.append({'case': name, 'pass': True})
    assert len(results) == len(cases), (len(results), len(cases))
    (args.work_dir / 'results.json').write_text(json.dumps(results, indent=2) + '\n')
    print(json.dumps(results, indent=2))


if __name__ == '__main__':
    main()
