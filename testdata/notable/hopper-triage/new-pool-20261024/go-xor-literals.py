"""Bounded constant propagation over literal setup code; does not execute input.
Decoded strings are candidates until a caller/data-flow review establishes use.
"""
from pathlib import Path
import json,struct,re
import pefile,capstone
from capstone.x86 import *
p=Path('/tmp/triage-new-20261024');inv=json.load(open(p/'inventory.json'))
for index in (48,):
 pe=pefile.PE(inv[index]['path']);base=pe.OPTIONAL_HEADER.ImageBase;funcs=json.load(open(p/f'go-symbols/{index}-functions.json'));names={f['address']:f['name'] for f in funcs};decoder=next(f['address'] for f in funcs if f['name']=='main.nMJTW');cs=capstone.Cs(capstone.CS_ARCH_X86,capstone.CS_MODE_64);cs.detail=True;results=[];heap=0x700000000000;mem={}
 def read(at,n):
  if n<0 or n>8192:return None
  if all(at+i in mem for i in range(n)):return bytes(mem[at+i] for i in range(n))
  if base<=at<base+pe.OPTIONAL_HEADER.SizeOfImage:
   try:return pe.get_data(at-base,n)
   except:return None
 def alloc(data):
  global heap
  at=heap;heap+=len(data)+32
  for j,b in enumerate(data):mem[at+j]=b
  return at
 def canonical(name):
  if name in ('al','ax','eax'):return 'rax'
  if name in ('bl','bx','ebx'):return 'rbx'
  if name in ('cl','cx','ecx'):return 'rcx'
  if name in ('dl','dx','edx'):return 'rdx'
  if name in ('sil','si','esi'):return 'rsi'
  if name in ('dil','di','edi'):return 'rdi'
  if name in ('esp','sp'):return 'rsp'
  if name in ('ebp','bp'):return 'rbp'
  return re.sub(r'(r\d+)[bdw]$',r'\1',name)
 for f in funcs:
  if not f['name'].startswith('main.') or f['address']==decoder:continue
  regs={'rsp':0x500000000000,'rbp':0x500000000000};mem={};code=pe.get_data(f['address']-base,min(f['size'],1000000))
  def val(op):
   if op.type==X86_OP_IMM:return op.imm
   if op.type==X86_OP_REG:return regs.get(canonical(cs.reg_name(op.reg)))
   if op.type==X86_OP_MEM:
    a=addr(op);b=read(a,op.size) if a is not None else None;return int.from_bytes(b,'little') if b is not None else None
  def addr(op):
   m=op.mem
   a=ins.address+ins.size if m.base==X86_REG_RIP else regs.get(canonical(cs.reg_name(m.base)),0) if m.base else 0
   v=regs.get(canonical(cs.reg_name(m.index)),0) if m.index else 0
   return a+v*m.scale+m.disp if a is not None and v is not None else None
  def put(op,v):
   if op.type==X86_OP_REG:
    name=canonical(cs.reg_name(op.reg));regs[name]=v & ((1<<(8*op.size))-1) if v is not None else None
   elif op.type==X86_OP_MEM:
    a=addr(op)
    if a is not None and v is not None:
     for j,b in enumerate((v & ((1<<(8*op.size))-1)).to_bytes(op.size,'little')):mem[a+j]=b
  for ins in cs.disasm(code,f['address']):
   ops=ins.operands
   if ins.mnemonic in ('mov','movabs','movzx','movsxd') and len(ops)==2:put(ops[0],val(ops[1]))
   elif ins.mnemonic=='lea' and len(ops)==2:put(ops[0],addr(ops[1]))
   elif ins.mnemonic in ('xor','sub','add','and','or') and len(ops)==2:
    a,b=val(ops[0]),val(ops[1]);v=None
    if ins.mnemonic=='xor' and ops[0].type==ops[1].type==X86_OP_REG and ops[0].reg==ops[1].reg:v=0
    elif a is not None and b is not None:v={'xor':lambda:a^b,'sub':lambda:a-b,'add':lambda:a+b,'and':lambda:a&b,'or':lambda:a|b}[ins.mnemonic]()
    put(ops[0],v)
   elif ins.mnemonic in ('movups','pxor','xorps') and len(ops)==2:
    if ins.mnemonic=='movups' and ops[1].type==X86_OP_REG and cs.reg_name(ops[1].reg)=='xmm15':put(ops[0],0)
   elif ins.mnemonic=='call':
    target=ops[0].imm if ops and ops[0].type==X86_OP_IMM else None;name=names.get(target,'');data=None;kind=''
    if target and any(x['address']<=target<x['address']+x['size'] and x['name'].startswith('runtime.duffzero') for x in funcs):continue
    if target==decoder:
     at,n,key=regs.get('rax'),regs.get('rbx'),regs.get('rdi')
     if at is not None and n is not None and key is not None:
      raw=read(at,n)
      if raw is not None:data=bytes(x^(key&255) for x in raw);kind='xor'
    elif name.startswith('runtime.concatstring'):
     count=name[-1] if name[-1:].isdigit() else None;pieces=[]
     if count:
      params=['rbx','rcx','rdi','rsi','r8','r9','r10','r11','r12','r13']
      for j in range(int(count)):
       at,n=regs.get(params[j*2]),regs.get(params[j*2+1])
       if j==4:
        raw=read(regs['rsp'],16);at,n=struct.unpack('<QQ',raw) if raw is not None else (None,None)
       v=read(at,n) if at is not None and n is not None else None
       if v is None:pieces=None;break
       pieces.append(v)
     else:
      at,n=regs.get('rbx'),regs.get('rcx')
      if at is not None and n is not None and n<=50:
       for j in range(n):
        raw=read(at+j*16,16)
        if raw is None:pieces=None;break
        a,z=struct.unpack('<QQ',raw);v=read(a,z)
        if v is None:pieces=None;break
        pieces.append(v)
      else:pieces=None
     if pieces:data=b''.join(pieces);kind='concat'
    if data is not None:
     results.append({'function':f['name'],'site':hex(ins.address),'kind':kind,'text':data.decode('utf-8',errors='replace')});regs['rax']=alloc(data);regs['rbx']=len(data)
    else:
     for r in ('rax','rbx','rcx','rdi','rsi','r8','r9','r10','r11'):regs[r]=None
 (p/f'go-symbols/{index}-decoded-literals.json').write_text(json.dumps(results,indent=2));print(index,'candidates',len(results))
 print('\n'.join(r['text'] for r in results if len(r['text'])>8 and r['kind']=='concat')[:12000])
