"""Inert controls for PE parsing, CIL structure, and command-target binding.
Run with a scratch output directory; no generated executable is launched.
"""
import json
import os
from pathlib import Path
import runpy
import struct
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
pe_image = runpy.run_path(str(ROOT/'testdata/native-rat-loader-triage/verify.py'))['pe_image']
dest = Path(sys.argv[1])
dest.mkdir(parents=True, exist_ok=True)
cil = bytes.fromhex('28 01 00 00 0A 06 20 00 10 00 00 28 01 00 00 06 28 01 00 00 2B 6F 02 00 00 0A 0B 07 6F 03 00 00 0A')
data=bytearray(0x200)
struct.pack_into('<IIIII',data,0,0x2040,0,0,0x2080,0x2060)
struct.pack_into('<Q',data,0x40,0x20a0)
struct.pack_into('<Q',data,0x60,0x20a0)
data[0x80:0x8d]=b'KERNEL32.dll\0'
data[0xa0:0xae]=b'\0\0ExitProcess\0'
parser_image=bytearray(pe_image(code=bytes.fromhex('B8 4D 5A 00 00 C3'),data=data))
struct.pack_into('<II',parser_image,0x98+120,0x2000,40)

# A real, inert import table across three DLLs tests the relocated service
# profile without pretending those independent imports are a backdoor.
data=bytearray(0x200)
cursor=80
for index,(dll,names) in enumerate([
    ('ADVAPI32.dll',['CreateServiceA']),
    ('USER32.dll',['OpenInputDesktop','SetThreadDesktop']),
    ('WININET.dll',['InternetOpenUrlA']),
]):
    dll_offset=cursor
    encoded=dll.encode()+b'\0'
    data[cursor:cursor+len(encoded)]=encoded
    cursor=(cursor+len(encoded)+7)&~7
    ilt=cursor;cursor+=8*(len(names)+1)
    iat=cursor;cursor+=8*(len(names)+1)
    for j,name in enumerate(names):
        hint=cursor;encoded=b'\0\0'+name.encode()+b'\0'
        data[cursor:cursor+len(encoded)]=encoded;cursor=(cursor+len(encoded)+1)&~1
        struct.pack_into('<Q',data,ilt+j*8,0x2000+hint)
        struct.pack_into('<Q',data,iat+j*8,0x2000+hint)
    struct.pack_into('<IIIII',data,index*20,0x2000+ilt,0,0,0x2000+dll_offset,0x2000+iat)
service_image=bytearray(pe_image(data=data))
struct.pack_into('<II',service_image,0x98+120,0x2000,80)

cases = {
 'service-api-profile.exe': bytes(service_image),
 'pe-parser.exe': bytes(parser_image),
 'cil-sequence.exe': pe_image(code=cil),
 'cil-data-only.exe': pe_image(data=cil),
 'cil-no-virtual-call.exe': pe_image(code=cil.replace(b'\x6f', b'\x28', 1)),
 'unrelated-security-list.exe': pe_image(data=b'avp.exe\0taskkill /f /im taskmgr.exe\0'),
 'bound-security-kill.exe': pe_image(data=b'taskkill /f /im avp.exe\0'),
 'similar-name.exe': pe_image(data=b'taskkill /f /im avp.exe.backup\0'),
 'admin-tool-kills.exe': pe_image(data=b'taskkill /f /im taskmgr.exe\0taskkill /f /im regedit.exe\0taskkill /f /im mmc.exe\0'),
 'one-admin-tool.exe': pe_image(data=b'taskkill /f /im taskmgr.exe\0'),
}
for name,data in cases.items(): (dest/name).write_bytes(data)
result=subprocess.run([os.environ.get('CLEAVE','cleave'),'--traits-dir',str(ROOT),'--format','json',*[str(dest/n) for n in cases]],check=True,stdout=subprocess.PIPE)
decoder=json.JSONDecoder()
text=result.stdout.decode()
files=[]
while text.strip():
    item,end=decoder.raw_decode(text.lstrip())
    files.extend(item.get('files',[item]))
    text=text.lstrip()[end:]
report={'files':files}
rows={Path(f['path']).name:{t['id']:t['crit'] for t in f.get('traits',[])} for f in report['files'] if '!!' not in f['path']}
(dest/'results.json').write_text(json.dumps(rows,indent=2)+'\n')
parser='micro-behaviors/data/format/pe-parser::mz-immediate-with-few-imports'
sequence='metadata/binary/instruction::cil-sized-helper-to-virtual-call-sequence'
kill='objectives/impact/degrade/edr/targeting::edr-security-process-termination'
admin='objectives/impact/degrade/process::force-kill-administration-tool-cluster'
assert rows['service-api-profile.exe'].get('micro-behaviors/os/service/create::create-service-desktop-wininet-api-profile')==3
assert rows['pe-parser.exe'].get(parser)==3
assert rows['cil-sequence.exe'].get(sequence)==3
assert sequence not in rows['cil-data-only.exe']
assert sequence not in rows['cil-no-virtual-call.exe']
assert kill not in rows['unrelated-security-list.exe']
assert rows['bound-security-kill.exe'].get(kill)==4
assert kill not in rows['similar-name.exe']
assert rows['admin-tool-kills.exe'].get(admin)==4
assert admin not in rows['one-admin-tool.exe']
for name,traits in rows.items(): assert all(c<5 for c in traits.values()), (name,traits)
(dest/'results.json').write_text(json.dumps(rows,indent=2)+'\n')
print('PASS: parsing, CIL location/near miss, unrelated security list, bound kill, admin targets')
