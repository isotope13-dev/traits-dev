import pefile,struct,zlib,json
from pathlib import Path
from unicorn import Uc,UC_ARCH_X86,UC_MODE_32
from unicorn.x86_const import UC_X86_REG_ECX,UC_X86_REG_ESP
import argparse
args=argparse.ArgumentParser(description="Recover table-decoded CLR resource without executing the sample")
args.add_argument("sample",type=Path)
args.add_argument("output",type=Path)
opts=args.parse_args()
base=opts.output
base.mkdir(parents=True,exist_ok=True)
p=pefile.PE(str(opts.sample))
for t in p.DIRECTORY_ENTRY_RESOURCE.entries:
 for n in t.directory.entries:
  for l in n.directory.entries:
   d=l.data.struct; b=p.get_data(d.OffsetToData,d.Size);print(t.id,str(n.name or n.id),d.Size)
   if t.id==10 and str(n.name)=="__": data=b
u=Uc(UC_ARCH_X86,UC_MODE_32);u.mem_map(0x400000,0x200000);u.mem_write(0x400000,p.get_memory_mapped_image());u.mem_map(0x1000000,0x100000);u.mem_map(0x2000000,0x100000)
u.reg_write(UC_X86_REG_ESP,0x20ff000);u.mem_write(0x20ff000,struct.pack('<I',0x500000));u.reg_write(UC_X86_REG_ECX,0x1000000)
u.emu_start(0x401300,0x500000,count=10000000)
tab=bytes(u.mem_read(0x1000000,0x40022)); out=bytearray()
for off in range(0,len(data),1024):
 b=bytearray(data[off:off+1024]); n=len(b); k=tab[0x20020]
 if n==1: b[0]=tab[0x10000+b[0]*256+k]
 else:
  for i in range(n-1): b[i]=tab[0x10000+b[i]*256+b[i+1]]
  b[-1]=tab[0x10000+b[-1]*256+(k^0x55)]
  for i in range(n-1,0,-1): b[i]=tab[0x10000+b[i]*256+b[i-1]]
  b[0]=tab[0x10000+b[0]*256+k]
 out+=b
base.joinpath('decoded.bin').write_bytes(out);print('decoded',out[:30].hex())
payload=zlib.decompress(out[4:]); print('size prefix',struct.unpack('<I',out[:4])[0],'decompressed',len(payload),payload[:40]);base.joinpath('managed.exe').write_bytes(payload[14:])
