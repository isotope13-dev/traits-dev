"""Inert PE fixtures for listener port-seizure and elevated Run persistence.

Each fixture is a minimal PE with a real import directory plus diagnostic
strings; none of them execute anything (single `ret` entry point).
"""
from pathlib import Path
import struct

ROOT = Path(__file__).parent


def build_pe(imports, payload):
    """Minimal PE32+ with .text (ret), .rdata (payload) and .idata (imports).

    imports: list of (dll_name, [func, ...]). RVAs equal file offsets.
    """
    # --- lay out .idata first to learn its size ---
    idata = bytearray()
    n_dll = len(imports)
    dir_off = 0  # offset of import directory array inside .idata
    desc_size = 20 * (n_dll + 1)
    pos = desc_size
    ilts = []
    for dll, funcs in imports:
        ilts.append(pos)
        pos += 4 * (len(funcs) + 1)
    iats = []
    for dll, funcs in imports:
        iats.append(pos)
        pos += 4 * (len(funcs) + 1)
    name_rvas = []
    for dll, funcs in imports:
        name_rvas.append(pos)
        pos += len(dll) + 1
    hn_rvas = []
    for dll, funcs in imports:
        cur = []
        for f in funcs:
            if pos % 2:
                pos += 1
            cur.append(pos)
            pos += 2 + len(f) + 1
        hn_rvas.append(cur)
    # --- headers ---
    HDR = 512
    text_raw, rdata_raw = 1024, 1536
    idata_raw = 2048
    total = idata_raw + ((pos + 511) // 512) * 512
    b = bytearray(total)
    b[:2] = b'MZ'
    struct.pack_into('<I', b, 60, 128)
    b[128:132] = b'PE\0\0'
    struct.pack_into('<HHIIIHH', b, 132, 0x8664, 3, 0, 0, 0, 240, 0x22)
    o = 152
    struct.pack_into('<H', b, o, 0x20b)
    struct.pack_into('<I', b, o + 16, 4096)
    struct.pack_into('<Q', b, o + 24, 0x140000000)
    struct.pack_into('<II', b, o + 32, 4096, 512)
    struct.pack_into('<II', b, o + 56, 0x10000, 1024)
    struct.pack_into('<H', b, o + 68, 3)
    struct.pack_into('<I', b, o + 108, 16)
    idata_rva = idata_raw
    struct.pack_into('<II', b, o + 112 + 8, idata_rva, desc_size)
    for j, (name, rva, size, flags) in enumerate([
        (b'.text', 4096, 512, 0x60000020),
        (b'.rdata', 8192, 512, 0x40000040),
        (b'.idata', idata_rva, total - idata_raw, 0x40000040),
    ]):
        q = o + 240 + j * 40
        raw = [text_raw, rdata_raw, idata_raw][j]
        b[q:q + len(name)] = name
        struct.pack_into('<IIII', b, q + 8, size, rva, size, raw)
        struct.pack_into('<I', b, q + 36, flags)
    b[text_raw] = 0xc3
    b[rdata_raw:rdata_raw + len(payload)] = payload
    # --- import directory ---
    base = idata_raw
    for k, (dll, funcs) in enumerate(imports):
        q = base + k * 20
        struct.pack_into('<IIIII', b, q, base + ilts[k], 0, 0,
                         base + name_rvas[k], base + iats[k])
    for k, (dll, funcs) in enumerate(imports):
        for n, f in enumerate(funcs):
            struct.pack_into('<I', b, base + ilts[k] + 4 * n,
                             base + hn_rvas[k][n])
            struct.pack_into('<I', b, base + iats[k] + 4 * n,
                             base + hn_rvas[k][n])
        b[base + name_rvas[k]:base + name_rvas[k] + len(dll)] = dll.encode()
        for n, f in enumerate(funcs):
            h = base + hn_rvas[k][n]
            struct.pack_into('<H', b, h, 0)
            b[h + 2:h + 2 + len(f)] = f.encode()
    return b


WILD = b'proxy: listening 0.0.0.0:%d\0'
KILL1 = b'proxy: port %d busy, killing owner (%d)\0'
KILL2 = b'proxy: killed pid %d holding port %d\0'
RUNKEY = b'Software\\Microsoft\\Windows\\CurrentVersion\\Run\0'
HKLM_OK = b'autostart: HKLM Run set -> %p\0'

FIXTURES = {
    'wildcard-port-kill.exe': (
        [('WS2_32.dll', ['bind', 'listen']),
         ('WS2_32.dll', ['accept', 'WSAStartup']),
         ('KERNEL32.dll', ['TerminateProcess'])],
        b'\0'.join([WILD, KILL1, KILL2])),
    'wildcard-listen-clean.exe': (
        [('WS2_32.dll', ['bind', 'listen']),
         ('WS2_32.dll', ['accept', 'WSAStartup'])],
        b'proxy: listening 0.0.0.0:%d\0bind failed: address in use, exiting\0'),
    'elevated-ownimage-run.exe': (
        [('KERNEL32.dll', ['GetModuleFileNameW', 'CreateFileW']),
         ('ADVAPI32.dll', ['RegSetValueExW', 'RegCreateKeyExW'])],
        b'\0'.join([RUNKEY, HKLM_OK, b'runas',
                     b'C:\\Tools\\helper.exe'])),
    'installer-run.exe': (
        [('ADVAPI32.dll', ['RegSetValueExW', 'RegCreateKeyExW'])],
        b'\0'.join([RUNKEY, b'C:\\Program Files\\Vendor\\app.exe'])),
}

if __name__ == '__main__':
    for name, (imports, payload) in FIXTURES.items():
        (ROOT / name).write_bytes(build_pe(imports, payload))
        print('wrote', name)
