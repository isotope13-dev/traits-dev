import pefile,struct,pathlib,json
from unicorn import *
from unicorn.x86_const import *
p=pathlib.Path('/usr/local/var/cyclotron/tmp.noindex/cyclotron-90084b2c/scratch/review-9f-e1-eb')
pe=pefile.PE('/usr/local/var/cyclotron/tmp.noindex/cyclotron-90084b2c/samples/9f63afa87f63/9f63afa87f638e54379c1b2d0980348936a7c40eb3039a294be96663d0a854bc.exe')
u=Uc(UC_ARCH_X86,UC_MODE_64);base=pe.OPTIONAL_HEADER.ImageBase
u.mem_map(base,0x200000);u.mem_write(base,pe.get_memory_mapped_image())
u.mem_map(0x100000,0x100000);u.reg_write(UC_X86_REG_RSP,0x1ff008);u.mem_write(0x1ff008,struct.pack('<Q',0x300000))
u.mem_map(0x300000,0x10000);u.mem_write(0x300000,b'\xc3'*0x10000)
heap=0x10000000;allocs={};stubs={};names={};resources={}
def stub(n):
 if n not in names:
  a=0x301000+len(names)*16;names[n]=a;stubs[a]=n
 return names[n]
for d in pe.DIRECTORY_ENTRY_IMPORT:
 for i in d.imports:u.mem_write(i.address,struct.pack('<Q',stub(i.name.decode())))
for e in pe.DIRECTORY_ENTRY_RESOURCE.entries:
 for e2 in e.directory.entries:
  for e3 in e2.directory.entries:
   d=e3.data.struct;resources[str(e2.name)]=(base+d.OffsetToData,d.Size)
print('resources',resources,flush=True)
for off,n in [(0x10038,'FindResourceA'),(0x10030,'LoadResource'),(0x10028,'LockResource'),(0x10020,'SizeofResource')]:u.mem_write(base+off,struct.pack('<Q',stub(n)))
def cs(a):return bytes(u.mem_read(a,200)).split(b'\0')[0].decode(errors='replace')
def allocate(n):
 global heap
 a=heap;heap+=(n+0xfff)&~0xfff;u.mem_map(a,(n+0xfff)&~0xfff);allocs[a]=n;return a

def hook(u,a,size,data):
 if a==0x300000:u.emu_stop();return
 if a not in stubs:return
 n=stubs[a];c,d,r,s=[u.reg_read(x) for x in [UC_X86_REG_RCX,UC_X86_REG_RDX,UC_X86_REG_R8,UC_X86_REG_R9]];v=1
 if n=='FindResourceA':
  key=cs(d);v=resources.get(key,(0,0))[0];print(n,key,hex(v),flush=True)
 elif n in ['LoadResource','LockResource']:v=d if n=='LoadResource' else c
 elif n=='SizeofResource':v=next((sz for addr,sz in resources.values() if addr==d),0)
 elif n=='GetProcessHeap':v=0x99
 elif n=='HeapAlloc':v=allocate(r)
 elif n=='HeapReAlloc':
  v=allocate(s);u.mem_write(v,bytes(u.mem_read(r,min(allocs[r],s))))
 elif n=='VirtualAlloc':
  v=allocate(d);print(n,hex(v),hex(d),hex(s),flush=True)
 elif n=='VirtualFree':
  print(n,hex(c),flush=True)
 elif n=='LoadLibraryA':print(n,cs(c),flush=True);v=0x777
 elif n=='GetProcAddress':print(n,cs(d),flush=True);v=stub(cs(d))
 elif n=='CreateThread':
  print(n,hex(r),hex(s),flush=True);u.emu_stop()
 elif n=='VirtualProtect':print(n,hex(c),hex(d),hex(r),flush=True)
 else:print(n,hex(c),hex(d),hex(r),hex(s),flush=True)
 u.reg_write(UC_X86_REG_RAX,v)
 rsp=u.reg_read(UC_X86_REG_RSP);ret=struct.unpack('<Q',u.mem_read(rsp,8))[0];u.reg_write(UC_X86_REG_RSP,rsp+8);u.reg_write(UC_X86_REG_RIP,ret)
u.hook_add(UC_HOOK_CODE,hook,begin=0x300000,end=0x310000)
def dump(u,a,size,data):
 addr=struct.unpack('<Q',u.mem_read(u.reg_read(UC_X86_REG_RSP)+0xa0,8))[0];sz=struct.unpack('<I',u.mem_read(u.reg_read(UC_X86_REG_RSP)+0xa8,4))[0]
 print('payload',hex(addr),sz,flush=True);(p/'payload.exe').write_bytes(bytes(u.mem_read(addr,sz)))
u.hook_add(UC_HOOK_CODE,dump,begin=base+0x2030,end=base+0x2030)
try:u.emu_start(base+0x1470,0x300000,timeout=240000000,count=600000000)
except UcError as e:print('error',e,hex(u.reg_read(UC_X86_REG_RIP)))
print('ended',hex(u.reg_read(UC_X86_REG_RIP)),flush=True)
for addr,sz in allocs.items():
 b=bytes(u.mem_read(addr,sz));(p/f'alloc-{addr:x}.bin').write_bytes(b)
