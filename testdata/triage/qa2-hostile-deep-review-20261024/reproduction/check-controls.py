"""Scan original samples and source/byte mutations; execute no samples."""
from pathlib import Path
import argparse,json,tempfile,subprocess,os,struct,textwrap,collections
ROOT=Path('/home/t/src/traits-dev');WORK=Path('/tmp/qa2-deep-review')
HEADER='micro-behaviors/data/control-flow/branch::response-header-task-handler-dispatch'
CHANNEL='objectives/command-and-control/remote-command/tasking::obfuscated-wsh-header-powershell-channel'
PROFILE='objectives/discovery/system/profile::header-command-agent-system-process-profile'
REMOVE='objectives/evasion/self-delete/cleanup/remove::header-command-agent-removal-routines'
START='objectives/supply-chain/install-hook/dropper/hook-setup::pypi-remote-executable-start-attempt'
MUTANT='objectives/anti-static/obfuscation/payload/polymorphic/generator::self-mutating-image-submission-loop'
REG='micro-behaviors/os/registry/delete::js-regdelete-method-call'
DELETE='micro-behaviors/fs/delete/file/library::js-bracket-deletefile-call'
rows=json.load(open(WORK/'samples.json'));cases=[]
with tempfile.TemporaryDirectory(prefix='endpoint-flow-boundaries-') as scratch:
 scratch=Path(scratch)
 def case(name,body,required=(),forbidden=(),basename=None,max_susp=None):
  p=scratch/name/(basename or ('input.js' if isinstance(body,str) else 'input.exe'));p.parent.mkdir(parents=True);p.write_text(body) if isinstance(body,str) else p.write_bytes(body);cases.append((name,p,set(required),set(forbidden),max_susp))
 for r in rows:
  sha=r['sha256'];required=set();max_susp=None
  if sha.startswith(('201707','311006','aab86')):required.add(MUTANT)
  elif sha.startswith('2e5c'):required.update([CHANNEL,PROFILE,REMOVE])
  elif sha.startswith('7e916'):required.add(START)
  elif sha.startswith(('7b5','eeab','a03','e60','2c4645','67a031')):max_susp=1
  cases.append((sha[:12],Path(r['analysis_path']),required,set(),max_susp))
 setup=next(Path('/tmp/qa2/hostile').glob('7e916*/setup.py')).read_text()
 case('installer-corrected-api',setup.replace('urllib.urlrequest','urllib.request'),[START],basename='setup.py')
 case('installer-changed-destination',setup.replace('syswin32.exe','different-helper.exe').replace('https://tryg.ga','https://changed.example.net'),[START],basename='setup.py')
 case('installer-wrong-file',setup.replace("['start', 'syswin32.exe']","['start', 'unrelated.exe']"),forbidden=[START],basename='setup.py')
 case('installer-no-shell',setup.replace('shell=True','shell=False'),forbidden=[START],basename='setup.py')
 case('installer-no-download',setup.replace('urlretrieve','retrieveLocal'),forbidden=[START],basename='setup.py')
 case('installer-text-resource',setup.replace('syswin32.exe','resource.txt'),forbidden=[START],basename='setup.py')
 case('installer-different-verb',setup.replace("['start',","['echo',"),forbidden=[START],basename='setup.py')
 case('installer-unused-helper','def unused():\n'+textwrap.indent(setup,'    '),forbidden=[START],basename='setup.py')
 case('installer-documentation','documentation = '+repr(setup)+'\n',forbidden=[START],basename='setup.py')
 case('ordinary-setup',"from setuptools import setup\nsetup(name='ordinary',version='1.0')\n",forbidden=[START],basename='setup.py',max_susp=0)
 case('direct-header-handler',"switch (response.GetResponseHeader('X-Task')) {case 'go': handle(response); break;}",[HEADER],forbidden=[CHANNEL,PROFILE,REMOVE],max_susp=0)
 case('wrong-header-response',"switch (response.GetResponseHeader('X-Task')) {case 'go': handle(unrelated); break;}",forbidden=[HEADER,CHANNEL])
 case('proxy-header-handler',"switch (api['GetResponseHeader'](response,key)) {case 'go': handlers.any(controller,response); break;}",[HEADER],forbidden=[CHANNEL])
 case('proxy-wrong-response',"switch (api['GetResponseHeader'](response,key)) {case 'go': handlers.any(controller,unrelated); break;}",forbidden=[HEADER,CHANNEL])
 case('bracket-delete-calls',"files['DeleteFile'](path); shell['RegDelete'](key);",[DELETE,REG],forbidden=[REMOVE],max_susp=0)
 case('delete-property-references',"var a = files['DeleteFile']; var b = shell['RegDelete'];",forbidden=[DELETE,REG,REMOVE],max_susp=0)
 rfq=(WORK/'rfq-engine-decoded.js').read_text()
 case('rfq-decoded',rfq,[CHANNEL,PROFILE,REMOVE])
 case('rfq-other-header',rfq.replace('X-A','X-Other-Task'),[CHANNEL,PROFILE,REMOVE])
 case('rfq-no-header-dispatch',rfq.replace('GetResponseHeader','ReadResponseNote'),forbidden=[HEADER,CHANNEL,PROFILE,REMOVE])
 case('rfq-no-powershell',rfq.replace('powershell -nop -enc','python -placeholder'),forbidden=[CHANNEL,PROFILE,REMOVE])
 case('rfq-no-registry-removal',rfq.replace('RegDelete','ReadRegistry'),[CHANNEL,PROFILE],forbidden=[REMOVE])
 case('rfq-no-file-removal',rfq.replace('DeleteFile','InspectFile'),[CHANNEL,PROFILE],forbidden=[REMOVE])
 native=next(Path('/tmp/qa2/hostile').glob('aab*/*')).read_bytes()
 b=bytearray(native);off=0x401551-0x401000+0x400;assert b[off]==0xe8;b[off:off+5]=bytes.fromhex('31 c0 90 90 90');case('native-no-random-mutation',b,forbidden=[MUTANT])
 b=bytearray(native);off=0x40158d-0x401000+0x400;assert struct.unpack_from('<I',b,off)[0]==0x423020;struct.pack_into('<I',b,off,0x423024);case('native-different-clone-buffer',b,forbidden=[MUTANT])
 command=[str(ROOT.parent/'cleave/target/release/cleave'),'--traits-dir',str(ROOT),'analyze','--format','jsonl',*[str(c[1]) for c in cases]]
 run=subprocess.run(command,text=True,capture_output=True,env={**os.environ,'CLEAVE_SKIP_CACHE':'1'});assert run.returncode==0,run.stderr[-3000:]
 reports={r['files'][0]['path']:r for r in map(json.loads,run.stdout.splitlines()) if r.get('files')}
 results=[]
 for name,p,required,forbidden,max_susp in cases:
  r=reports.get(str(p));assert r is not None,(name,'missing result');ts={t['id']:t['crit'] for f in r['files'] for t in f.get('traits',[])}
  missing=sorted(required-ts.keys());unexpected=sorted(forbidden & ts.keys());h=sum(v==5 for v in ts.values());s=sum(v==4 for v in ts.values());passed=not missing and not unexpected and (max_susp is None or h==0 and s<=max_susp)
  results.append({'case':name,'passed':passed,'missing':missing,'unexpected':unexpected,'hostile':h,'suspicious':s,'max_suspicious':max_susp});print('PASS' if passed else 'FAIL',name,missing,unexpected,h,s,flush=True)
 (WORK/'boundary-results.json').write_text(json.dumps(results,indent=2)+'\n');assert all(r['passed'] for r in results),[r for r in results if not r['passed']]
print(len(results),'boundary checks passed')
