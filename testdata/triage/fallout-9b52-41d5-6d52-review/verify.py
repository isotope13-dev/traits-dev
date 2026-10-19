#!/usr/bin/env python3
"""Static regression controls. Never executes a sample or contacts its C2."""
import argparse, concurrent.futures, hashlib, json, os, pathlib, struct, subprocess
P=argparse.ArgumentParser();P.add_argument('samples',type=pathlib.Path);P.add_argument('output',type=pathlib.Path);a=P.parse_args();a.output.mkdir(parents=True,exist_ok=True)
inputs={
 'dotnet':('9b5270d17a1d/xoilac86zsz.io_ransome.exe','9b5270d17a1d230dd50aa4f1f23e6dd0d789e289cc28d409f75c05cde6fb6072'),
 'native':('41d58fabb989/2026-10-19_b559d1b81f67c4e3bc631f682e5c4585_elex_wannacry','41d58fabb9890cbaa1196571d04fbc644a41705dee4bd08edce0ebcbdd16bec0'),
 'ios':('6d522977b4f5/99d0_decompressed_start256.bin','6d522977b4f5473050ae9f493cc34e837110fd5b06c236517c317d15623ba86c')}
paths={};data={}
for n,(rel,sha) in inputs.items():
 paths[n]=a.samples/rel;data[n]=paths[n].read_bytes();assert hashlib.sha256(data[n]).hexdigest()==sha
loader='objectives/execution/payload/module-load::ios-evasive-http-memory-loader'
family='well-known/malware/stealer/coruna-ios::coruna-ios-reporting-dylib'
probe='objectives/anti-analysis/emulator-detect::corellium-daemon-stat-probe'
webcam='objectives/collection/camera::managed-keylogger-vfw-frame-save-attempt'
cron='micro-behaviors/process/argument/option::cron-daemon-commandline'
serial='micro-behaviors/os/sysinfo/machine-id::ioplatformserialnum'
oldserial='objectives/discovery/system/fingerprint/machine-id::ioplatformserialnum'
cases=[]
def case(n,p,yes=(),no=()):cases.append((n,p,set(yes),set(no)))
def mutate(n,source,old,new,yes=(),no=()):
 assert old in data[source] and len(old)==len(new)
 p=a.output/(n+('.bin' if source=='ios' else '.exe'));p.write_bytes(data[source].replace(old,new));case(n,p,yes,no)
case('ios-original',paths['ios'],[loader,family,probe,serial],[oldserial,'well-known/malware/stealer/coruna-ios::coruna-ios-fingerprint-exfil-dylib'])
case('dotnet-original',paths['dotnet'],[webcam])
case('native-original',paths['native'],['objectives/persistence/login/registry/autostart::active-setup-service-dll-injector','objectives/persistence/system/service/loader::lanmanserver-resource-injection-hijack'])
mutate('ios-no-corellium','ios',b'/usr/libexec/corelliumd',b'/usr/libexec/ordinarydd',[serial],[probe,loader,family,'objectives/anti-analysis/vm-detect/artifact::macos-vm-hardware-check'])
mutate('ios-no-entry-dispatch','ios',bytes.fromhex('e00313aaea0315aad2120094f60300aa'),bytes.fromhex('e00313aaea031faad2120094f60300aa'),[probe],[loader,family])
mutate('ios-no-cipher-constant','ios',b'expand 32-byte k',b'ordinary data 00',[probe],[loader,family])
mutate('ios-no-family-template','ios',b'{"cmd":"logmsg","args":{"msg":"%s"}}',b'{"cmd":"notice","args":{"msg":"%s"}}',[loader],[family])
mutate('ios-no-serial-name','ios',b'IOPlatformSerialNumber',b'IOPlatformSerialNamere',[loader,family],[serial,oldserial])
mutate('dotnet-no-savedib','dotnet',bytes.fromhex('062025040000160928170000062609282f00000a'),bytes.fromhex('062024040000160928170000062609282f00000a'),[],[webcam])
mutate('dotnet-no-capture-api','dotnet',b'capCreateCaptureWindowA',b'napCreateCaptureWindowA',[],[webcam])
def elf(text):
 # A relocatable ELF with named, nonexecutable string data; no entry point.
 names=b'\0.shstrtab\0.rodata\0';blob=text.encode()+b'\0';off=64+len(names);shoff=(off+len(blob)+7)&~7
 ident=b'\x7fELF\x02\x01\x01'+b'\0'*9
 header=struct.pack('<16sHHIQQQIHHHHHH',ident,1,62,1,0,0,shoff,0,64,0,0,64,3,1)
 section=lambda *v:struct.pack('<IIQQQQIIQQ',*v)
 return header+names+blob+b'\0'*(shoff-off-len(blob))+b'\0'*64+section(1,3,0,0,64,len(names),0,0,1,0)+section(11,1,2,0,off,len(blob),0,0,1,0)
for label,text,expected in [('cron-foreground','/usr/sbin/cron -f',True),('cron-nofork','/usr/sbin/cron -n',True),('cron-path-only','/usr/sbin/cron',False)]:
 p=a.output/(label+'.elf');p.write_bytes(elf(text));case(label,p,[cron] if expected else [],[] if expected else [cron])
# Consumer/reference migration retains the same command matcher and scope.
env=dict(os.environ);env.pop('SCAN_HOPPER',None);env['CLEAVE_TRAITS_DIR']=str(pathlib.Path.cwd());env['SCAN_FETCH']='none'
def run(c):
 n,p,yes,no=c
 r=subprocess.run(['atomscan','--no-update','--mode','slow','--format','json',str(p)],env=env,capture_output=True,text=True)
 (a.output/(n+'.scan.json')).write_text(r.stdout);(a.output/(n+'.scan.err')).write_text(r.stderr)
 d=json.loads(r.stdout)['raw'];ts=[t for f in d['files'] for t in f.get('traits',[])];ids={t['id'] for t in ts}
 assert yes<=ids,(n,'missing',yes-ids)
 assert not(no&ids),(n,'unexpected',no&ids)
 assert not r.stderr.strip(),(n,r.stderr)
 out={'case':n,'required':sorted(yes),'absent':sorted(no),'hostile':[t['id'] for t in ts if t['crit']==5],'suspicious':[t['id'] for t in ts if t['crit']==4]}
 print(n,'PASS',flush=True);return out
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:results=list(pool.map(run,cases))
(a.output/'results.json').write_text(json.dumps(results,indent=2)+'\n')
print(len(results),'controls passed')
