"""Verify malformed INT21 relocation in one hash-checked sample, CPU model only.

Requires Unicorn and Capstone. No native sample execution or interrupt services.
Synthetic COM entry register values are assumptions, not universal DOS defaults.
"""
from pathlib import Path
import json,struct,hashlib,argparse
import unicorn,capstone
from unicorn.x86_const import *
ap=argparse.ArgumentParser(description=__doc__)
ap.add_argument('sample',type=Path)
ap.add_argument('--output',type=Path,required=True)
args=ap.parse_args()
b=args.sample.read_bytes()
assert hashlib.sha256(b).hexdigest()=='0a967cea6e689473893bfb06d740cd9d757b10ceb1183c85f81dc15cc8e8a703' 
def run(old_offset=0x1234,ax=0):
 u=unicorn.Uc(unicorn.UC_ARCH_X86,unicorn.UC_MODE_16);u.mem_map(0,0x100000);seg=0x2000;base=seg*16
 u.mem_write(base+0x100,b);u.mem_write(0x84,struct.pack('<HH',old_offset,0xf000));u.mem_write(base+0xfffe,b'\0\0')
 for r,v in [(UC_X86_REG_CS,seg),(UC_X86_REG_DS,seg),(UC_X86_REG_ES,seg),(UC_X86_REG_SS,seg),(UC_X86_REG_IP,0x100),(UC_X86_REG_SP,0xfffe),(UC_X86_REG_AX,ax),(UC_X86_REG_BX,0),(UC_X86_REG_CX,0xff),(UC_X86_REG_DX,seg),(UC_X86_REG_SI,0x100),(UC_X86_REG_DI,0xfffe),(UC_X86_REG_EFLAGS,0x202)]:u.reg_write(r,v)
 writes=[];count=0;last=[]
 class Stop(Exception):pass
 def code(uc,a,n,user):
  nonlocal count
  count+=1;last.append(hex(a-base))
  if len(writes)==2:raise Stop('two IVT writes observed')
  if a<base or a>=base+0x10000:raise Stop('outside modeled program segment')
  if bytes(uc.mem_read(a,1))==b'\xcd':raise Stop('interrupt boundary')
 def write(uc,access,a,n,value,user):
  if a<0x100:writes.append({'address':hex(a),'size':n,'value':hex(value),'ip':hex(u.reg_read(UC_X86_REG_IP))})
 u.hook_add(unicorn.UC_HOOK_CODE,code);u.hook_add(unicorn.UC_HOOK_MEM_WRITE,write)
 try:u.emu_start(base+0x100,base+0x10000,count=2000,timeout=1000000);reason='budget'
 except Exception as e:reason=str(e)
 off,segment=struct.unpack('<HH',u.mem_read(0x84,4));a=segment*16+off;c=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_16)
 return {'old_offset':hex(old_offset),'initial_ax':hex(ax),'reason':reason,'instructions':count,'writes':writes,'installed':f'{segment:04x}:{off:04x}','installed_bytes':bytes(u.mem_read(a,12)).hex(),'installed_instructions':[f'{i.mnemonic} {i.op_str}' for i in c.disasm(bytes(u.mem_read(a,12)),a)],'declared_copy_length':0x3f,'actual_write_guard_offset':hex(b.index(bytes.fromhex('608bf2ac3de940'))),'last':last[-10:]}
x={'sha256':hashlib.sha256(b).hexdigest(),'model':'CPU-only 16-bit execution; synthetic COM registers and INT21 vector. No interrupts or host I/O are executed.','assumptions':{'CS_DS_ES_SS':'0x2000','SI':'0x100','DI_SP':'0xfffe','BX':'0','CX':'0xff','DF':0},'runs':[run(),run(0x1229),run(0x1234,0xff)]};x['conclusion']='The vector is installed as 0025:0025, four bytes before the apparent handler at copied-body offset 0x29. This verifies malformed relocation, not a working resident infection.'
for n in [0,2]:
 assert x['runs'][n]['installed']=='0025:0025'
 assert [w['address'] for w in x['runs'][n]['writes']]==['0x84','0x86']
 assert x['runs'][n]['installed_bytes'].startswith('f3a4ebd7')
 assert x['runs'][n]['actual_write_guard_offset']=='0x29'
assert len(x['runs'][1]['writes'])==1
assert x['runs'][1]['installed']=='f000:0025'
args.output.write_text(json.dumps(x,indent=2)+'\n')
print('Verified two relocation cases and the old-vector comparison branch; installed target is malformed.')
