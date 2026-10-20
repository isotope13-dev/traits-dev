"""Generate inert PE fixtures rather than storing large padded binaries."""
import struct

def pe(overlay,peb=True,truncated=False):
 d=bytearray(1024+overlay);d[:2]=b'MZ';struct.pack_into('<I',d,0x3c,0x80);d[0x80:0x84]=b'PE\0\0';struct.pack_into('<HHIIIHH',d,0x84,0x14c,1,0,0,0,224,0x102)
 o=0x98;struct.pack_into('<H',d,o,0x10b);struct.pack_into('<IIIIII',d,o+4,512,0,0,0x1000,0x1000,0x2000);struct.pack_into('<III',d,o+28,0x400000,4096,512);struct.pack_into('<HHHHHH',d,o+40,4,0,0,0,4,0);struct.pack_into('<II',d,o+56,0x2000,512);struct.pack_into('<HH',d,o+68,3,0);struct.pack_into('<IIIIII',d,o+72,0x100000,4096,0x100000,4096,0,16)
 sh=o+224;struct.pack_into('<8sIIIIIIHHI',d,sh,b'.text',512,4096,512,512,0,0,0,0,0x60000020)
 d[512:522]=bytes.fromhex('64 A1 30 00 00 00 8B 40 0C C3') if peb else b'\x90'*9+b'\xc3'
 if truncated:struct.pack_into('<II',d,o+96+4*8,len(d)-4,512)
 return d
