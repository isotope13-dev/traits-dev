from pathlib import Path
import pefile,json,struct,capstone
from unicorn import *
from unicorn.x86_const import *
r=Path('/tmp/hopper-new-review-20261023');i=next(x for x in json.load(open(r/'inventory.json')) if x['sha256'].startswith('b4fa4397c031'));p=pefile.PE(i['path']);b=Path(i['path']).read_bytes();base=p.OPTIONAL_HEADER.ImageBase;image=p.get_memory_mapped_image();u=Uc(UC_ARCH_X86,UC_MODE_32);u.mem_map(base,(p.OPTIONAL_HEADER.SizeOfImage+0x10000+4095)&~4095);u.mem_write(base,image);u.mem_map(0x70000000,0x200000);u.reg_write(UC_X86_REG_ESP,0x70100000);u.mem_write(0x70100000,struct.pack('<I',0xdeadbeef));start=base+p.OPTIONAL_HEADER.AddressOfEntryPoint;calls={z.address:x.dll.decode()+':'+(z.name.decode() if z.name else str(z.ordinal)) for x in p.DIRECTORY_ENTRY_IMPORT for z in x.imports};stop=[];last=[];steps=[0];cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_32)
# Any attempted imported API stops emulation. Only decompression instructions run.
for at in calls:u.mem_write(at,struct.pack('<I',0x60000000+len(stop)*0x100))
def hook(uc,at,sz,_):
 steps[0]+=1;last.append(at)
 if len(last)>30:last.pop(0)
 if at<start and at>=base+0x1000 and steps[0]>100:
  stop.append({'reason':'transfer to decompressed image','at':hex(at)});uc.emu_stop()
 if 0x60000000<=at<0x60100000:stop.append({'reason':'import boundary','at':hex(at)});uc.emu_stop()
def invalid(uc,access,addr,size,value,_):stop.append({'reason':'unmapped','at':hex(uc.reg_read(UC_X86_REG_EIP)),'address':hex(addr)});return False
u.hook_add(UC_HOOK_CODE,hook);u.hook_add(UC_HOOK_MEM_INVALID,invalid)
try:u.emu_start(start,base+p.OPTIONAL_HEADER.SizeOfImage,count=10000000)
except UcError as e:stop.append({'error':str(e)})
mem=bytes(u.mem_read(base,p.OPTIONAL_HEADER.SizeOfImage));out=Path('/tmp/hopper-deep-review-20261023/upx-memory.bin');out.write_bytes(mem);info={'steps':steps[0],'stop':stop,'last':[hex(x) for x in last]};Path('/tmp/hopper-deep-review-20261023/upx-emulation.json').write_text(json.dumps(info,indent=2));print(info)
# Rebuild a disk view, retaining raw extraction explicitly rather than claiming a pristine original.
q=pefile.PE(data=mem);q.OPTIONAL_HEADER.AddressOfEntryPoint=int(stop[0]['at'],16)-base if stop and stop[0].get('reason')=='transfer to decompressed image' else q.sections[0].VirtualAddress
for s in q.sections:
 s.PointerToRawData=s.VirtualAddress;s.SizeOfRawData=(s.Misc_VirtualSize+511)&~511
 s.Name=s.Name.replace(b'UPX0',b'.tex').replace(b'UPX1',b'.dat').replace(b'UPX2',b'.imp')
q.OPTIONAL_HEADER.CheckSum=0;mem=bytearray(mem);hdr=q.write()[:q.OPTIONAL_HEADER.SizeOfHeaders];mem[:len(hdr)]=hdr;Path('/tmp/hopper-deep-review-20261023/upx-reconstructed.exe').write_bytes(mem)
print('Strings',[(m.group()[:150]) for m in __import__('re').finditer(rb'[\x20-\x7e]{8,}',mem) if any(t in m.group().lower() for t in [b'http',b'password',b'wallet',b'stratum',b'xmrig',b'cmd.exe',b'bitcoin'])][:25])
