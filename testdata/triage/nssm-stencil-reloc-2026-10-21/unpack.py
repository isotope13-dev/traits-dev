"""Reproduce the dd80 sample's arithmetic and LZNT1 unpacking.

Usage: python3 unpack.py <dd80-sample> <output-directory>
Requires pefile and unicorn. Emulation stops BEFORE the decoded code is called;
no Windows API, process, file, or network behavior of the payload is executed.
Addresses below are analysis evidence for this specimen, never rule constants.
"""
import hashlib
from pathlib import Path
import struct
import sys
import pefile
import unicorn
from unicorn.x86_const import UC_X86_REG_EIP, UC_X86_REG_ESP

sample = Path(sys.argv[1]).read_bytes()
assert hashlib.sha256(sample).hexdigest() == 'dd80d5d4c5392894a3e0bbd3ea1ac5c044ac8e5fd61635fbe92ce88c984e2370'
out = Path(sys.argv[2]);out.mkdir(parents=True,exist_ok=True)
pe = pefile.PE(data=sample)
u = unicorn.Uc(unicorn.UC_ARCH_X86,unicorn.UC_MODE_32)
u.mem_map(0x400000,0x600000)
u.mem_write(0x400000,pe.get_memory_mapped_image())
u.mem_map(0x10000000,0x100000)
u.reg_write(UC_X86_REG_ESP,0x10080000)
u.emu_start(0x967000,0x9678c1,count=500000)
assert u.reg_read(UC_X86_REG_EIP) == 0x9678c1
memory = u.mem_read(0x400000,0x569000)
(out/'decoded-memory.bin').write_bytes(memory)
blob = memory[0x4da884:0x4da884+0x46110]
payload = bytearray();pos=0
while pos+2 <= len(blob):
    h=int.from_bytes(blob[pos:pos+2],'little');pos+=2
    if h==0:break
    end=pos+(h&0xfff)+1;chunk=blob[pos:end];pos=end
    if not h&0x8000:
        payload.extend(chunk);continue
    decoded=bytearray();i=0
    while i<len(chunk):
        flags=chunk[i];i+=1
        for bit in range(8):
            if i>=len(chunk):break
            if flags&(1<<bit):
                token=int.from_bytes(chunk[i:i+2],'little');i+=2
                mask=0xfff;shift=12;position=len(decoded)-1
                while position>=0x10:mask>>=1;shift-=1;position>>=1
                length=(token&mask)+3;distance=(token>>shift)+1
                for _ in range(length):decoded.append(decoded[-distance])
            else:
                decoded.append(chunk[i]);i+=1
    payload.extend(decoded)
assert len(payload)==404992 and payload[:8]==b'\x89PNG\r\n\x1a\n'
(out/'disguised-payload.bin').write_bytes(payload)
# Analysis-only reconstruction of the custom PNG-shaped PE header. The actual
# loader has a separate parser branch for this format at 0x923b98..0x923f53.
nt=struct.unpack_from('<I',payload,8)[0]
payload[:2]=b'MZ';struct.pack_into('<I',payload,0x3c,nt)
payload[nt:nt+4]=b'PE\0\0'
(out/'reconstructed-payload.exe').write_bytes(payload)
print('Recovered 573440 decoded bytes and a 404992-byte disguised PE.')
