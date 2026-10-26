import pathlib,struct,re,pefile
from unicorn import *
from unicorn.x86_const import *
p=pathlib.Path('/usr/local/var/cyclotron/tmp.noindex/cyclotron-90084b2c/scratch/review-9f-e1-eb');pe=pefile.PE(str(p/'payload.exe'));b=pe.OPTIONAL_HEADER.ImageBase
u=Uc(UC_ARCH_X86,UC_MODE_64);u.mem_map(b,0x300000);u.mem_write(b,pe.get_memory_mapped_image());u.mem_map(0x100000,0x100000);u.reg_write(UC_X86_REG_RSP,0x1ff008);u.mem_write(0x1ff008,struct.pack('<Q',0x300000));u.mem_map(0x300000,0x1000)
log=[]
def invalid(u,access,address,size,value,data):
 print('unmapped',access,hex(address),'at',hex(u.reg_read(UC_X86_REG_RIP)),flush=True);return False
u.hook_add(UC_HOOK_MEM_INVALID,invalid)
try:u.emu_start(b+pe.OPTIONAL_HEADER.AddressOfEntryPoint,0x300000,timeout=15000000,count=2000000)
except UcError as e:print(e)
print('stopped',hex(u.reg_read(UC_X86_REG_RIP)))
for name,address,size in [('stack',0x100000,0x100000),('image',b,0x300000)]:
 out=bytes(u.mem_read(address,size));(p/f'inner-{name}.bin').write_bytes(out)
 ss=re.findall(rb'[\x20-\x7e]{6,}',out)
 for s in ss:
  if re.search(rb'password|http|kernel|ntdll|LoadLibrary|GetProcAddress|\.dll|\.exe|\.pdb|AppData',s,re.I):print(name,s[:500])
