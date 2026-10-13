"""Static review controls using private specimens; never execute an image.

python3 check.py --cleave ../cleave/target/release/cleave
No specimen bytes are checked into this repository. Mutants are inert controls,
not asserted benign software. Results default to the private audit directory.
"""
import argparse
import json
import pathlib
import subprocess

BASE = 'objectives/evasion/anti-av/verification::eset-update-signature-suppression-proxy'
TLS = 'micro-behaviors/communications/tls/verify/disable::x86-winhttp-ignore-certificate-errors'
SIGNED_TCL = 'well-known/lib/runtime/native-platform/tcl-tk::signed-tcl-tk-product'
EUPDATE = '6d39535074e2274ccc3a91feaae694881f0e1cc635202ab70c9dd5d4d2949874'
PACKED_EUPDATE = 'ecf5e0e083cc020803ab9c09b30f48e63980d82540a5424079b131f9c907d257'
SCANLINE = 'well-known/tool/sysadmin/network::foundstone-scanline'


def documents(text):
    decoder = json.JSONDecoder()
    while text.strip():
        text = text.lstrip()
        result, end = decoder.raw_decode(text)
        yield result
        text = text[end:]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--cleave', required=True)
    ap.add_argument('--source', type=pathlib.Path, default=pathlib.Path('/tmp/triage/sightings-pe/samples'))
    ap.add_argument('--audit', type=pathlib.Path, default=pathlib.Path('/tmp/triage/sightings-pe'))
    args = ap.parse_args()
    out = args.audit / 'controls'
    out.mkdir(parents=True, exist_ok=True)
    cases = []

    def add(name, data, expectations, suffix='.exe'):
        path = out / (name + suffix)
        path.write_bytes(data)
        cases.append({'name': name, 'path': str(path), 'expectations': expectations})

    def replace(data, old, new):
        assert len(old) == len(new) and data.count(old) >= 1
        return data.replace(old, new)

    original = (args.source / EUPDATE).read_bytes()
    for name in [EUPDATE, PACKED_EUPDATE]:
        add(name, (args.source / name).read_bytes(), {BASE: True, TLS: True})
    # A brand/author change must not bypass tampering or certificate relaxation.
    variant = replace(original, 'Eupdate Helper'.encode('utf-16le'), 'Routine Update'.encode('utf-16le'))
    add('eupdate-renamed-product', variant, {BASE: True, TLS: True})
    add('no-signed-resource-role', replace(original, b'.signed\0', b'.sigxxx\0'), {BASE: False, TLS: True})
    add('no-update-manifest-role', replace(original, b'[SERVERS]\0', b'[SOURCES]\0'), {BASE: False, TLS: True})

    # The existing signature-resource handler uses HTTP 404 at this site.
    response = bytes.fromhex('ba 94 01 00 00 89 d8')
    assert original.count(response) == 1
    add('http-200-reduction', replace(original, response, bytes.fromhex('ba c8 00 00 00 89 d8')),
        {BASE: False, TLS: True})

    # Reorder the same MOV, PUSH, TEST instructions into the earlier compiler
    # schedule. Relocations and API-to-slot binding remain unchanged.
    resolver = original.find(bytes.fromhex('c7 44 24 04 39 e7 41 00 89 04 24 ff d3'))
    assert resolver >= 0 and original[resolver+19] == 0xa3
    tail = original[resolver+19:resolver+28]
    assert tail[5:] == bytes.fromhex('51 51 85 d2')
    scheduled = bytes.fromhex('85 d2 51 51') + tail[:5]
    add('tls-alternate-instruction-schedule', original[:resolver+19] + scheduled + original[resolver+28:],
        {BASE: True, TLS: True})
    relax = original.find(bytes.fromhex('8d 45 98 c7 45 98 00 33 00 00'))
    assert relax >= 0
    for name, mask, expected in [('tls-one-error-bit', 0x1000, True), ('tls-no-error-bits', 0, False)]:
        variant = original[:relax+6] + mask.to_bytes(4, 'little') + original[relax+10:]
        add(name, variant, {BASE: True, TLS: expected})
    at = relax + 26
    assert original[at:at+4] == bytes.fromhex('1f 00 00 00')
    add('tls-option-84-is-protocol-selection', original[:at] + bytes.fromhex('54 00 00 00') + original[at+4:],
        {BASE: True, TLS: False})
    slot = int.from_bytes(original[resolver+20:resolver+24], 'little')
    add('tls-resolved-slot-mismatch', original[:resolver+20] + (slot+4).to_bytes(4, 'little') + original[resolver+24:],
        {BASE: True, TLS: False})

    for name in ['tcl86t.dll', 'tk86t.dll']:
        data = (args.source / name).read_bytes()
        add('renamed-' + name, data, {SIGNED_TCL: True, BASE: False}, suffix='.dll')
        # Alter a code byte while retaining the original signature blob. The
        # digest gate must fail; a basename alone must not supply the exception.
        at = 0x450
        damaged = data[:at] + bytes([data[at] ^ 1]) + data[at+1:]
        add('changed-code-' + name, damaged, {SIGNED_TCL: False, BASE: False}, suffix='.dll')

    scan = next(args.source.glob('eaef901b*')).read_bytes()
    add('scanline-packed', scan, {SCANLINE: True, BASE: False})
    add('scanline-unpacked', (args.audit / 'eaef-unpacked.exe').read_bytes(), {SCANLINE: True, BASE: False})
    add('peboot-control', next(args.source.glob('fc4eae33*')).read_bytes(), {BASE: False, TLS: False})

    for case in cases:
        run = subprocess.run([args.cleave, '--traits-dir', '.', '--format=json', case['path']],
                             capture_output=True, text=True, check=True)
        report = list(documents(run.stdout))[0]
        traits = {t['id']: t for t in report['files'][0]['traits']}
        case['actual'] = {i: i in traits for i in case['expectations']}
        case['pass'] = case['actual'] == case['expectations']
        print(json.dumps({'case': case['name'], 'pass': case['pass']}), flush=True)
    result = {'cases': cases, 'passed': sum(c['pass'] for c in cases), 'total': len(cases),
              'assertions': sum(len(c['expectations']) for c in cases)}
    (out / 'review.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: result[k] for k in ['passed', 'total', 'assertions']}))
    if result['passed'] != result['total']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
