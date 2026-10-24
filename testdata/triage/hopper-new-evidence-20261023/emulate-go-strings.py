# Bounded CPU-only emulation. The specimen is never launched, and no host API
# is called: only heap/string primitives are mocked, all OS calls stop a run.
from pathlib import Path
import json,pefile,capstone,struct
from unicorn import Uc,UC_ARCH_X86,UC_MODE_64,UC_HOOK_CODE,UcError
from unicorn.x86_const import *
r=Path('/tmp/hopper-new-review-20261023');inv=json.load(open(r/'inventory.json'))
for sha in ['a58c639a1083','a5d4f63e443a','744f82adda79']:
 i=next(x for x in inv if x['sha256'].startswith(sha));b=Path(i['path']).read_bytes();pe=pefile.PE(data=b);base=pe.OPTIONAL_HEADER.ImageBase;image=pe.get_memory_mapped_image();fs=json.load(open(r/'native'/sha/'go-functions.json'));names={x['va']:x['name'] for x in fs};main=[f for f in fs if f['name'].startswith('main.')];results=[]
 for f in main:
  uc=Uc(UC_ARCH_X86,UC_MODE_64);uc.mem_map(base,(len(image)+4095)&~4095);uc.mem_write(base,image);stack=0x70000000;heap=0x60000000;g=0x50000000;uc.mem_map(stack,0x200000);uc.mem_map(heap,0x400000);uc.mem_map(g,0x10000);rsp=stack+0x100000;uc.reg_write(UC_X86_REG_RSP,rsp);uc.reg_write(UC_X86_REG_R14,g);uc.mem_write(g+0x10,struct.pack('<Q',stack+4096));uc.mem_write(rsp,struct.pack('<Q',0xdeadbeef));cursor=[heap+0x1000];strings=[];stop=[''];steps=[0]
  def alloc(n):
   if n<0 or n>1000000:raise ValueError('allocation budget')
   p=cursor[0];cursor[0]+=(n+31)&~15
   if cursor[0]>heap+0x400000:raise ValueError('heap budget')
   return p
  def ret():
   sp=uc.reg_read(UC_X86_REG_RSP);to=struct.unpack('<Q',uc.mem_read(sp,8))[0];uc.reg_write(UC_X86_REG_RSP,sp+8);uc.reg_write(UC_X86_REG_RIP,to)
  def readtext(p,n):
   if not 0<n<10000:return ''
   try:
    bb=bytes(uc.mem_read(p,n));s=bb.decode('utf-8');return s if sum(c.isprintable() for c in s)>len(s)*.9 else ''
   except:return ''
  def hook(u,at,size,_):
   steps[0]+=1
   if at==0xdeadbeef:stop[0]='returned';u.emu_stop();return
   name=names.get(at)
   if not name or name.startswith('main.'):return
   a=u.reg_read(UC_X86_REG_RAX);bx=u.reg_read(UC_X86_REG_RBX);cx=u.reg_read(UC_X86_REG_RCX)
   try:
    if name.startswith('runtime.print'):ret();return
    if name in ['runtime.makeslice','runtime.newobject','runtime.mallocgc']:
     n=max(bx,cx)*16 if name=='runtime.makeslice' else (a if name=='runtime.mallocgc' else 4096);p=alloc(n);u.reg_write(UC_X86_REG_RAX,p);ret();return
    if name=='runtime.slicebytetostring':
     s=readtext(bx,cx)
     if s:strings.append({'at':hex(at),'text':s})
     u.reg_write(UC_X86_REG_RAX,bx);u.reg_write(UC_X86_REG_RBX,cx);ret();return
    if name=='runtime.stringtoslicebyte':
     bb=bytes(u.mem_read(bx,cx));p=alloc(cx);u.mem_write(p,bb);u.reg_write(UC_X86_REG_RAX,p);u.reg_write(UC_X86_REG_RBX,cx);u.reg_write(UC_X86_REG_RCX,cx);ret();return
    if name=='runtime.memmove':u.mem_write(a,bytes(u.mem_read(bx,cx)));ret();return
    if name=='syscall.LoadLibrary':
     s=readtext(a,bx)
     if s:strings.append({'api':name,'text':s})
     u.reg_write(UC_X86_REG_RAX,0x1234);u.reg_write(UC_X86_REG_RBX,0);u.reg_write(UC_X86_REG_RCX,0);ret();return
    if name.startswith('syscall.'):
     for p,n in [(a,bx),(bx,cx)]:
      s=readtext(p,n)
      if s:strings.append({'at':hex(at),'api':name,'text':s})
     
     if name=='syscall.(*LazyProc).Call':
      for j in range(0,64,8):
       try:
        p,n=struct.unpack('<QQ',u.mem_read(a+j,16));ss=readtext(p,n)
        if ss:strings.append({'api':name,'struct_offset':j,'text':ss})
       except:pass
     stop[0]='OS boundary '+name;u.emu_stop();return
    if name.startswith('runtime.duff') or name.startswith('runtime.memclr'):return
    stop[0]='unmodeled '+name;u.emu_stop()
   except Exception as e:stop[0]=str(e);u.emu_stop()
  uc.hook_add(UC_HOOK_CODE,hook)
  try:uc.emu_start(f['va'],0xdeadbeef,count=250000)
  except UcError as e:stop[0]=str(e)
  
  import re
  for region,size in [(heap,min(cursor[0]-heap,0x400000)),(rsp-0x10000,0x10000)]:
   raw=bytes(uc.mem_read(region,size))
   for m in re.finditer(rb'[\x20-\x7e]{6,}',raw):
    text=m.group().decode()
    if len(text)<500:strings.append({'memory':hex(region+m.start()),'text':text})
   for m in re.finditer(rb'(?:[\x20-\x7e]\0){6,}',raw):
    strings.append({'memory':hex(region+m.start()),'text':m.group().decode('utf-16le')})
  results.append({'function':f,'steps':steps[0],'stop':stop[0],'strings':strings})
 (r/'native'/sha/'emulated-string-boundaries.json').write_text(json.dumps(results,indent=2)+'\n');print(sha,[(x['function']['name'],x['stop'],x['strings']) for x in results if x['strings']],flush=True)
