"""Build inert PE import-table controls; no executable code is emitted."""
from pathlib import Path
import struct


def image(library, api, overlay=b''):
    data = bytearray(0x600)
    data[:2] = b'MZ'
    struct.pack_into('<I', data, 0x3c, 0x80)
    data[0x80:0x84] = b'PE\0\0'
    struct.pack_into('<HHIIIHH', data, 0x84,
                     0x14c, 1, 0x65000000, 0, 0, 224, 0x102)
    optional = 0x98
    struct.pack_into('<H', data, optional, 0x10b)
    struct.pack_into('<III', data, optional + 16, 0, 0x1000, 0x1000)
    struct.pack_into('<III', data, optional + 28, 0x400000, 0x1000, 0x200)
    struct.pack_into('<HH', data, optional + 40, 4, 0)
    struct.pack_into('<HH', data, optional + 48, 4, 0)
    struct.pack_into('<II', data, optional + 56, 0x2000, 0x200)
    struct.pack_into('<H', data, optional + 68, 3)
    struct.pack_into('<IIIIII', data, optional + 72,
                     0x100000, 0x1000, 0x100000, 0x1000, 0, 16)
    struct.pack_into('<II', data, optional + 96 + 8, 0x1000, 40)
    struct.pack_into('<8sIIIIIIHHI', data, optional + 224,
                     b'.rdata\0\0', 0x400, 0x1000, 0x400, 0x200,
                     0, 0, 0, 0, 0x40000040)
    struct.pack_into('<IIIII', data, 0x200,
                     0x1050, 0, 0, 0x1080, 0x1060)
    struct.pack_into('<II', data, 0x250, 0x10a0, 0)
    struct.pack_into('<II', data, 0x260, 0x10a0, 0)
    dll = library.encode() + b'\0'
    data[0x280:0x280 + len(dll)] = dll
    symbol = b'\0\0' + api.encode() + b'\0'
    data[0x2a0:0x2a0 + len(symbol)] = symbol
    return bytes(data) + overlay


if __name__ == '__main__':
    root = Path(__file__).parent
    (root / 'actual-media-import.exe').write_bytes(
        image('DSOUND.dll', 'DirectSoundCreate'))
    (root / 'overlay-media-paths.exe').write_bytes(
        image('KERNEL32.dll', 'Sleep',
              '\\Device\\HarddiskVolume2\\Windows\\DSOUND.dll\0'
              '\\Device\\HarddiskVolume2\\Windows\\D3D11.dll\0'
              '\\Device\\HarddiskVolume2\\Windows\\DXGI.dll\0'
              '\\Device\\HarddiskVolume2\\Windows\\DWrite.dll\0'
              .encode('utf-16le')))
