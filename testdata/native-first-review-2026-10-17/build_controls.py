"""Inert PE64 matcher controls. Entry returns; signature bytes are unreachable."""
import struct
from pathlib import Path

ROOT = Path(__file__).parent


def image(mode='positive'):
    data = bytearray(0xe00)
    data[:2] = b'MZ'
    struct.pack_into('<I', data, 0x3c, 0x80)
    data[0x80:0x84] = b'PE\0\0'
    struct.pack_into('<HHIIIHH', data, 0x84, 0x8664, 2, 1700000000, 0, 0, 240, 0x22)
    opt = 0x98
    struct.pack_into('<H', data, opt, 0x20b)
    for off, val in {4: 0x400, 8: 0x800, 16: 0x1000, 20: 0x1000,
                     32: 0x1000, 36: 0x200, 56: 0x3000, 60: 0x200,
                     108: 16}.items():
        struct.pack_into('<I', data, opt + off, val)
    struct.pack_into('<Q', data, opt + 24, 0x140000000)
    struct.pack_into('<H', data, opt + 68, 3)
    struct.pack_into('<II', data, opt + 120, 0x2000, 60)
    for i, (name, rva, size, raw, flags) in enumerate([
        (b'.text', 0x1000, 0x400, 0x200, 0x60000020),
        (b'.rdata', 0x2000, 0x800, 0x600, 0x40000040),
    ]):
        struct.pack_into('<8sIIIIIIHHI', data, opt + 240 + 40 * i,
                         name, size, rva, size, raw, 0, 0, 0, 0, flags)
    imports = [
        ('ntdll.dll', ['NtSetInformationFile', 'NtWriteFile', 'NtCreateSection', 'NtMapViewOfSection']),
        ('KERNEL32.dll', ['SetThreadContext', 'GetThreadContext', 'ResumeThread']),
    ]
    slots = {}
    name_pos = 0x900
    for i, (dll, names) in enumerate(imports):
        dll_pos = 0x680 + i * 0x30
        data[dll_pos:dll_pos + len(dll) + 1] = dll.encode() + b'\0'
        ilt, iat = 0x700 + i * 0x60, 0x800 + i * 0x60
        struct.pack_into('<IIIII', data, 0x600 + 20 * i,
                         ilt + 0x1a00, 0, 0, dll_pos + 0x1a00, iat + 0x1a00)
        for j, name in enumerate(names):
            data[name_pos:name_pos + len(name) + 3] = b'\0\0' + name.encode() + b'\0'
            struct.pack_into('<Q', data, ilt + 8 * j, name_pos + 0x1a00)
            struct.pack_into('<Q', data, iat + 8 * j, name_pos + 0x1a00)
            slots[name] = iat + 8 * j + 0x1a00
            name_pos += len(name) + 3
            name_pos += name_pos % 2
    data[0x200] = 0xc3
    dispose = bytearray.fromhex(
        'c6 84 24 98 00 00 00 01 41 b9 01 00 00 00 c7 44 24 20 0d 00 00 00 '
        '4c 8d 84 24 98 00 00 00 48 8b c8 48 8d 54 24 60 0f 11 44 24 60 ff 15 00 00 00 00')
    if mode == 'wrong-disposition-buffer':
        dispose[26] = 0x99
    elif mode == 'keep-file':
        dispose[7] = 0
    dest = 'NtWriteFile' if mode == 'wrong-disposition-call' else 'NtSetInformationFile'
    struct.pack_into('<i', dispose, len(dispose) - 4, slots[dest] - (0x1040 + len(dispose)))
    data[0x240:0x240 + len(dispose)] = dispose
    image_setup = bytearray.fromhex('c7 44 24 28 00 00 00 01 45 33 c9 ff 15 00 00 00 00')
    dest = 'NtWriteFile' if mode == 'wrong-image-call' else 'NtCreateSection'
    struct.pack_into('<i', image_setup, 13, slots[dest] - (0x10c0 + len(image_setup)))
    data[0x2c0:0x2c0 + len(image_setup)] = image_setup
    if mode == 'non-image-section':
        data[0x2c7] = 0
    rewrite = bytearray.fromhex(
        '48 8b 4b 08 48 8d 94 24 20 03 00 00 '
        '48 89 bc 24 a0 03 00 00 ff 15 00 00 00 00')
    if mode == 'wrong-context-register':
        rewrite[16] = 0xa8
    dest = 'GetThreadContext' if mode == 'wrong-context-call' else 'SetThreadContext'
    struct.pack_into('<i', rewrite, 22, slots[dest] - (0x1140 + len(rewrite)))
    data[0x340:0x340 + len(rewrite)] = rewrite
    strings = {
        'positive': b'ShellExecuteA\0MicrosoftEdge\0',
        'autorun-directive': b'ShellExecute=autorun.exe\0MicrosoftEdgeUpdateTask_\0',
    }.get(mode, b'')
    data[0xc00:0xc00 + len(strings)] = strings
    return data


if __name__ == '__main__':
    for mode in ['positive', 'wrong-disposition-buffer', 'wrong-disposition-call',
                 'keep-file', 'non-image-section', 'wrong-image-call', 'wrong-context-register',
                 'wrong-context-call', 'autorun-directive']:
        (ROOT / (mode + '.exe')).write_bytes(image(mode))
