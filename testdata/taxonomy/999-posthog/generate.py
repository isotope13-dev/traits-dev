"""Small, non-runnable PE layouts and source controls for static matchers."""
from pathlib import Path
import struct,json
p=Path(__file__).parent

def pe(name,code,section=b'.text'):
    raw_size=(len(code)+511)&~511
    b=bytearray(512+raw_size);b[:2]=b'MZ';struct.pack_into('<I',b,0x3c,0x80)
    b[0x80:0x84]=b'PE\0\0';struct.pack_into('<HHIIIHH',b,0x84,0x8664,1,0,0,0,0xf0,0x22)
    o=0x98;struct.pack_into('<H',b,o,0x20b);struct.pack_into('<I',b,o+16,0x1000)
    struct.pack_into('<Q',b,o+24,0x140000000);struct.pack_into('<II',b,o+32,0x1000,0x200)
    struct.pack_into('<II',b,o+56,0x1000+((len(code)+4095)&~4095),512)
    struct.pack_into('<HH',b,o+68,3,0x160);struct.pack_into('<I',b,o+108,16)
    struct.pack_into('<8sIIIIIIHHI',b,0x188,section,len(code),0x1000,raw_size,512,0,0,0,0,0x60000020)
    b[512:512+len(code)]=code;(p/name).write_bytes(b)
# Same instruction forms as the traced loader; a different key and section
# prove neither build-specific constants nor the collector's filename gate it.
dec=bytes.fromhex('41 8b c8 b8 78 56 34 12 d3 c0 80 ff 25 41 02 c0 40 f6 c6 20 41 32 04 11 88 02')
exp=bytes.fromhex('48 63 41 3c 81 3c 08 50 45 00 00 e9 00 00 00 00 0f 85 bf ff ff ff 44 8b 8c 08 88 00 00 00')
pe('rotating-exports.exe',dec+b'\x90'*64+exp,b'.code')
pe('xor-only.exe',dec)
pe('export-only.exe',exp)
pe('wrong-directory.exe',dec+b'\x90'*64+exp.replace(bytes.fromhex('88 00 00 00'),bytes.fromhex('98 00 00 00')))
pe('no-xor.exe',dec.replace(bytes.fromhex('41 32 04 11'),bytes.fromhex('41 02 04 11'))+b'\x90'*64+exp)
pe('distant.exe',dec+b'\x90'*4096+exp)
pe('label-only.exe',b'\xc3'*8,b'.enigma1')
(p/'node-positive.ts').write_text("import { platform, release } from 'node:os'\nimport { gzip } from 'node:zlib'\nimport { promisify } from 'node:util'\nconst compress = promisify(gzip)\nexport const run = (x: string) => [platform(), release(), compress(x)]\n")
(p/'node-names-only.ts').write_text("const platform=()=>1, release=()=>2, gzip=()=>3, promisify=(f:Function)=>f; platform(); release(); promisify(gzip);\n")
(p/'node-imports-only.ts').write_text("import { platform, release } from 'node:os'; import { gzip } from 'node:zlib'; import { promisify } from 'node:util'; export { platform, release, gzip, promisify };\n")
(p/'node-comments.ts').write_text("// import { platform, release } from 'node:os'; platform(); release();\n// import { gzip } from 'node:zlib'; import { promisify } from 'node:util'; promisify(gzip);\nexport const description = 'platform(); release(); promisify(gzip)';\n")
(p/'posthog-client.ts').write_text("const client = new PostHog('key', {host:'https://us.i.posthog.com'}); client.capture({distinctId:'user',event:'click',properties:{}});\n")
(p/'posthog-host-only.ts').write_text("export const endpoint = 'https://us.i.posthog.com'\n")
