"""Inert BMP/PE and JavaScript controls; no embedded code is executed.

Run: python3 testdata/bitmap-and-ui-triage/verify.py <scratch-directory>
"""
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import runpy
import struct
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
pe_image = runpy.run_path(str(ROOT / 'testdata/native-rat-loader-triage/verify.py'))['pe_image']
BMP = 'micro-behaviors/data/embedded/payload/image::bmp-rgb-column-pe-header'
BRACKET = 'objectives/anti-static/obfuscation/string/dynamic::hex-escaped-bracket-property'


def bitmap(valid=True, wrong_pointer=False):
    width, height = 2, 160
    data = bytearray(54 + width * height * 4)
    data[:2] = b'BM'
    struct.pack_into('<I', data, 2, len(data))
    struct.pack_into('<I', data, 10, 54)
    struct.pack_into('<IiiHHI', data, 14, 40, width, height, 1, 32, 0)
    header = bytearray(144)
    header[:3] = b'MZ\x90'
    struct.pack_into('<I', header, 60, 96 if wrong_pointer else 128)
    header[128:132] = b'PE\0\0' if valid else b'XX\0\0'
    for i, value in enumerate(header):
        pixel, channel = divmod(i, 3)
        data[54 + (height - 1 - pixel) * width * 4 + 2 - channel] = value
    return data


def wrap(data):
    image = bytearray(pe_image())[:1024]
    size = (len(data) + 511) // 512 * 512
    struct.pack_into('<I', image, 0x1b0 + 8, len(data))
    struct.pack_into('<I', image, 0x1b0 + 16, size)
    return image + data + bytes(size - len(data))


def main():
    dest = Path(sys.argv[1])
    dest.mkdir(parents=True, exist_ok=True)
    cases = {
        'column.exe': (wrap(bitmap()), BMP, True),
        'wrong-nt.exe': (wrap(bitmap(valid=False)), BMP, False),
        'wrong-pointer.exe': (wrap(bitmap(wrong_pointer=True)), BMP, False),
        'ordinary-image.exe': (wrap(bytes(1334)), BMP, False),
        'property.js': (rb'const value = obj["\x66\x6f\x6f"];', BRACKET, True),
        'translation.js': (rb'const values = ["\x66\x6f\x6f"];', BRACKET, False),
        'returned-array.js': (rb'function f() { return ["\x66\x6f\x6f"]; }', BRACKET, False),
    }
    def check(item):
        name, (data, trait, expected) = item
        path = dest / name
        path.write_bytes(data)
        result = subprocess.run([os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
                                 '--format', 'json', str(path)], capture_output=True, check=True)
        traits = json.loads(result.stdout)['files'][0]['traits']
        assert (trait in {t['id'] for t in traits}) == expected, (name, traits)
        assert not any(t['crit'] >= 4 for t in traits), (name, traits)
        return name
    with ThreadPoolExecutor(max_workers=3) as pool:
        for name in pool.map(check, cases.items()):
            print('PASS', name, flush=True)


if __name__ == '__main__':
    main()
