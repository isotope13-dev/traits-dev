# Isolate only the table-building function. No host API or program entry runs.
from pathlib import Path
import pefile,json,struct,zlib,hashlib
from unicorn import *
from unicorn.x86_const import *
r=Path('/tmp/hopper-new-review-20261023');out=Path('/tmp/hopper-deep-review-20261023');inv=json.load(open(r/'inventory.json'))
for sha in ['58d3ffd6c841','bb9830beab57']:
 i=next(x for x in inv if x['sha256'].startswith(sha));p=pefile.PE(i['path']);image=p.get_memory_mapped_image();base=p.OPTIONAL_HEADER.ImageBase;u=Uc(UC_ARCH_X86,UC_MODE_32);u.mem_map(base,(len(image)+4095)&~4095);u.mem_write(base,image);obj=0x60000000;stack=0x70000000;u.mem_map(obj,0x50000);u.mem_map(stack,0x100000);sp=stack+0x80000;u.mem_write(sp,struct.pack('<I',0xdeadbeef));u.reg_write(UC_X86_REG_ESP,sp);u.reg_write(UC_X86_REG_ECX,obj)
 try:u.emu_start(0x401300,0xdeadbeef,count=15000000)
 except UcError as e:raise RuntimeError((sha,str(e),hex(u.reg_read(UC_X86_REG_EIP))))
 assert u.reg_read(UC_X86_REG_EIP)==0xdeadbeef,hex(u.reg_read(UC_X86_REG_EIP))
 table=bytes(u.mem_read(obj,0x40022));(out/(sha+'-tables.bin')).write_bytes(table);key=table[0x20020];data=bytearray((r/'native'/sha/'resource-10-__-0.bin').read_bytes())
 # The caller decodes independent 1024-byte chunks into a second buffer.
 for start in range(0,len(data),1024):
  n=min(1024,len(data)-start)
  for k in range(n-1):data[start+k]=table[((data[start+k]+256)<<8)+data[start+k+1]]
  data[start+n-1]=table[((data[start+n-1]+256)<<8)+(key^0x55)]
  for k in range(n-1,0,-1):data[start+k]=table[((data[start+k]+256)<<8)+data[start+k-1]]
  data[start]=table[((data[start]+256)<<8)+key]
 (out/(sha+'-decoded-resource.bin')).write_bytes(data);print(sha,'decoded',len(data),repr(data[:24]),flush=True)
 # Native wrapper prefixes the zlib stream with the expanded length.
 for at in range(0,24):
  try:
   dec=zlib.decompress(data[at:]);(out/(sha+'-expanded.bin')).write_bytes(dec);print('ZLIB',at,len(dec),repr(dec[:70]),flush=True)
   at=0
   while True:
    at=dec.find(b'MZ',at)
    if at<0:break
    try:
     pe=pefile.PE(data=dec[at:]);size=max(s.PointerToRawData+s.SizeOfRawData for s in pe.sections);f=out/(sha+f'-managed-{at:x}.exe');f.write_bytes(dec[at:at+size]);print('PE',str(f),len(f.read_bytes()),flush=True)
    except:pass
    at+=2
   break
  except zlib.error:pass
