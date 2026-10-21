"""Generate inert PE shapes and compare baseline/current trait coverage.

Usage: python3 check.py <baseline-traits> <output-directory>
No fixture is executed. Native code is RET or a static opcode observation.
"""
import concurrent.futures
import json
import os
from pathlib import Path
import random
import struct
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(sys.argv[2]).resolve()
OUT.mkdir(parents=True, exist_ok=True)
BASELINE = Path(sys.argv[1]).resolve()
OLD = 'objectives/persistence/system/service/install::service-install-dispatch-chain'
NEW = 'micro-behaviors/os/service/control::service-create-dispatch-api-profile'
DEC = 'objectives/anti-static/obfuscation/payload/section/layout::x86-unrolled-dword-decoder-in-reloc'
DIV = 'objectives/evasion/hijack-execution-flow/entrypoint::reloc-decoder-entry-diversion'
ENTRY = 'metadata/binary/section/header::entry-call-to-reloc-register-save-stub'
SHORT = 'objectives/evasion/hijack-execution-flow/shortcut::script-host-shortcut-proxy-hijack'
LUA = 'objectives/command-and-control/dropper/staging/runtime::embedded-lua-service-carrier'


def pe(payload=b'', imports=(), reloc=None, divert=False):
    # PE32, .text RET, .rdata with import descriptors and analyst-controlled
    # observations. All offsets are constructed, never copied from a sample.
    r = bytearray(40)
    def put(data):
        off = len(r)
        r.extend(data)
        return 0x2000 + off
    if imports:
        dll = put(b'ADVAPI32.dll\0')
        names = [put(b'\0\0' + s.encode() + b'\0') for s in imports]
        ilt = put(b''.join(struct.pack('<I', n) for n in names) + b'\0'*4)
        iat = put(b''.join(struct.pack('<I', n) for n in names) + b'\0'*4)
        struct.pack_into('<IIIII', r, 0, ilt, 0, 0, dll, iat)
    put(b'\0' + payload)
    r.extend(b'\0' * ((-len(r)) % 512))
    sections = [(b'.text', 0x1000, 1024, 512, 0x60000020),
                (b'.rdata', 0x2000, 1536, len(r), 0x40000040)]
    if reloc is not None:
        sections.append((b'.reloc', 0x10000, 1536+len(r), len(reloc), 0xe2000040))
    b = bytearray(1536 + len(r) + (len(reloc) if reloc is not None else 0))
    b[:2] = b'MZ'; struct.pack_into('<I', b, 0x3c, 128)
    b[128:132] = b'PE\0\0'
    struct.pack_into('<HHIIIHH', b, 132, 0x14c, len(sections), 1700000000, 0, 0, 224, 0x102)
    o = 152
    struct.pack_into('<H', b, o, 0x10b)
    struct.pack_into('<I', b, o+16, 0x1000)
    struct.pack_into('<I', b, o+28, 0x400000)
    struct.pack_into('<II', b, o+32, 4096, 512)
    struct.pack_into('<II', b, o+56, 0x30000, 1024)
    struct.pack_into('<H', b, o+68, 3)
    struct.pack_into('<I', b, o+92, 16)
    if imports:struct.pack_into('<II', b, o+104, 0x2000, 40)
    for j, (name, rva, pa, size, flags) in enumerate(sections):
        q = o+224+j*40;b[q:q+len(name)] = name
        struct.pack_into('<IIII', b, q+8, size, rva, size, pa)
        struct.pack_into('<I', b, q+36, flags)
    b[1024] = 0xc3
    if divert:b[1024:1029] = b'\xe8'+struct.pack('<i', 0x10000+0x100-0x1000-5)
    b[1536:1536+len(r)] = r
    if reloc is not None:b[1536+len(r):] = reloc
    return b


apis = ['OpenSCManagerW', 'CreateServiceW', 'StartServiceCtrlDispatcherW',
        'RegisterServiceCtrlHandlerExW', 'SetServiceStatus']
service_path = b'SYSTEM\\CurrentControlSet\\Services\\%s\0'
lua = b'\x1bLua\0' + b''.join(prefix+b' lua_open\0'+prefix+b' install_implant\0'
                               for prefix in [b'first',b'second',b'third'])
cases = []
for name, extra, imports, yes, no in [
    ('service-administrator', service_path, apis, [NEW], [LUA]),
    ('lua-implant-service', service_path+lua, apis, [NEW,LUA], []),
    ('service-no-configuration', b'', apis, [], [NEW,LUA]),
    ('service-no-create', service_path, [s for s in apis if s!='CreateServiceW'], [], [NEW,LUA]),
]:
    p=OUT/(name+'.exe');p.write_bytes(pe(extra, imports));cases.append((p,yes,no))
# Original decoder, a reordered EAX/XOR/SUB form, and a byte-close non-decoder.
original=bytes.fromhex('50 51 52 53 55 56 57 E8 00 00 00 00 5B 81 EB 11 22 33 44 BF 00 00 00 00 53 81 83 44 33 22 11 78 56 34 12 81 B3 11 22 33 44 12 34 56 78 F7 93')
variant=bytearray(original);variant[19]=0xb8;variant[26]=0xb3;variant[36]=0xab;variant[-2:]=b'\x81\xb3'
near=bytearray(variant);near[24]=0x90
for name, code, expected in [('decoder-original',original,True),('decoder-reordered',variant,True),('decoder-near-miss',near,False)]:
    r=bytearray(random.Random(42).randbytes(65536))
    r[256:256+len(code)]=code
    p=OUT/(name+'.exe');p.write_bytes(pe(reloc=r,divert=True));cases.append((p,[ENTRY]+([DEC] if expected else []),[DIV]+([] if expected else [DEC])))
# The diversion must resolve to the save stub, not merely another location in
# the same section. This catches RVA-vs-file-offset and rel32 errors.
b=bytearray((OUT/'decoder-reordered.exe').read_bytes());struct.pack_into('<i',b,1025,0x10000+0x104-0x1000-5)
p=OUT/'entry-unrelated-target.exe';p.write_bytes(b);cases.append((p,[DEC],[ENTRY,DIV]))
p=OUT/'shortcut-proxy.vbs';p.write_text('''Set sh = CreateObject("WScript.Shell")
Set link = sh.CreateShortcut("C:\\User Pinned\\TaskBar\\Example.lnk")
link.TargetPath = "wscript.exe"
link.Arguments = WScript.ScriptFullName
link.Save
''');cases.append((p,[SHORT,'micro-behaviors/fs/path/app-data::taskbar-pinned-shortcut-path'],[]))
p=OUT/'taskbar-reference.c';p.write_text('const char *p = "User Pinned\\\\TaskBar";\n');cases.append((p,[],[SHORT]))
p=OUT/'cache-read.js';p.write_text('const fs = require("fs");\nconst cache = "Service Worker/ScriptCache";\nfs.readFileSync(cache);\n')
cases.append((p,['micro-behaviors/fs/path/cache::chromium-profile-script-cache-path',
                 'micro-behaviors/fs/read/file/target::node-file-read-near-resource-path'],[]))
p=OUT/'cache-path-near-miss.js';p.write_text('const path = "Service Worker/ScriptFiles";\n')
cases.append((p,[],['micro-behaviors/fs/path/cache::chromium-profile-script-cache-path']))
# Existing controls outside this batch exercise retained hostile service and
# registry-stager behavior and ordinary shortcut/service near misses.
for rel in ['testdata/hostile/renamed-miner-service-install.ps1',
            'testdata/hostile/registry-stager-stubs/service-install.go',
            'testdata/stranded-registry-relay-review/service-only.c',
            'testdata/gauntlet-missed-controls/shortcut-editor.js']:
    cases.append((ROOT/rel,[],[]))


def scan(case, tree):
    p,yes,no=case
    result=subprocess.run(['cleave','--traits-dir',str(tree),'--format','json',str(p)],capture_output=True,text=True,
                          env={**os.environ,'CLEAVE_VALIDATE':'0','CLEAVE_SKIP_CACHE':'1'})
    assert result.returncode==0,(p,result.returncode,result.stderr[-3000:])
    obj=json.loads(result.stdout);raw=obj.get('raw',obj)
    label = 'before' if tree == BASELINE else 'after'
    (OUT/(p.name+'.'+label+'.json')).write_text(result.stdout)
    ids={t['id']:t['crit'] for f in raw.get('files',[]) for t in f.get('traits',[])}
    return ids


def compare(case):
    old=scan(case,BASELINE);new=scan(case,ROOT);p,yes,no=case
    assert set(yes)<=new.keys(),(p,'missing',set(yes)-new.keys())
    assert not set(no)&new.keys(),(p,'unexpected',set(no)&new.keys())
    if OLD in old:assert NEW in new,(p,'lost service capability')
    if DEC in old:assert DEC in new,(p,'lost decoder variant')
    old_attacks={k:v for k,v in old.items() if v>=4 and k!=OLD}
    assert old_attacks.keys()<=new.keys(),(p,'lost attacks',old_attacks.keys()-new.keys())
    for k,v in old_attacks.items():assert new[k]>=v,(p,'lowered attack',k)
    return {'case':p.name,'required':yes,'absent':no,'before_attack_traits':old_attacks,
            'after_attack_traits':{k:v for k,v in new.items() if v>=4},'lost':sorted(old.keys()-new.keys()),'gained':sorted(new.keys()-old.keys())}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:results=list(pool.map(compare,cases))
(OUT/'results.json').write_text(json.dumps(results,indent=2)+'\n')
print(f'{len(results)} baseline/current comparisons passed; {OUT}/results.json')
