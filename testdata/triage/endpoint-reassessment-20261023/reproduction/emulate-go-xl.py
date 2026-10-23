# Run selected Go application instructions only inside Unicorn. Runtime memory
# helpers are modeled; every syscall/Windows request is recorded and blocked.
import json,pefile,struct,time
from pathlib import Path
import unicorn
from unicorn.x86_const import *
row=next(s for s in json.load(open('/tmp/endpoint-review-20261023/inventory.json')) if s['sha256'].startswith('a989'))
p=pefile.PE(row['local_path']);base=p.OPTIONAL_HEADER.ImageBase;im=p.get_memory_mapped_image();root=Path('/tmp/endpoint-review-20261023/native/a9892231ad05')
fs=json.load(open(root/'go-functions.json'));by={f['va']:f['name'] for f in fs};addr={f['name']:f['va'] for f in fs};u=unicorn.Uc(unicorn.UC_ARCH_X86,unicorn.UC_MODE_64)
u.mem_map(base,(len(im)+4095)&~4095);u.mem_write(base,im)
for a,n in [(0x70000000,0x1000000),(0x80000000,0x4000000),(0x60000000,0x100000)]:u.mem_map(a,n)
u.reg_write(UC_X86_REG_R14,0x60001000);u.mem_write(0x60001010,struct.pack('<Q',0x70001000));heap=0x80001000;events=[];calls=0;winprocs={};handles={};tls={}
regs=[UC_X86_REG_RAX,UC_X86_REG_RBX,UC_X86_REG_RCX,UC_X86_REG_RDI,UC_X86_REG_RSI,UC_X86_REG_R8,UC_X86_REG_R9,UC_X86_REG_R10,UC_X86_REG_R11]
def allocate(n):
 global heap
 if n>0x1000000:raise RuntimeError('allocation bound '+str(n))
 a=heap;heap+=(max(n,1)+15)&~15
 if heap>=0x84000000:raise RuntimeError('heap bound')
 return a
q=lambda a:struct.unpack('<Q',u.mem_read(a,8))[0]
def string(a,n):return bytes(u.mem_read(a,min(n,10000))).decode(errors='replace') if a and n else ''
def cstring(a):
 try:return bytes(u.mem_read(a,512)).split(b'\0')[0].decode(errors='replace')
 except:return '<unmapped>'
def win(name,params):
 events.append({'winapi':name,'parameters':[hex(x) for x in params]})
 if name=='GetProcessHeap':return 1
 if name=='GetModuleFileNameW':
  text='C:\\Program Files\\Granite\\application.exe';u.mem_write(params[1],(text+'\0').encode('utf-16le'));return len(text)
 if name=='TlsAlloc':return 1
 if name=='TlsSetValue':tls[params[0]]=params[1];return 1
 if name=='TlsGetValue':return tls.get(params[0],0)
 if name in ['HeapAlloc','LocalAlloc','VirtualAlloc']:return allocate(params[2] if name=='HeapAlloc' else params[1])
 if name in ['GetCurrentProcess','GetCurrentThread']:return 0xffffffffffffffff
 if name=='HeapFree':return 1
 if name=='GetModuleHandleW':return base
 if name=='GetSystemMetrics':return 1920 if params[0]==0 else 1080
 if name in ['GetDC','CreateCompatibleDC','CreateCompatibleBitmap','BitBlt','DeleteDC','DeleteObject','ReleaseDC']:return 0x99
 raise Stop('recorded WinAPI '+name)
def goobj(a):
 result=[]
 for off in range(0,48,8):
  try:
   p,n=q(a+off),q(a+off+8)
   if p and 0<n<200:result.append({'offset':off,'text':string(p,n)})
  except:pass
 return result
class Stop(Exception):pass
def hook(u,a,size,user):
 global calls
 name=by.get(a)
 if not name or name.startswith('main.'):return
 if name.startswith(('runtime.duff','runtime.memclr')):return
 args=[u.reg_read(r) for r in regs];sp=u.reg_read(UC_X86_REG_RSP);ret=q(sp);out=[];calls+=1
 if calls>500000:raise Stop('call bound')
 if name=='runtime.newobject':out=[allocate(q(args[0]))]
 elif name=='runtime.makeslice':out=[allocate(args[2]*q(args[0]))]
 elif name=='runtime.growslice':
  n,cap=args[1],max(args[1],args[2]*2,4);sz=q(args[4]);a=allocate(cap*sz);u.mem_write(a,bytes(u.mem_read(args[0],max(0,n-args[3])*sz)));out=[a,n,cap]
 elif name=='runtime.stringtoslicebyte':
  a=allocate(args[2]);u.mem_write(a,bytes(u.mem_read(args[1],args[2])));out=[a,args[2],args[2]]
 elif name=='runtime.slicebytetostring':out=[args[1],args[2]]
 elif name=='runtime.memmove':u.mem_write(args[0],bytes(u.mem_read(args[1],args[2])))
 elif name.startswith('runtime.print'):pass
 elif name.startswith(('runtime.panic','runtime.morestack','runtime.throw','runtime.fatal')):raise Stop(name)
 elif name=='syscall.(*LazyProc).Call':
  e={'call':name,'object':hex(args[0]),'fields':goobj(args[0]),'return_address':hex(ret),'args':[hex(x) for x in args[1:4]]};events.append(e)
  names=' '.join(x['text'] for x in e['fields'])
  params=list(struct.unpack('<'+'Q'*args[2],u.mem_read(args[1],args[2]*8))) if args[2] else [];out=[win(names,params),0,0]
 elif name=='syscall.LoadLibrary':
  text=string(args[0],args[1]);events.append({'LoadLibrary':text});out=[0x51000000,0,0]
 elif name=='syscall.GetProcAddress':
  text=string(args[1],args[2]);fake=0x60010000+len(winprocs)*16;winprocs[fake]=text;events.append({'GetProcAddress':text});out=[fake,0,0]
 elif name=='syscall.SyscallN':
  params=list(struct.unpack('<'+'Q'*args[2],u.mem_read(args[1],args[2]*8))) if args[2] else [];out=[win(winprocs.get(args[0],hex(args[0])),params),0,0]
 elif name=='syscall.UTF16ToString':
  raw=bytes(u.mem_read(args[0],args[1]*2));t=raw.decode('utf-16le',errors='replace').split('\0')[0].encode();a=allocate(len(t));u.mem_write(a,t);out=[a,len(t)]
 elif name.startswith('syscall.'):
  events.append({'call':name,'return_address':hex(ret),'args':[hex(x) for x in args], 'objects':[goobj(x) for x in args[:3]]});raise Stop('recorded syscall boundary')
 else:
  events.append({'call':name,'return_address':hex(ret),'args':[hex(x) for x in args]});raise Stop('unmodeled Go call '+name)
 for r,v in zip(regs,out):u.reg_write(r,v)
 u.reg_write(UC_X86_REG_RSP,sp+8);u.reg_write(UC_X86_REG_RIP,ret)
# Function-start hooks leave internal compiler helpers and application branches intact.
for a,name in by.items():
 if not name.startswith('main.'):u.hook_add(unicorn.UC_HOOK_CODE,hook,begin=a,end=a)
def run(name):
 sp=0x70f00008;end=0x600ff000;u.mem_write(sp,struct.pack('<Q',end));u.reg_write(UC_X86_REG_RSP,sp);start=time.monotonic()
 try:u.emu_start(addr[name],end,timeout=15000000,count=300000000);reason='return or bound'
 except (Stop,RuntimeError,unicorn.UcError) as e:reason=str(e)
 events.append({'function':name,'reason':reason,'pc':hex(u.reg_read(UC_X86_REG_RIP)),'seconds':time.monotonic()-start})
run('main.init');run('main.main');(root/'emulation.json').write_text(json.dumps({'events':events,'calls':calls},indent=2));print(json.dumps(events,indent=2))
