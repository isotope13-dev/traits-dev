#!/usr/bin/env python3
"""Scan inert PE controls; never execute a fixture or specimen."""
import argparse
from pathlib import Path
import struct
import subprocess


def pe(text=b'\xc3', data=b''):
    """Two-section PE32 carrying inert code and configuration data."""
    image = bytearray(1536)
    image[:2] = b'MZ'
    struct.pack_into('<I', image, 0x3c, 0x80)
    image[0x80:0x84] = b'PE\0\0'
    struct.pack_into('<HHIIIHH', image, 0x84, 0x14c, 2, 0, 0, 0, 224, 0x102)
    optional = 0x98
    struct.pack_into('<H', image, optional, 0x10b)
    struct.pack_into('<III', image, optional + 16, 0x1000, 0x1000, 0x2000)
    struct.pack_into('<III', image, optional + 28, 0x400000, 0x1000, 0x200)
    struct.pack_into('<II', image, optional + 56, 0x3000, 0x200)
    struct.pack_into('<H', image, optional + 68, 3)
    struct.pack_into('<I', image, optional + 92, 16)
    for i, (name, rva, offset, flags, body) in enumerate([
        (b'.text', 0x1000, 0x200, 0x60000020, text),
        (b'.data', 0x2000, 0x400, 0xc0000040, data),
    ]):
        struct.pack_into('<8sIIIIIIHHI', image, optional + 224 + i * 40,
                         name, len(body), rva, 512, offset, 0, 0, 0, 0, flags)
        image[offset:offset + len(body)] = body
    return image


def setting(index, kind=3, length=64):
    value = b'%windir%\\system32\\worker.exe'
    return struct.pack('>HHH', index, kind, length) + value.ljust(length, b'\0')


parser = argparse.ArgumentParser()
parser.add_argument('scratch', type=Path)
args = parser.parse_args()
args.scratch.mkdir(parents=True, exist_ok=True)
root = Path(__file__).resolve().parents[2]
prefix = 'well-known/malware/rat/cobalt-strike/config::'
pixel = 'micro-behaviors/ui/graphics/image::'
cases = {
    'x86-setting.exe': (pe(data=setting(29)), {prefix + 'cfg-spawn-x86'},
                        {prefix + 'cfg-spawn-x64'}),
    'x64-setting.exe': (pe(data=setting(30)), {prefix + 'cfg-spawn-x64'},
                        {prefix + 'cfg-spawn-x86'}),
    'both-settings.exe': (pe(data=setting(29) + setting(30)),
                          {prefix + 'cfg-spawn-x86', prefix + 'cfg-spawn-x64',
                           prefix + 'cfg-spawn-any'}, set()),
    'wrong-type.exe': (pe(data=setting(29, kind=1)), set(),
                       {prefix + 'cfg-spawn-x86'}),
    'other-setting.exe': (pe(data=setting(13)), set(),
                          {prefix + 'cfg-spawn-x86'}),
    'legacy-instructions.exe': (pe(text=bytes.fromhex('00 0d 00 80 00 00 c3')),
                                set(), {prefix + 'cfg-spawn-x86'}),
    'native-pixel.exe': (pe(data=b'GetPixel\0'),
                         {pixel + 'getpixel-api-name', pixel + 'pixel-operation-references',
                          pixel + 'pixel-operation-or-layout-references'}, set()),
}
for name, (body, present, absent) in cases.items():
    path = args.scratch / name
    path.write_bytes(body)
    # Partial headers may be stripped from normal output when no meaningful
    # consumer fires. Debug evaluation checks matching independently of that
    # presentation behavior, including negative component controls.
    result = subprocess.run(['cleave', '--traits-dir', str(root), 'test-rules',
                             str(path), '--rules', ','.join(sorted(present | absent))],
                            capture_output=True, text=True)
    if result.returncode not in (0, 1):
        raise RuntimeError(result.stderr)
    actual = {line.split()[1] for line in result.stdout.splitlines()
              if line.startswith('MATCHED ')}
    assert present <= actual, (name, 'missing', present - actual)
    assert not actual & absent, (name, 'unexpected', actual & absent)
    print('PASS', name)
