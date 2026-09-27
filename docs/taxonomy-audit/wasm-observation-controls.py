from pathlib import Path
# Generate inert fixtures in a caller-selected directory; never execute modules.
import sys
root=Path(sys.argv[1])
root.mkdir(parents=True, exist_ok=True)
def leb(n):
 out=bytearray()
 while True:
  b=n&127;n>>=7;out.append(b|(128 if n else 0))
  if not n:return bytes(out)
def string(s):
 b=s.encode();return leb(len(b))+b
def section(k,b):return bytes([k])+leb(len(b))+b
names=['go_scheduler','asyncify_start_unwind','__wbindgen_malloc','__wbindgen_free','_emscripten_helper','stackSave']
header=b'\0asm\x01\0\0\0'
base=header+section(1,b'\x01\x60\x00\x00')+section(3,b'\x01\x00')
exports=leb(len(names))+b''.join(string(n)+b'\x00\x00' for n in names)
producer=string('producers')+b'\x01'+string('processed-by')+b'\x01'+string('taxonomy-fixture')+string('1')
(root/'toolchain-export-facts.wasm').write_bytes(base+section(7,exports)+section(10,b'\x01\x02\x00\x0b')+section(0,producer))
(root/'toolchain-names-without-exports.wasm').write_bytes(header+section(0,string('notes')+' '.join(names).encode()))
# One helper export is insufficient for the paired compiler attribution.
one_export=b'\x01'+string('stackSave')+b'\x00\x00'
(root/'single-helper-export.wasm').write_bytes(base+section(7,one_export)+section(10,b'\x01\x02\x00\x0b')+section(0,string('notes')+b'encoding/base64'))
