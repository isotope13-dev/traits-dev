import struct,json,re,sys
from pathlib import Path
from capstone import *
B=Path(sys.argv[1]).read_bytes()
key=B[0x15048:0x15068]; nonce=B[0x1503c:0x15048]
def rol(x,n):return ((x<<n)|(x>>(32-n)))&0xffffffff
def block(c):
 s=list(struct.unpack('<4I',b'expand 32-byte k'))+list(struct.unpack('<8I',key))+[c]+list(struct.unpack('<3I',nonce));x=s[:]
 def q(a,b,c,d):
  x[a]=(x[a]+x[b])&0xffffffff;x[d]=rol(x[d]^x[a],16)
  x[c]=(x[c]+x[d])&0xffffffff;x[b]=rol(x[b]^x[c],12)
  x[a]=(x[a]+x[b])&0xffffffff;x[d]=rol(x[d]^x[a],8)
  x[c]=(x[c]+x[d])&0xffffffff;x[b]=rol(x[b]^x[c],7)
 for _ in range(10):
  for p in [(0,4,8,12),(1,5,9,13),(2,6,10,14),(3,7,11,15),(0,5,10,15),(1,6,11,12),(2,7,8,13),(3,4,9,14)]:q(*p)
 return struct.pack('<16I',*[(a+b)&0xffffffff for a,b in zip(x,s)])
def decrypt(b):
 k=b''.join(block(i) for i in range((len(b)+63)//64));return bytes(a^c for a,c in zip(b,k))
md=Cs(CS_ARCH_MIPS,CS_MODE_MIPS32|CS_MODE_LITTLE_ENDIAN)
ins=list(md.disasm(B[0x200:0x750],0x400200));regs={'zero':0}; pending=False;decoded={}
for i in ins:
 p=i.op_str.replace('$','').split(', ');m=i.mnemonic
 try:
  if m=='lui':regs[p[0]]=int(p[1],0)<<16
  elif m=='addiu':regs[p[0]]=(regs.get(p[1],0)+int(p[2],0))&0xffffffff
  elif m=='move':regs[p[0]]=regs.get(p[1],0)
 except ValueError:pass
 if pending:
  idx,addr,size=[regs.get(r) for r in ['a0','a1','a2']]
  if addr and 0x400000<addr<0x415000:
   dec=decrypt(B[addr-0x400000:addr-0x400000+size])
   decoded[idx]={'addr':hex(addr),'size':size,'text':dec.decode('latin1')}
   print(idx,hex(addr),size,repr(dec))
  pending=False
 if m=='jal' and int(p[0],0)==0x404ac0:pending=True
if len(sys.argv)>2: Path(sys.argv[2]).write_text(json.dumps(decoded,indent=2))
print('KEY',key.hex(),'NONCE',nonce.hex())
