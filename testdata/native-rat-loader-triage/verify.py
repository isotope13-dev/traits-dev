"""Inert PE controls for section boundaries and incomplete marker clusters.
Run: python3 testdata/native-rat-loader-triage/verify.py <scratch-directory>
The generated PEs contain no executable malware and are never executed.
"""
import json
import os
from pathlib import Path
import struct
import subprocess
import sys


def pe_image(code=b'\xc3', data=b'', data_section='.rdata', overlay=b''):
    header = bytearray(0x200)
    header[:2] = b'MZ'
    struct.pack_into('<I', header, 0x3c, 0x80)
    header[0x80:0x84] = b'PE\0\0'
    struct.pack_into('<HHIIIHH', header, 0x84, 0x8664, 2, 0, 0, 0, 0xf0, 0x22)
    opt = 0x98
    struct.pack_into('<H', header, opt, 0x20b)
    struct.pack_into('<I', header, opt+16, 0x1000)
    struct.pack_into('<Q', header, opt+24, 0x140000000)
    struct.pack_into('<II', header, opt+32, 0x1000, 0x200)
    struct.pack_into('<II', header, opt+56, 0x3000, 0x200)
    struct.pack_into('<H', header, opt+68, 3)
    struct.pack_into('<I', header, opt+108, 16)
    for off, name, blob, va, raw, flags in [
        (0x188, '.text', code, 0x1000, 0x200, 0x60000020),
        (0x1b0, data_section, data, 0x2000, 0x400, 0x40000040),
    ]:
        struct.pack_into('<8sIIIIIIHHI', header, off, name.encode(), max(len(blob),1),
                         va, 0x200, raw, 0, 0, 0, 0, flags)
    assert len(code) <= 0x200 and len(data) <= 0x200
    return bytes(header)+code.ljust(0x200,b'\0')+data.ljust(0x200,b'\0')+overlay


def main():
    dest = Path(sys.argv[1])
    dest.mkdir(parents=True, exist_ok=True)
    restore = bytes.fromhex('41 C6 44 07 01 45 41 C6 47 01 5A 41 C6 04 07 50')
    names = b'mscoree.dll\0CorExitProcess\0IsDebuggerPresent\0VirtualProtect\0LoadLibraryA\0WriteFile\0'
    gh0st = (b'SAM\\SAM\\Domains\\Account\\Users\\Names\\%s\0'
             b'GetMP privilege::debug sekurlsa::logonpasswords exit\0'
             b'Http/1.1 403 Forbidden\r\n\r\n<H1>403 Forbidden</H1>\0')
    cases = {
        'ordinary-runtime.exe': pe_image(data=names),
        'partial-hide-log.exe': pe_image(data=b'QAssist!AddHiddenFile\0QAssist!Start\0'),
        'shared-config.exe': pe_image(data='Hid_State\0Hid_StealthMode\0'.encode('utf-16le')),
        'hash-substring.exe': pe_image(data=b'ciphertext_a1dJb2e9_without_identifier_boundaries\0'),
        'signature-data.exe': pe_image(data=restore),
        'gh0st-overlay.exe': pe_image(overlay=gh0st),
        'gh0st-loaded-section.exe': pe_image(data=gh0st),
        'gh0st-partial-profile.exe': pe_image(data=gh0st.split(b'Http/')[0]),
    }
    family = 'well-known/malware/rat/gh0st::gh0st-credential-command-profile'
    for name, contents in cases.items():
        p=dest/name
        p.write_bytes(contents)
        result=subprocess.run(['cleave','--format','json',str(p)],check=True,
                              stdout=subprocess.PIPE, env={**os.environ,'CLEAVE_VALIDATE':'0'})
        report=json.loads(result.stdout)
        traits=report['files'][0]['traits']
        ids={x['id'] for x in traits}
        hostile={x['id'] for x in traits if x['crit']==5}
        if name=='gh0st-loaded-section.exe':
            assert family in hostile, (name,hostile)
        else:
            assert not hostile, (name,hostile)
            assert family not in ids, (name,ids)
        if name=='hash-substring.exe':
            assert 'micro-behaviors/os/api-resolution/hash-based::djb2-hash' not in ids
        if name=='shared-config.exe':
            assert 'well-known/tool/offensive/hidden-rootkit::hid-stealthmode-config-marker' in ids
            assert not any('coolclient' in x.lower() for x in ids)
        print('PASS',name)


if __name__=='__main__':
    main()
