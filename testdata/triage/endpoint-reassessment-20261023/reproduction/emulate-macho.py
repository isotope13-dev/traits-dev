# Mach-O loader subset for isolated x86-64 CPU emulation. Imported OS APIs are
# inert and task_info fails explicitly; no host process or network bridge.
from pathlib import Path
import json,struct,time,re
import unicorn
from unicorn.x86_const import *
row=next(s for s in json.load(open('/tmp/endpoint-review-20261023/inventory.json')) if s['sha256'].startswith('af9fed'))
raw=Path(row['local_path']).read_bytes();n=struct.unpack_from('>I',raw,4)[0];archs=[struct.unpack_from('>5I',raw,8+i*20) for i in range(n)];cpu,sub,off,size,align=next(x for x in archs if x[0]==0x1000007);data=raw[off:off+size];hdr=struct.unpack_from('<IiiIIIII',data);at=32;segs=[];initializers=[];entryoff=None
for i in range(hdr[4]):
 cmd,sz=struct.unpack_from('<II',data,at)
 if cmd==0x19:
  name=data[at+8:at+24].split(b'\0')[0].decode();va,vs,fo,fs,mp,ip,ns,flags=struct.unpack_from('<4Q4I',data,at+24)
  segs.append((name,va,vs,fo,fs))
  for j in range(ns):
   sec=at+72+j*80;sn=data[sec:sec+16].split(b'\0')[0].decode();sa,ss,sfo=struct.unpack_from('<QQI',data,sec+32)
   if sn=='__mod_init_func':initializers += list(struct.unpack_from('<'+'Q'*(ss//8),data,sfo))
 if cmd==0x80000028:entryoff=struct.unpack_from('<Q',data,at+8)[0]
 at+=sz
u=unicorn.Uc(unicorn.UC_ARCH_X86,unicorn.UC_MODE_64)
for name,va,vs,fo,fs in segs:
 if name=='__PAGEZERO' or not vs:continue
 u.mem_map(va,(vs+4095)&~4095);u.mem_write(va,data[fo:fo+fs])
u.mem_map(0x70000000,0x1000000);u.mem_map(0x80000000,0x4000000);u.mem_map(0x60000000,0x100000)
u.mem_write(0x1000cfd70,struct.pack('<Q',0x60001000));u.mem_write(0x60001000,struct.pack('<Q',0x123456789abcdef0));u.mem_write(0x1000cfd78,struct.pack('<Q',0x60001010));u.mem_write(0x60001010,struct.pack('<I',1))
u.mem_write(0x60002000,struct.pack('<QQ',0x60003000,0));u.mem_write(0x60003000,b'/Applications/utility\0')
info=json.load(open('/tmp/endpoint-review-20261023/native/af9fedc9c2e8/decoded-info.json'));imports={x['plt']:x['name'] for x in info['imports'] if x.get('plt')};heap=0x80001000;events=[];stops=[];allocations={}
def allocate(n):
 global heap
 if n>0x1000000:raise RuntimeError('allocation bound')
 a=heap;heap+=(max(1,n)+15)&~15
 if heap>=0x84000000:raise RuntimeError('heap bound')
 allocations[a]=n;return a
class Stop(Exception):pass
def hook(u,a,size,_):
 name=imports.get(a)
 if not name:return
 regs=[UC_X86_REG_RDI,UC_X86_REG_RSI,UC_X86_REG_RDX,UC_X86_REG_RCX,UC_X86_REG_R8,UC_X86_REG_R9];args=[u.reg_read(r) for r in regs];sp=u.reg_read(UC_X86_REG_RSP);ret=struct.unpack('<Q',u.mem_read(sp,8))[0];events.append({'api':name,'caller':hex(ret),'args':[hex(x) for x in args]});result=0
 if len(events)>1000:raise Stop('API bound')
 if name=='malloc':result=allocate(args[0])
 elif name=='calloc':result=allocate(args[0]*args[1])
 elif name in ['free']:pass
 elif name=='memcpy':u.mem_write(args[0],bytes(u.mem_read(args[1],args[2])));result=args[0]
 elif name=='__bzero':u.mem_write(args[0],b'\0'*args[1])
 elif name=='strlen':result=len(bytes(u.mem_read(args[0],100000)).split(b'\0')[0])
 elif name in ['getpid']:result=1000
 elif name=='time':result=1792770000
 elif name=='mach_task_self_':result=1
 elif name=='task_info':result=5
 elif name=='pthread_once':
  if bytes(u.mem_read(args[0],8))==b'\0'*8:
   u.mem_write(args[0],struct.pack('<Q',1));u.reg_write(UC_X86_REG_RIP,args[1]);return
 elif name=='__stack_chk_fail':raise Stop('stack canary failure')
 else:raise Stop('unimplemented '+name)
 u.reg_write(UC_X86_REG_RAX,result);u.reg_write(UC_X86_REG_RSP,sp+8);u.reg_write(UC_X86_REG_RIP,ret)
for a in imports:u.hook_add(unicorn.UC_HOOK_CODE,hook,begin=a,end=a)
def sys(u,_):raise Stop('syscall intercepted')
u.hook_add(unicorn.UC_HOOK_INSN,sys,None,1,0,UC_X86_INS_SYSCALL)
base=next(x[1] for x in segs if x[0]=='__TEXT')
for entry in initializers+[base+entryoff]:
 sp=0x70f00008;end=0x600ff000;u.mem_write(sp,struct.pack('<Q',end));u.reg_write(UC_X86_REG_RSP,sp);start=time.monotonic()
 if entry==base+entryoff:u.reg_write(UC_X86_REG_RDI,1);u.reg_write(UC_X86_REG_RSI,0x60002000)
 try:u.emu_start(entry,end,timeout=10000000,count=300000000);reason='return or bound'
 except (Stop,RuntimeError,unicorn.UcError) as e:reason=str(e)
 stops.append({'entry':hex(entry),'pc':hex(u.reg_read(UC_X86_REG_RIP)),'reason':reason,'seconds':time.monotonic()-start})
new=[]
for name,va,vs,fo,fs in segs:
 if name not in ['__DATA','__DATA_CONST']:continue
 b=bytes(u.mem_read(va,vs));original=data[fo:fo+fs]
 for m in re.finditer(rb'[ -~]{8,300}',b):
  if m[0] not in original and re.search(rb'https?://|/bin/|/tmp/|dylib|sysctl|osascript',m[0]):new.append({'va':hex(va+m.start()),'string':m[0].decode()})
root=Path('/tmp/endpoint-review-20261023/native/af9fedc9c2e8');(root/'emulation.json').write_text(json.dumps({'initializers':[hex(x) for x in initializers],'stops':stops,'events':events,'new_strings':new},indent=2));print(json.dumps({'stops':stops,'apis':sorted(set(x['api'] for x in events)),'new_strings':new},indent=2))
