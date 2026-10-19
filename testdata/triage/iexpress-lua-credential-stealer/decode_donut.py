"""Offline Donut Chaskey-CTR decoding; specimen instructions are never run."""
from pathlib import Path
import struct,json,hashlib
root=Path(__file__).resolve().parent
MASK=0xffffffff
def rol(x,n):return ((x<<n)|(x>>(32-n)))&MASK
def block(key,data):
 k=struct.unpack('<4I',key);w=[a^b for a,b in zip(struct.unpack('<4I',data),k)]
 for _ in range(16):
  w[0]=(w[0]+w[1])&MASK;w[1]=rol(w[1],5)^w[0]
  w[2]=(w[2]+w[3])&MASK;w[3]=rol(w[3],8)^w[2]
  w[2]=(w[2]+w[1])&MASK;w[0]=(rol(w[0],16)+w[3])&MASK
  w[3]=rol(w[3],13)^w[0];w[1]=rol(w[1],7)^w[2];w[2]=rol(w[2],16)
 return struct.pack('<4I',*[a^b for a,b in zip(w,k)])
assert block(bytes.fromhex('5609e9685f58e32940ecec98c522982f'),bytes.fromhex('b8232826fd5e405e69a301a978ea7ad8'))==bytes.fromhex('d5608d4da2bf347babf8772fdfedde07')
def ctr(key,counter,data):
 counter=int.from_bytes(counter,'big');out=bytearray()
 for pos in range(0,len(data),16):
  stream=block(key,counter.to_bytes(16,'big'));out.extend(a^b for a,b in zip(data[pos:pos+16],stream));counter=(counter+1)%2**128
 return bytes(out)
shellcode=(root/'shellcode.bin').read_bytes();assert shellcode[0]==0xe8
length=struct.unpack_from('<I',shellcode,5)[0];assert length==struct.unpack_from('<I',shellcode,1)[0]
instance=shellcode[5:5+length];clear=instance[:572]+ctr(instance[4:20],instance[20:36],instance[572:]);(root/'donut-instance.bin').write_bytes(clear)
print('API count',struct.unpack_from('<I',clear,572)[0]);print('Config strings',[m.decode('ascii','replace') for m in __import__('re').findall(rb'[\x20-\x7e]{6,}',clear[:4500])]);print('MZ offsets',[m.start() for m in __import__('re').finditer(b'MZ',clear)])

module_offset=3424
kind,thread,compression=struct.unpack_from('<3I',clear,module_offset)
assert kind==2 and compression==1
size=struct.unpack_from('<I',clear,module_offset+1316)[0]
payload=clear[module_offset+1320:module_offset+1320+size]
assert len(payload)==size and payload[:2]==b'MZ'
pe_offset=struct.unpack_from('<I',payload,60)[0]
assert payload[pe_offset:pe_offset+4]==b'PE\0\0'
(root/'agenttesla.exe').write_bytes(payload)
print('Recovered managed payload:',size,hashlib.sha256(payload).hexdigest())
