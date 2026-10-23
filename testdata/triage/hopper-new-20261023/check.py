"""Synthetic matcher boundaries; never imports or executes specimen code."""
from pathlib import Path
import argparse,json,subprocess,os
p=argparse.ArgumentParser();p.add_argument('--scratch',type=Path,default=Path('/tmp/hopper-new-boundaries'));p.add_argument('--atomscan',type=Path);args=p.parse_args()
root=Path(__file__).resolve().parents[3];scratch=args.scratch;scratch.mkdir(parents=True,exist_ok=True);cases=scratch/'inputs';cases.mkdir(exist_ok=True);expected={}
def put(name,source,trait,want):
 (cases/name).write_text(source);expected[name]=(trait,want)
prefix='objectives/command-and-control/backdoor/tasking/json-http::'
selectors=scratch/'selector-inputs';selectors.mkdir(exist_ok=True)
selector_names=set()
for branch in ['shell','upload','download']:
 trait=prefix+'python-'+branch+'-command-selector'
 base=f'def dispatch(message):\n    chosen = message["command"]\n    if chosen == "{branch}":\n        return None\n'
 variants={
  'alias':(base,True),
  'renamed':(base.replace('chosen','selected'),True),
  'elif':(base.replace(f'if chosen == "{branch}":',f'if chosen == "ignored":\n        pass\n    elif chosen == "{branch}":'),True),
  'different-var':(base.replace('if chosen','if other'),False),
  'different-field':(base.replace('["command"]','["description"]'),False),
  'quoted':(repr(base)+'\n',False),
  'comment':('\n'.join('# '+v for v in base.splitlines()),False),
 }
 for variant,(source,want) in variants.items():
  name=branch+'-'+variant+'.py';(selectors/name).write_text(source)
  expected[name]=(trait,want);selector_names.add(name)
post='micro-behaviors/communications/http/request/json::python-post-json-method'
put('post-json.py','session.post(url, json={"result": "ok"})\n',post,True)
put('post-other.py','session.post(url, data={"result": "ok"})\n',post,False)
put('post-quoted.py','"session.post(url, json=payload)"\n',post,False)
tele='micro-behaviors/os/telemetry/logging/lifecycle::python-import-environment-event'
beacon='''import sys
try:
    if is_telemetry_enabled():
        record_event("module_init", {"python_version": sys.version})
except Exception:
    pass
'''
put('import-event.py',beacon,tele,True)
put('function-event.py','def later():\n'+''.join('    '+v+'\n' for v in beacon.splitlines()),tele,False)
put('import-event-quoted.py',repr(beacon)+'\n',tele,False)
put('other-event.py',beacon.replace('module_init','click'),tele,False)
# All code below is inert test text. No FFI or network function is called.
base='''const https=require('https'); const crypto=require('crypto');
function parse(buf,p,o){
 if(buf.readUInt16LE(0)!==23117)throw Error();
 if(buf.readUInt32LE(p)!==17744)throw Error();
 return {entryPoint:buf.readUInt32LE(o+16),imageBase:buf.readBigUInt64LE(o+24)};
}
class Mapper {
 erase(){const n=this.sizeOfHeaders; const z=new Uint8Array(n); new Uint8Array(ffi.view(ptr,n)).set(z);}
}
ffi.proto('int __stdcall Entry(void *base, uint32 reason, void *reserved)');
crypto.createDecipheriv('aes-256-cbc', key, iv);
bytes.set([76,139,209]); bytes.set([255,37,0,0,0,0]);
'''
mapper='objectives/anti-static/obfuscation/payload/memory::node-ffi-pe-header-overwrite-loader'
http='objectives/command-and-control/dropper/image-map::node-encrypted-http-pe-stager'
syscall='objectives/evasion/anti-av/syscall::node-pe-stager-indirect-syscall-builder'
put('mapper.js',base,mapper,True)
put('mapper-renamed.js',base.replace('buf','buffer').replace('const n=','const length=').replace('Array(n)','Array(length)').replace('ptr,n','ptr,length'),mapper,True)
put('mapper-no-write.js',base.replace('.set(z)','.slice(z)'),mapper,False)
put('mapper-wrong-buffer.js',base.replace('.set(z)','.set(other)'),mapper,False)
put('mapper-wrong-size.js',base.replace('ffi.view(ptr,n)','ffi.view(ptr,other)'),mapper,False)
put('mapper-no-prototype.js',base.replace('ffi.proto','ffi.example'),mapper,False)
put('mapper-comment.js','/*\n'+base+'\n*/',mapper,False)
put('encrypted-stager.js',base,http,True)
put('unencrypted-mapper.js',base.replace('createDecipheriv','createHash'),http,False)
put('indirect-stub.js',base,syscall,True)
put('indirect-hex.js',base.replace('[76,139,209]','[0x4c,0x8b,0xd1]').replace('[255,37,0,0,0,0]','[0xff,0x25,0x0,0x0,0x0,0x0]'),syscall,True)
put('no-indirect-stub.js',base.replace('[255,37,0,0,0,0]','[144,144,144,144,144,144]'),syscall,False)
put('opcode-only.js','bytes.set([76,139,209]);bytes.set([255,37,0,0,0,0]);',syscall,False)
cmd=[str(args.atomscan or root/'../scan/target/release/atomscan'),'--no-update','--mode','slow','--format','json','path',str(cases)]
r=subprocess.run(cmd,cwd=root,env=dict(os.environ,CLEAVE_TRAITS_DIR=str(root)),capture_output=True,text=True);(scratch/'boundaries.jsonl').write_text(r.stdout);(scratch/'boundaries.log').write_text(r.stderr);assert r.returncode in (0,1,2),r.stderr[-2000:]
records={}
for line in r.stdout.splitlines():
 for f in json.loads(line)['raw']['files']:records[Path(f['path']).name]={t['id']:t['crit'] for t in f.get('traits',[])}
# Production output hides component-only matches. Expose only these three
# unchanged queries at notable criticality in an isolated temporary rule tree.
# Full-production composites are separately verified on both supplied agents.
registration=(root/'objectives/command-and-control/backdoor/tasking/json-http/registration.yaml').read_text()
block=registration[registration.index('  - id: python-shell-command-selector'):registration.index('\ncomposite_rules:')]
probe=scratch/'selector-rules';target=probe/'objectives/command-and-control/backdoor/tasking/json-http/registration.yaml';target.parent.mkdir(parents=True,exist_ok=True)
target.write_text('defaults:\n  platforms: [unix, windows]\n  for: [python]\ntraits:\n'+block.replace('crit: component','crit: notable'))
cleave=root/'../cleave/target/release/cleave'
r=subprocess.run([str(cleave),'--traits-dir',str(probe),'--format','json','analyze',str(selectors)],cwd=root,capture_output=True,text=True)
(scratch/'selectors.json').write_text(r.stdout);(scratch/'selectors.log').write_text(r.stderr);assert r.returncode==0,r.stderr[-2000:]
remaining=r.stdout.strip();decoder=json.JSONDecoder()
while remaining:
 obj,end=decoder.raw_decode(remaining)
 for f in obj['files']:records[Path(f['path']).name]={v['id']:v['crit'] for v in f.get('traits',[])}
 remaining=remaining[end:].lstrip()
results=[]
for name,(trait,want) in expected.items():
 found=trait in records.get(name,{});results.append(dict(case=name,trait=trait,expected=want,found=found,passed=found==want))
 for_failure='' if found==want else f' expected {want}, found {found}'
 print(name, 'PASS' if found==want else 'FAIL'+for_failure)
(scratch/'boundary-results.json').write_text(json.dumps(results,indent=2)+'\n');assert all(v['passed'] for v in results),[v for v in results if not v['passed']]
print(len(results),'boundaries passed')
