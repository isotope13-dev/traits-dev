#!/usr/bin/env python3
"""Static boundary checks for stack-linked Go native entry handoffs.

No fixture or specimen is executed. The real-sample controls retain all four
instruction fragments while breaking the required stack-slot relationships.
"""
from pathlib import Path
import argparse,json,os,re,struct,subprocess,hashlib

ROOT=Path(__file__).resolve().parents[3]
LINK='micro-behaviors/data/arithmetic::go-field-base-sum-call-setup'
UNPACK='objectives/anti-static/pack/manual-map::go-arithmetic-pe-unpacker'
SUBST='objectives/evasion/process/loader::go-packed-pe-imagebase-substitution'
p=argparse.ArgumentParser();p.add_argument('--cleave',required=True);p.add_argument('--work',default='/tmp/hopper-combination-controls-20261023');p.add_argument('--inventory',default='/tmp/hopper-new-review-20261023/inventory.json');p.add_argument('--probe',default='/tmp/hopper-deep-review-20261023/spilled-handoff-probe.json');a=p.parse_args();work=Path(a.work);work.mkdir(parents=True,exist_ok=True);cases=[]

def image(code,data=b'',machine=0x8664):
    textlen=(max(len(code)+1,1)+511)&~511;datalen=(max(len(data),1)+511)&~511
    data_va=(0x1000+textlen+4095)&~4095;b=bytearray(512+textlen+datalen);b[:2]=b'MZ';struct.pack_into('<I',b,0x3c,0x80);b[0x80:0x84]=b'PE\0\0';struct.pack_into('<HHIIIHH',b,0x84,machine,2,0,0,0,240,0x22);opt=0x98;struct.pack_into('<H',b,opt,0x20b);struct.pack_into('<II',b,opt+16,0x1000,0x1000);struct.pack_into('<QII',b,opt+24,0x140000000,4096,512);struct.pack_into('<II',b,opt+56,(data_va+datalen+4095)&~4095,512);struct.pack_into('<H',b,opt+68,3);struct.pack_into('<I',b,opt+108,16)
    for k,(name,va,off,size,flags) in enumerate([(b'.text',0x1000,512,textlen,0x60000020),(b'.rdata',data_va,512+textlen,datalen,0x40000040)]):struct.pack_into('<8sIIIIIIHHI',b,opt+240+k*40,name,size,va,size,off,0,0,0,0,flags)
    b[512]=0xc3;b[513:513+len(code)]=code;b[512+textlen:512+textlen+len(data)]=data;return b

def parts(field=0x80,base=0x100,target=0x120,field_reload=None,target_reload=None,gaps=(24,96,48)):
    field_reload=field if field_reload is None else field_reload;target_reload=target if target_reload is None else target_reload
    f=bytes.fromhex('8B401048898424')+struct.pack('<I',field)
    add=bytes.fromhex('488B8C24')+struct.pack('<I',field_reload)+bytes.fromhex('488B9424')+struct.pack('<I',base)+bytes.fromhex('4801D1')
    save=bytes.fromhex('48898C24')+struct.pack('<I',target)
    call=bytes.fromhex('488B8424')+struct.pack('<I',target_reload)+bytes.fromhex('31DB31C94889CFE800000000')
    return f+b'\x90'*gaps[0]+add+b'\x90'*gaps[1]+save+b'\x90'*gaps[2]+call

def add(name,data,required=(),forbidden=()):
    path=work/(name+'.exe');path.write_bytes(data);cases.append({'name':name,'path':str(path),'sha256':hashlib.sha256(data).hexdigest(),'required':list(required),'forbidden':list(forbidden)})

code=parts();add('linked-spills',image(code),[LINK]);add('different-stack-layout',image(parts(field=0x228,base=0x300,target=0x488)),[LINK]);add('wrong-field-reload',image(parts(field_reload=0x88)),forbidden=[LINK]);add('wrong-call-reload',image(parts(target_reload=0x128)),forbidden=[LINK]);add('field-at-different-offset',image(code.replace(bytes.fromhex('8B4010'),bytes.fromhex('8B4014'))),forbidden=[LINK]);add('without-addition',image(code.replace(bytes.fromhex('4801D1'),bytes.fromhex('4831D1'))),forbidden=[LINK]);add('without-zero-argument-setup',image(code.replace(bytes.fromhex('31DB31C9'),bytes.fromhex('31D231C9'))),forbidden=[LINK]);add('fragments-in-data',image(b'',code),forbidden=[LINK]);add('different-machine',image(code,machine=0x14c),forbidden=[LINK]);add('field-gap-at-limit',image(parts(gaps=(501,96,48))),[LINK]);add('field-gap-too-large',image(parts(gaps=(502,96,48))),forbidden=[LINK]);add('sum-gap-too-large',image(parts(gaps=(24,494,48))),forbidden=[LINK]);add('target-gap-too-large',image(parts(gaps=(24,96,1017))),forbidden=[LINK])

inventory=json.load(open(a.inventory));probe=json.load(open(a.probe))
for sha in ['a58c639a1083','a5d4f63e443a']:
    sample=next(x for x in inventory if x['sha256'].startswith(sha));raw=Path(sample['path']).read_bytes();row=next(x for x in probe if x['sha12']==sha);add('renamed-'+sha,raw,[LINK,UNPACK,SUBST])
    for name,at in [('field-link',row['add_offset']+4),('target-link',row['call_offset']+4)]:
        modified=bytearray(raw);value=struct.unpack_from('<I',modified,at)[0];struct.pack_into('<I',modified,at,value+8);add('broken-'+name+'-'+sha,modified,forbidden=[LINK,UNPACK,SUBST])
    modified=bytearray(raw);start=row['add_offset'];assert modified[start+16:start+19]==bytes.fromhex('4801D1');modified[start+17]=0x31;add('no-addition-'+sha,modified,forbidden=[LINK,UNPACK,SUBST])
sample=next(x for x in inventory if x['sha256'].startswith('744f82adda79'));add('existing-register-variant',Path(sample['path']).read_bytes(),[UNPACK,SUBST])

env={**os.environ,'XDG_CACHE_HOME':'/tmp/hopper-new-review-20261023/cache'};cmd=[a.cleave,'--no-update-check','--traits-dir',str(ROOT),'--disable','radare2','analyze','--format','json']+[c['path'] for c in cases]
with (work/'scan.json').open('w') as stdout,(work/'scan.log').open('w') as stderr:rr=subprocess.run(cmd,stdout=stdout,stderr=stderr,env=env)
assert rr.returncode==0,rr.returncode
text=(work/'scan.json').read_text().lstrip();decoder=json.JSONDecoder();files={}
while text:
    report,n=decoder.raw_decode(text);text=text[n:].lstrip();files.update({f['path']:f for f in report['files']})
for case in cases:
    f=files[case['path']];traits={t['id']:t for t in f['traits']};case['failures']=['missing '+x for x in case['required'] if x not in traits]+['unexpected '+x for x in case['forbidden'] if x in traits];case['observed_relevant']=[{k:traits[x][k] for k in ['id','crit','desc']} for x in [LINK,UNPACK,SUBST] if x in traits]
result={'passed':sum(not c['failures'] for c in cases),'failed':sum(bool(c['failures']) for c in cases),'cases':cases};(work/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'passed':result['passed'],'failed':result['failed'],'failures':[x for x in cases if x['failures']]},indent=2));raise SystemExit(bool(result['failed']))
