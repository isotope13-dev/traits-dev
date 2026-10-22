"""Build inert PE/source controls; no specimen or generated code is executed."""
import argparse
import json
import struct
from pathlib import Path

HERE = Path(__file__).parent
BRANCH = 'objectives/anti-static/obfuscation/instruction/junk::repeated-complementary-branches-over-junk'
TLS = 'micro-behaviors/communications/tls/verify/disable::x64-winhttp-frame-certificate-ignore-call'
HTTP = 'micro-behaviors/communications/http/client/winhttp::winhttp-file-folder-com-api-set'
EMBED = 'metadata/lang/source/syntax/directive::go-embed-library-or-payload-asset'
MAP = 'metadata/package/integrity::library-payload-map-sha256-value'
OLD_TLS = 'micro-behaviors/communications/tls/verify/disable::x64-winhttp-certificate-ignore-call-setup'


def image(imports, code=b'', executable=True):
    data = bytearray(0x2000)
    data[:2] = b'MZ'
    struct.pack_into('<I', data, 0x3c, 0x80)
    data[0x80:0x84] = b'PE\0\0'
    struct.pack_into('<HHIIIHH', data, 0x84, 0x8664, 3, 1600000000, 0, 0, 240, 0x22)
    opt = 0x98
    struct.pack_into('<H', data, opt, 0x20b)
    struct.pack_into('<Q', data, opt+24, 0x180000000)
    for off, value in {4:0x800, 8:0x1400, 16:0x1000, 20:0x1000, 32:0x1000,
                       36:0x200, 56:0x4000, 60:0x400, 108:16}.items():
        struct.pack_into('<I', data, opt+off, value)
    struct.pack_into('<HH', data, opt+40, 6, 0)
    struct.pack_into('<HH', data, opt+48, 6, 0)
    struct.pack_into('<H', data, opt+68, 3)
    for i, (name, rva, raw, size, flags) in enumerate([
        (b'.text', 0x1000, 0x400, 0x800, 0x60000020 if executable else 0x40000040),
        (b'.idata', 0x2000, 0xc00, 0x1000, 0xc0000040),
        (b'.rdata', 0x3000, 0x1c00, 0x400, 0x40000040),
    ]):
        struct.pack_into('<8sIIIIIIHHI', data, opt+240+i*40,
                         name, size, rva, size, raw, 0, 0, 0, 0, flags)
    # All synthetic instructions follow an immediate return.
    data[0x400] = 0xc3
    data[0x410:0x410+len(code)] = code
    cursor = 0x100
    slots = {}
    if imports:
        struct.pack_into('<II', data, opt+120, 0x2000, (len(imports)+1)*20)
    for index, (library, names) in enumerate(imports.items()):
        lib_rva = 0x2000+cursor
        blob = library.encode()+b'\0'
        data[0xc00+cursor:0xc00+cursor+len(blob)] = blob
        cursor = (cursor+len(blob)+7)&~7
        lookup = 0x2000+cursor
        cursor += (len(names)+1)*8
        iat = 0x2000+cursor
        cursor += (len(names)+1)*8
        struct.pack_into('<IIIII', data, 0xc00+index*20, lookup, 0, 0, lib_rva, iat)
        for n, name in enumerate(names):
            cursor = (cursor+1)&~1
            name_rva = 0x2000+cursor
            encoded = b'\0\0'+name.encode()+b'\0'
            data[0xc00+cursor:0xc00+cursor+len(encoded)] = encoded
            struct.pack_into('<Q', data, 0xc00+lookup-0x2000+n*8, name_rva)
            struct.pack_into('<Q', data, 0xc00+iat-0x2000+n*8, name_rva)
            slots[name] = iat+n*8
            cursor += len(encoded)
    assert cursor < 0x1000
    return data, slots


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    cases = []

    def add(name, data, expected):
        (args.output/name).write_bytes(data)
        cases.append({'path':str(args.output/name),
                      'matched':[k for k,v in expected.items() if v],
                      'not_matched':[k for k,v in expected.items() if not v]})

    # Branch polarity and displacement must both agree. Bytes in data do not count.
    pair = bytes.fromhex('77 12 76 10')+b'\xcc'*16
    for name, code, executable, expected in [
        ('eight-branches.exe', pair*8, True, True),
        ('seven-branches.exe', pair*7, True, False),
        ('different-targets.exe', pair.replace(b'\x76\x10', b'\x76\x0f')*8, True, False),
        ('same-condition.exe', pair.replace(b'\x76\x10', b'\x77\x10')*8, True, False),
        ('branches-in-data.exe', pair*8, False, False),
    ]:
        add(name, image({}, code, executable)[0], {BRANCH:expected, TLS:False})

    # Bound option, flag mask, local address and imported call target.
    data, slots = image({'WINHTTP.dll':['WinHttpSetOption', 'WinHttpQueryHeaders']})
    setup = bytearray.fromhex('c7 85 00 0c 00 00 00 31 00 00 4c 8d 85 00 0c 00 00 '
                              '48 8b 8d a8 0f 00 00 ba 1f 00 00 00 '
                              '41 b9 04 00 00 00 ff 15 00 00 00 00')
    struct.pack_into('<i', setup, 37, slots['WinHttpSetOption']-(0x1010+41))
    for name, offset, replacement, expected in [
        ('tls-ignore.exe', None, b'', True),
        ('tls-protocol-option.exe', 25, b'\x54', False),
        ('tls-no-ignore.exe', 6, bytes(4), False),
        ('tls-different-local.exe', 13, b'\x04', False),
        ('tls-wrong-api.exe', 37, struct.pack('<i', slots['WinHttpQueryHeaders']-(0x1010+41)), False),
    ]:
        code = setup.copy()
        if offset is not None:
            code[offset:offset+len(replacement)] = replacement
        copy = data.copy()
        copy[0x410:0x410+len(code)] = code
        add(name, copy, {TLS:expected, BRANCH:False})

    # Preserve the pre-existing R12-indirect WinHTTP variant in the edited file.
    load = bytearray.fromhex('4c 8b 25 00 00 00 00 41 ff d4')
    struct.pack_into('<i', load, 3, slots['WinHttpSetOption']-(0x1010+7))
    relax = bytes.fromhex('41 b9 04 00 00 00 4c 8d 44 24 64 ba 1f 00 00 00 '
                           '48 89 d9 c7 44 24 64 00 33 00 00 41 ff d4')
    for name, body, expected in [
        ('tls-existing-r12.exe', relax, True),
        ('tls-existing-r12-no-flags.exe', relax[:23]+bytes(4)+relax[27:], False),
    ]:
        copy = data.copy()
        code = load+b'\x90'*16+body
        copy[0x410:0x410+len(code)] = code
        add(name, copy, {OLD_TLS:expected, TLS:False})

    imports = {'WINHTTP.dll':['WinHttpOpen', 'WinHttpConnect', 'WinHttpOpenRequest',
               'WinHttpSendRequest', 'WinHttpReceiveResponse', 'WinHttpReadData', 'WinHttpCloseHandle',
               'WinHttpSetTimeouts'],
               'KERNEL32.dll':['CreateFileA', 'WriteFile'],
               'SHELL32.dll':['SHGetFolderPathA'], 'ole32.dll':['CoCreateInstance']}
    add('inert-http-file-com-imports.exe', image(imports)[0], {HTTP:True, BRANCH:False, TLS:False})
    del imports['ole32.dll']
    add('http-file-without-com.exe', image(imports)[0], {HTTP:False})
    add('embed.go', b'package assets\nimport _ "embed"\n//go:embed assets/windows-amd64.payload\nvar payload []byte\n', {EMBED:True})
    add('ordinary-embed.go', b'package assets\n//go:embed logo.png\nvar logo []byte\n', {EMBED:False})
    add('manifest.json', json.dumps({'libraries':{'windows/amd64/helper.dll':'a'*64}}).encode(), {MAP:True})
    add('non-digest.json', b'{"libraries":{"helper.dll":"not a digest"}}', {MAP:False})
    (args.output/'cases.json').write_text(json.dumps({'fixtures':cases}, indent=2)+'\n')
    print(f'Wrote {len(cases)} inert controls')


if __name__ == '__main__':
    main()
