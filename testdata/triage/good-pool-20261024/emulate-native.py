"""Bounded CPU-only decoder tracing. No specimen Windows APIs are executed."""
from pathlib import Path
import json,struct,re
import pefile,unicorn,capstone
from unicorn.x86_const import *
p=Path('/tmp/triage-good-20261024');inv=json.loads((p/'inventory.json').read_text())
for n in [63,64,65]:
 path=Path(inv[n]['path']);pe=pefile.PE(str(path));base=pe.OPTIONAL_HEADER.ImageBase;bits=64 if pe.FILE_HEADER.Machine==0x8664 else 32;size=(pe.OPTIONAL_HEADER.SizeOfImage+0xfff)&~0xfff
 u=unicorn.Uc(unicorn.UC_ARCH_X86,unicorn.UC_MODE_64 if bits==64 else unicorn.UC_MODE_32);u.mem_map(base,size);u.mem_write(base,pe.get_memory_mapped_image());stack=0x20000000;u.mem_map(stack,0x200000);sp=stack+0x100000;u.reg_write(UC_X86_REG_RSP if bits==64 else UC_X86_REG_ESP,sp);u.mem_map(0,0x10000);u.mem_map(0x7ffdf000,0x1000)
 u.mem_write(0x30,struct.pack('<I',0x7ffdf000));u.mem_write(0x7ffdf008,struct.pack('<I',base&0xffffffff));u.mem_write(0x7ffdf010,struct.pack('<Q',base));u.mem_write(sp,b'\0'*64)
 ipreg=UC_X86_REG_RIP if bits==64 else UC_X86_REG_EIP;api={};apis=0x30000000;u.mem_map(apis,0x10000);pack='<Q' if bits==64 else '<I'
 for lib in getattr(pe,'DIRECTORY_ENTRY_IMPORT',[]):
  for f in lib.imports:
   addr=apis+len(api)*16;api[addr]=lib.dll.decode(errors='replace')+'!'+(f.name.decode(errors='replace') if f.name else str(f.ordinal));u.mem_write(f.address,struct.pack(pack,addr));u.mem_write(addr,b'\xc3')
 trace=[];blocks=set();changes={};stops=[];count=[0]
 def code(uc,address,size,other):
  count[0]+=1
  if len(trace)<1000:trace.append(hex(address))
  if address in api:
   spnow=uc.reg_read(UC_X86_REG_RSP if bits==64 else UC_X86_REG_ESP);words=struct.unpack('<' + ('Q' if bits==64 else 'I')*12,uc.mem_read(spnow,(8 if bits==64 else 4)*12));args=[hex(x) for x in words]
   stops.append({'api':api[address],'ip':hex(address),'stack':args});uc.emu_stop()
 def block(uc,address,size,other):blocks.add(address)
 def write(uc,access,address,size,value,other):
  if base<=address<base+sizeimage:
   page=address&~0xfff;changes[page]=changes.get(page,0)+1
 def invalid(uc,access,address,size,value,other):stops.append({'invalid_access':access,'address':hex(address),'ip':hex(uc.reg_read(ipreg))});return False
 sizeimage=size
 u.hook_add(unicorn.UC_HOOK_CODE,code);u.hook_add(unicorn.UC_HOOK_BLOCK,block);u.hook_add(unicorn.UC_HOOK_MEM_WRITE,write);u.hook_add(unicorn.UC_HOOK_MEM_INVALID,invalid)
 try:u.emu_start(base+pe.OPTIONAL_HEADER.AddressOfEntryPoint,base+size,timeout=15_000_000,count=1000000)
 except unicorn.UcError as e:stops.append({'error':str(e)})
 out=p/'native'/str(n);out.mkdir(exist_ok=True);image=bytes(u.mem_read(base,size));(out/'emulated-image.bin').write_bytes(image);new=bytearray(path.read_bytes())
 for sec in pe.sections:
  new[sec.PointerToRawData:sec.PointerToRawData+sec.SizeOfRawData]=image[sec.VirtualAddress:sec.VirtualAddress+sec.SizeOfRawData]
 (out/'emulated.exe').write_bytes(new)
 strings=[]
 for m in re.finditer(rb'[ -~]{8,}',image):
  t=m.group().decode()
  if re.search(r'https?://|\.exe\b|\.dll\b|AppData|CurrentVersion|powershell|cmd\.exe|loadlibrary|virtualalloc|explorer|socket|GetProc',t,re.I):strings.append({'rva':hex(m.start()),'text':t[:250]})
 report={'index':n,'sha256':inv[n]['sha256'],'bits':bits,'instructions':count[0],'blocks':len(blocks),'last_ip':hex(u.reg_read(ipreg)),'stops':stops,'changed_pages':{hex(k):v for k,v in changes.items()},'initial_trace':trace,'strings':strings};(out/'emulation.json').write_text(json.dumps(report,indent=2));print(n,'instructions',count[0],'blocks',len(blocks),'stops',stops,'writes',len(changes),flush=True)
