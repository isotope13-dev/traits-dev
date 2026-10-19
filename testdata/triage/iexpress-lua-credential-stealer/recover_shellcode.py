"""Recover data bytes without invoking Lua, FFI, or shellcode."""
from pathlib import Path
import re,base64,json,hashlib
root=Path(__file__).resolve().parent
s=(root/'loader.lua').read_text()
encoded=re.search(r'local FNJHLNG = "([^"\n]*)"',s)[1]
# Alphabet table is literal-only; no Lua expression is interpreted.
start=s.index('local Ar=')
# Decode decimal literal spelling only in the bounded alphabet-table region.
table=s[start:s.index('function u0Zw356QS2JN',start)]
table=re.sub(r'\\(\d{1,3})',lambda m:chr(int(m[1])),table)
chars=re.findall(r'"([^"\\]*)"',table)
assert len(chars)==250,len(chars)
assert encoded[0]=='|'
index=int(encoded[1],36);assert 0<=index<25
mapping=dict(zip(chars[index*10:index*10+10],'ABCDEFabcd'))
base64_data=''.join(mapping.get(c,c) for c in encoded[2:])[::-1]
rotated=base64.b64decode(base64_data,validate=True)
shift=rotated[0]-128;assert 0<=shift<=93
payload=bytes(33+(c-33+94-shift)%94 if 33<=c<=126 else c for c in rotated[1:])
assert payload[0]==0xe8
(root/'shellcode.bin').write_bytes(payload)
print('Recovered shellcode:',len(payload),hashlib.sha256(payload).hexdigest())
