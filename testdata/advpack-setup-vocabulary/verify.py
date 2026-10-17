"""Advpack setup engine carries INF section vocabulary.

Run: python3 testdata/advpack-setup-vocabulary/verify.py <scratch-directory>

`inf-presetup-commands-section` matches the RunPreSetupCommands /
PreSetupCommandsSection INF vocabulary. The advpack setup engine embeds that
vocabulary because it implements INF installation, so binaries exporting the
advpack setup entry points are excluded from the atomic. A binary that
mentions the vocabulary without exporting the engine surface still matches.
"""
import json
import os
import struct
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TARGET = ('objectives/privilege-escalation/elevation-control/uac-bypass/inf::'
          'inf-presetup-commands-section')

BAT_POSITIVE = """\
[PreSetupCommandsSection]
RunPreSetupCommands=payload.exe /setup
"""


def align(n, a):
    return (n + a - 1) // a * a


def build_pe(*, exports=(), strings=()):
    """Minimal PE32 with .text strings and an export table (or none)."""
    text_blob = b'\x33\xc0\xc3' + b'\x00' * 29
    for s in strings:
        text_blob += s.encode('ascii') + b'\x00'
    while len(text_blob) % 4:
        text_blob += b'\x00'

    size_headers, file_align, sec_align = 0x200, 0x200, 0x1000
    rva_text, rva_edata = 0x1000, 0x2000
    off_text, off_edata = size_headers, size_headers + 0x200

    edata = bytearray(0x200)
    if exports:
        nexp = len(exports)
        func_tab, name_tab, ord_tab = 40, 40 + nexp * 4, 40 + nexp * 8
        str_off = ord_tab + nexp * 2
        struct.pack_into('<IIHHIIIIIII', edata, 0,
                         0, 0, 0, 0, 0, 1, nexp, nexp,
                         rva_edata + func_tab, rva_edata + name_tab,
                         rva_edata + ord_tab)
        for k, e in enumerate(exports):
            struct.pack_into('<I', edata, func_tab + k * 4, rva_text)
            struct.pack_into('<I', edata, name_tab + k * 4, rva_edata + str_off)
            struct.pack_into('<H', edata, ord_tab + k * 2, k)
            edata[str_off:str_off + len(e)] = e.encode('ascii')
            str_off += len(e) + 1

    dos = bytearray(0x80)
    dos[0:2] = b'MZ'
    struct.pack_into('<I', dos, 0x3c, 0x80)
    pe = bytearray(bytes(dos) + b'PE\x00\x00')
    pe += struct.pack('<HHIIIHH', 0x14c, 2 if exports else 1, 0, 0, 0,
                      224, 0x2102)
    opt = bytearray(224)
    struct.pack_into('<HBB', opt, 0, 0x10b, 0, 0)
    struct.pack_into('<III', opt, 4, 0x200, 0x200, 0)
    struct.pack_into('<III', opt, 16, rva_text, rva_text, rva_text)
    struct.pack_into('<III', opt, 28, 0x400000, sec_align, file_align)
    struct.pack_into('<HHHHHH', opt, 40, 4, 0, 0, 0, 0, 0)
    struct.pack_into('<III', opt, 52, 0, 0x4000, size_headers)
    struct.pack_into('<I', opt, 64, 0)
    struct.pack_into('<HH', opt, 68, 2, 0)
    struct.pack_into('<IIII', opt, 72, 0x100000, 0x1000, 0x100000, 0x1000)
    struct.pack_into('<II', opt, 88, 0, 16)
    if exports:
        struct.pack_into('<II', opt, 96, rva_edata, 0x200)
    pe += bytes(opt)
    secs = [('.text', rva_text, len(text_blob), off_text, 0x60000020)]
    if exports:
        secs.append(('.edata', rva_edata, 0x200, off_edata, 0x40000040))
    for nm, vr, vs, fo, ch in secs:
        pe += nm.encode('ascii').ljust(8, b'\x00')
        pe += struct.pack('<IIIIIIHHI', vs, vr, align(vs, file_align), fo,
                          0, 0, 0, 0, ch)
    pe += b'\x00' * (size_headers - len(pe))
    pe += text_blob + b'\x00' * (0x200 - len(text_blob))
    if exports:
        pe += bytes(edata)
    return bytes(pe)


def scan(path):
    result = subprocess.run(
        [os.environ.get('CLEAVE', 'cleave'), '--traits-dir', str(ROOT),
         '--format', 'json', str(path)],
        env=dict(os.environ, CLEAVE_VALIDATE='0'),
        text=True, capture_output=True, check=True)
    report = json.loads(result.stdout)
    return {t['id'] for entry in report['files'] for t in entry['traits']}


def main():
    dest = Path(sys.argv[1])
    dest.mkdir(parents=True, exist_ok=True)

    bat = dest / 'inf-vocabulary-positive.bat'
    bat.write_text(BAT_POSITIVE)
    assert TARGET in scan(bat), 'positive .bat must match the atomic'
    print('PASS inf-vocabulary-positive.bat', flush=True)

    engine = dest / 'advpack-engine-negative.dll'
    engine.write_bytes(build_pe(
        exports=['LaunchINFSectionEx', 'RunSetupCommand'],
        strings=['RunPreSetupCommands', 'DefaultInstall']))
    assert TARGET not in scan(engine), 'setup engine must be excluded'
    print('PASS advpack-engine-negative.dll', flush=True)

    plain = dest / 'vocabulary-no-exports-positive.dll'
    plain.write_bytes(build_pe(strings=['RunPreSetupCommands']))
    assert TARGET in scan(plain), 'vocabulary without engine stays suspicious'
    print('PASS vocabulary-no-exports-positive.dll', flush=True)


if __name__ == '__main__':
    main()
