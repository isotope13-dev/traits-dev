"""Small PE controls for opcode placement and filename-versus-execution."""
from pathlib import Path
import struct

root = Path(__file__).resolve().parent

def pe(name, text, *, rdtscp=0, data_rdtscp=False, launch=False, catalog=False):
    image = bytearray(0x600)
    image[:2] = b'MZ'
    struct.pack_into('<I', image, 0x3c, 0x80)
    image[0x80:0x84] = b'PE\0\0'
    struct.pack_into('<HHIIIHH', image, 0x84, 0x8664, 2, 0, 0, 0, 240, 0x22)
    o = 0x98
    struct.pack_into('<H', image, o, 0x20b)
    struct.pack_into('<III', image, o+4, 0x200, 0x200, 0)
    struct.pack_into('<IIQ', image, o+16, 0x1000, 0x1000, 0x140000000)
    struct.pack_into('<II', image, o+32, 0x1000, 0x200)
    struct.pack_into('<HH', image, o+40, 6, 0)
    struct.pack_into('<HH', image, o+48, 6, 0)
    struct.pack_into('<II', image, o+56, 0x3000, 0x200)
    struct.pack_into('<HH', image, o+68, 3, 0x140)
    struct.pack_into('<QQQQII', image, o+72, 0x100000, 0x1000, 0x100000, 0x1000, 0, 16)
    for i, (section, address, offset, flags) in enumerate([
            (b'.text', 0x1000, 0x200, 0x60000020),
            (b'.idata', 0x2000, 0x400, 0xc0000040)]):
        struct.pack_into('<8sIIIIIIHHI', image, o+240+i*40,
                         section, 0x200, address, 0x200, offset, 0, 0, 0, 0, flags)
    code = b'\x0f\x01\xf9' * rdtscp + b'\xc3\0' + text
    assert len(code) < 0x200
    image[0x200:0x200+len(code)] = code
    if data_rdtscp:
        image[0x500:0x506] = b'\x0f\x01\xf9' * 2
    if launch:
        struct.pack_into('<II', image, o+112+8, 0x2000, 40)
        struct.pack_into('<IIIII', image, 0x400, 0x2060, 0, 0, 0x2040, 0x2080)
        image[0x440:0x44d] = b'KERNEL32.dll\0'
        struct.pack_into('<Q', image, 0x460, 0x20a0)
        struct.pack_into('<Q', image, 0x480, 0x20a0)
        image[0x4a0:0x4aa] = b'\0\0WinExec\0\0'
    if catalog:
        struct.pack_into('<II', image, o+112+9*8, 0x2100, 40)
        struct.pack_into('<QQQQII', image, 0x500, 0, 0, 0x140002140, 0x140002160, 0, 0)
        struct.pack_into('<QQQ', image, 0x560, 0x140001000, 0x140001003, 0)
        image += b'overlay\0' * 4096
    (root/name).write_bytes(image)

pe('native-opcodes.exe', b'', rdtscp=2)
pe('single-opcode.exe', b'', rdtscp=1)
pe('data-opcodes.exe', b'', data_rdtscp=True)
pe('setup-name-only.exe', b'C:\\downloads\\demo-setup.exe\0')
pe('download-launch.exe', b'DownloadURL\0RunWhenDone=\0C:\\downloads\\demo-setup.exe\0', launch=True)
pe('download-no-name.exe', b'DownloadURL\0RunWhenDone=\0', launch=True)
pe('analysis-catalog.exe', b'SbieDll\0M_CpuidHypervisor\0M_MacAddress\0M_SandboxProcesses\0M_RdtscTiming\0DEBUGGER DETECTED\0', rdtscp=2, catalog=True)
