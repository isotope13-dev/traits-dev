#!/usr/bin/env python3
"""Static boundary checks. Never imports or executes submitted sample code.
Run with Python + pefile, pointing --samples at the original or relocated tree.
"""
import argparse, hashlib, json, os, pathlib, subprocess
import pefile
p=argparse.ArgumentParser();p.add_argument('--samples',default='/var/tmp/hopper-triage/good');p.add_argument('--work',default='/tmp/hopper-good-boundaries-20261023');p.add_argument('--cleave',default='../cleave/target/release/cleave');a=p.parse_args()
root=pathlib.Path.cwd();work=pathlib.Path(a.work);work.mkdir(parents=True,exist_ok=True)
base=pathlib.Path(a.samples); relocated=pathlib.Path('/tmp/triage/misplaced-good/hopper-good-evidence-20261023')
def sample(rel):
 f=base/rel
 return f if f.exists() else relocated/rel
cases=[]
def add(name,content,required=(),forbidden=(),max_high=None):
 f=work/name;f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes(content if isinstance(content,(bytes,bytearray)) else content.encode());cases.append(dict(path=str(f),sha256=hashlib.sha256(f.read_bytes()).hexdigest(),required=list(required),forbidden=list(forbidden),max_high=max_high))
source=sample('upload/setup.py').read_text()
add('dormant/setup.py',source,max_high=0)
add('called/setup.py',source+'\nfetch()\n',required=['micro-behaviors/communications/http/download/helper::module-invokes-download-process-helper','objectives/execution/payload/file-exec::setup-install-urlretrieve-exec','objectives/execution/payload/file-exec::download-execute-chain'])
add('renamed/setup.py',source.replace('fetch','retrieve_component')+'\nretrieve_component()\n',required=['micro-behaviors/communications/http/download/helper::module-invokes-download-process-helper','objectives/execution/payload/file-exec::setup-install-urlretrieve-exec','objectives/execution/payload/file-exec::download-execute-chain'])
add('unrelated/setup.py',source+'\ndef build():\n    subprocess.run(["cc", "build.c"])\nbuild()\n',max_high=0)
load='micro-behaviors/data/serialize/unsafe::module-scope-torch-load'
add('safe-load.py','import torch\nm = torch.load("weights.pt", weights_only=True)\n',forbidden=[load])
add('unsafe-load.py','import torch\nm = torch.load("weights.pt", weights_only=False)\n',required=[load])
add('mixed-load.py','import torch\ns = torch.load("safe.pt", weights_only=True)\nm = torch.load("unsafe.pt", weights_only=False)\n',required=[load])
add('ordinary-ui.js','const label = "The skill name cannot be changed: injection keys and scene bindings address it.";\n',max_high=0)
corpus='metadata/package/testing/corpus::javascript-labeled-injection-input-array'
add('labeled-inputs.js','const renamed = [["sql", "1 OR 1=1", "probe"], ["xss", "<img src=x onerror=alert(1)>", "probe"], ["xxe", "<!DOCTYPE x [<!ENTITY e SYSTEM \'file:///etc/passwd\'>]><x>&e;</x>", "probe"]];\n',required=[corpus],max_high=0)
add('single-entity.js','const x = "<!DOCTYPE x [<!ENTITY e SYSTEM \'file:///etc/passwd\'>]><x>&e;</x>";\n',forbidden=[corpus])
# Native controls are mutated only as bytes. No Windows code is run.
blob=sample('triage/R6 Launcher.exe').read_bytes();pe=pefile.PE(data=blob);sites=json.load(open(pathlib.Path(__file__).with_name('r6-decoded-strings.json')))
def off(va):return pe.get_offset_from_rva(int(va,16)-pe.OPTIONAL_HEADER.ImageBase)
def recode(items,keys=False):
 out=bytearray(blob)
 for site in sites:
  s,k,n=off(site['source']),off(site['key']),site['length'];old=blob[k:k+16];plain=bytes(blob[s+j]^old[j%16] for j in range(n))
  if site['text'] in items:plain=items[site['text']].encode().ljust(n,b'\x00')[:n]
  key=hashlib.sha256(site['key'].encode()).digest()[:16] if keys else old
  out[s:s+n]=bytes(plain[j]^key[j%16] for j in range(n));out[k:k+16]=key
 return out
hostile='objectives/command-and-control/channel/deaddrop/blockchain::concealed-blockchain-peruser-python-loader'
vm='objectives/anti-analysis/environment-detect/check::xor-virtual-cpu-model-with-hardware-queries'
add('renamed.exe',blob,required=[hostile,vm])
add('all-new-keys.exe',recode({},True),required=[hostile,vm])
qemu=next(s['text'] for s in sites if 'Broadwell' in s['text']);add('no-virtual-cpu.exe',recode({qemu:'Ordinary processor'}),forbidden=[hostile,vm])
rpc=next(s['text'] for s in sites if 'eth_call' in s['text']);add('no-blockchain-call.exe',recode({rpc:rpc.replace('eth_call','eth_read')}),required=[vm],forbidden=[hostile])
path=next(s['text'] for s in sites if s['text'].startswith('Microsoft\\Windows\\'));add('no-windows-camouflage.exe',recode({path:'Documents\\ApplicationData'}),required=[vm],forbidden=[hostile])
out=bytearray(blob)
for site in sites:
 start=off(site['at']);at=blob.find(bytes.fromhex('44 32 04 08'),start,start+60)
 assert at>=0,site
 out[at:at+4]=bytes.fromhex('44 8a 04 08') # mov, not xor: the decoder predicate must fail.
add('no-xor.exe',out,forbidden=[hostile,vm])
# RET + no data directories proves this specific fixture has no activation path.
b=sample('upload/resource-entry-signatures.exe').read_bytes();p0=pefile.PE(data=b);entry=p0.get_offset_from_rva(p0.OPTIONAL_HEADER.AddressOfEntryPoint)
add('return-only.exe',b,max_high=0)
b1=bytearray(b);b1[entry]=0x90
add('non-return-entry.exe',b1,required=['metadata/binary/section/header::pe-entry-in-resource-section'])
# A TLS directory prevents the return-only control exemption.
tls=p0.OPTIONAL_HEADER.DATA_DIRECTORY[9];b2=bytearray(b);at=tls.get_file_offset();b2[at:at+8]=(p0.OPTIONAL_HEADER.AddressOfEntryPoint+32).to_bytes(4,'little')+(24).to_bytes(4,'little')
add('tls-before-entry.exe',b2,required=['metadata/binary/section/header::pe-entry-in-resource-section'])
env=os.environ.copy();env['XDG_CACHE_HOME']=str(work/'cache')
cmd=[str(pathlib.Path(a.cleave).resolve()),'--no-update-check','--traits-dir',str(root),'analyze','--format','json']+[c['path'] for c in cases]
r=subprocess.run(cmd,env=env,text=True,capture_output=True);(work/'stderr.log').write_text(r.stderr);assert r.returncode==0,r.stderr
reports=[]; remaining=r.stdout.lstrip(); decoder=json.JSONDecoder()
while remaining:
 report,end=decoder.raw_decode(remaining);reports.append(report);remaining=remaining[end:].lstrip()
by={f['path']:f for report in reports for f in report['files']};fail=[]
for c in cases:
 f=by[c['path']];ts={t['id']:t for t in f.get('traits',[])};high=[t for t in ts.values() if t.get('crit',0)>=4]
 c['high_findings']=[{'id':t['id'],'crit':t['crit'],'desc':t['desc']} for t in high]
 c['failures']=[f'missing {i}' for i in c['required'] if i not in ts]+[f'unexpected {i}' for i in c['forbidden'] if i in ts]
 if c['max_high'] is not None and len(high)>c['max_high']:c['failures'].append(f'{len(high)} high findings exceeds {c["max_high"]}')
 if c['failures']:fail.append(c)
result={'command':cmd,'cases':cases,'passed':len(cases)-len(fail),'failed':len(fail)};(work/'results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'passed':result['passed'],'failed':result['failed'],'failures':fail},indent=2));raise SystemExit(bool(fail))
