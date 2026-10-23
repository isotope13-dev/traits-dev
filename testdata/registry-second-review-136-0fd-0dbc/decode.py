#!/usr/bin/env python3
"""Offline RC4 recovery derived from the specimen disassembly; never executes it."""
from pathlib import Path
import sys, hashlib
b=Path(sys.argv[1]).read_bytes()
assert hashlib.sha256(b).hexdigest() == 'ba14cfe19a51a168813ee1d2bd2e57a8d2aeffa7721575772b6718114df778f3'
d=bytearray(b[0x30c0:0x30c0+0x10da]); s=list(range(256)); i=j=k=0

def key(data):
 global i,k
 while len(data)>0:
  while True:
   t=s[i]; k=(k+t+data[i%len(data)])%256; s[i]=s[k]; s[k]=t; i=(i+1)%256
   if i==0: break
  data=data[256:]

def arc(off,n):
 global i,j
 for z in range(off,off+n):
  i=(i+1)%256; t=s[i]; j=(j+t)%256; s[i]=s[j]; s[j]=t; d[z]^=s[(t+s[i])%256]
 print(hex(off),n,repr(bytes(d[off:off+n])) if n<300 else 'payload')
 return bytes(d[off:off+n])
key(d[0x56:0x56+256])
arc(0x18f,65);arc(0x1ee,1);arc(1,10);arc(0x10ab,3);arc(0x10af,15);arc(0x10bf,1)
t=arc(0x10c2,22);key(t);a=arc(0x1d3,22);assert a==t
arc(0xf,19)
relax=arc(0x185,1)
if relax==b'\0': raise RuntimeError('file metadata key required')
arc(0x1ed,1);payload=arc(0x397,0xc93)
t=arc(0x1094,19);key(t);a=arc(0x172,19);assert a==t
Path(sys.argv[2]).write_bytes(payload.rstrip(b'\0'))
print(payload.decode())
