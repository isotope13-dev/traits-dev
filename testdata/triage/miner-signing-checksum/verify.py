"""Inert import-table and graphics-reference controls; no generated PE is run."""
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import runpy
import struct
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
pe_image = runpy.run_path(str(ROOT / 'testdata/native-rat-loader-triage/verify.py'))['pe_image']
PREFIX = 'micro-behaviors/ui/graphics/image::'
ASCII = 'micro-behaviors/hardware/input/keyboard/layout::to-ascii-import'
OWIN = 'micro-behaviors/communications/http/server/listener::owin-hosting-namespace'


def image(import_name=None, markers=b''):
    data = bytearray(512)
    if import_name:
        # Descriptor, ILT and IAT, followed by DLL and hint/name records.
        struct.pack_into('<5I', data, 0, 0x2040, 0, 0, 0x2080, 0x2060)
        struct.pack_into('<Q', data, 0x40, 0x2090)
        struct.pack_into('<Q', data, 0x60, 0x2090)
        data[0x80:0x8b] = b'user32.dll\0'
        name = import_name.encode() + b'\0'
        data[0x92:0x92+len(name)] = name
    data[0x100:0x100+len(markers)] = markers
    result = bytearray(pe_image(code=b'\xc3BSJB\0', data=bytes(data)))
    if import_name:
        struct.pack_into('<II', result, 0x98+112+8, 0x2000, 40)
    if import_name == '_CorExeMain':
        struct.pack_into('<II', result, 0x98+112+14*8, 0x21a0, 72)
        struct.pack_into('<IHHII', result, 0x5a0, 72, 2, 5, 0x1001, 8)
    return result


def main():
    dest = Path(sys.argv[1]); dest.mkdir(parents=True, exist_ok=True)
    bitmap = b'System.Drawing.Bitmap\0'
    resource = b'ResourceManager\0'
    # A CLR header and BSJB supply the managed-assembly observations.
    cases = {
        'toascii-import.exe': (image('ToAscii'), {ASCII}),
        'toascii-text.exe': (image(markers=b'ToAscii\0'), set()),
        'other-import.exe': (image('GetWindowTextA'), set()),
        'bitmap.exe': (image('_CorExeMain', bitmap), {PREFIX+'dotnet-bitmap-type-token'}),
        'resources.exe': (image('_CorExeMain', resource), set()),
        'bitmap-resources.exe': (image('_CorExeMain', bitmap+resource), {
            PREFIX+'dotnet-bitmap-type-token', PREFIX+'dotnet-bitmap-resource-api-references'}),
        'bitmap-pixels.exe': (image('_CorExeMain', bitmap+resource+b'GetPixel\0'), {
            PREFIX+'dotnet-bitmap-type-token', PREFIX+'dotnet-bitmap-resource-api-references',
            PREFIX+'dotnet-bitmap-resource-pixel-api-references'}),
        'owin.exe': (image(markers=b'Microsoft.Owin.Hosting\0'), {OWIN}),
        'owin-near-miss.exe': (image(markers=b'Microsoft.Owin.Security\0'), set()),
    }
    watched = {ASCII, OWIN} | {PREFIX+x for x in (
        'dotnet-bitmap-type-token', 'dotnet-bitmap-resource-api-references',
        'dotnet-bitmap-resource-pixel-api-references')}

    def check(item):
        name, (content, expected) = item
        path = dest / name; path.write_bytes(content)
        r = subprocess.run([os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
                            '--format', 'json', str(path)], capture_output=True, check=True)
        ids = {t['id'] for t in json.loads(r.stdout)['files'][0]['traits']}
        assert ids & watched == expected, (name, ids & watched, expected)
        assert not any(i.startswith('micro-behaviors/data/embedded/payload/image::dotnet-') for i in ids)
        return 'PASS '+name

    with ThreadPoolExecutor(max_workers=3) as pool:
        for result in pool.map(check, cases.items()): print(result)


if __name__ == '__main__':
    main()
