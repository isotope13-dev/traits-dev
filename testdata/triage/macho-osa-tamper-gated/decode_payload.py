"""Offline data recovery only. No instructions from the specimen are executed."""
from pathlib import Path
import struct,hashlib,hmac,ctypes,json
ROOT=Path(__file__).resolve().parent
DATA=(ROOT/'arm64.macho').read_bytes()
def read(addr,n):
    offset=addr-0x100000000 if addr>=0x100000000 else addr
    return DATA[offset:offset+n]
def u64(addr):return struct.unpack('<Q',read(addr,8))[0]
def cstring(addr):
    offset=addr-0x100000000
    return DATA[offset:DATA.index(0,offset)]
def xor(a,b,n):return bytes(x^y for x,y in zip(read(a,n),read(b,n)))
def hm(key,data):return hmac.new(key,data,hashlib.sha256).digest()
def hkdf(ikm,salt,info,n):return hm(hm(salt or bytes(32),ikm),info+b'\x01')[:n]
CC=ctypes.CDLL('/usr/lib/system/libcommonCrypto.dylib')
gcm=CC.CCCryptorGCMOneshotDecrypt
gcm.argtypes=[ctypes.c_uint32,ctypes.c_void_p,ctypes.c_size_t,ctypes.c_void_p,ctypes.c_size_t,ctypes.c_void_p,ctypes.c_size_t,ctypes.c_void_p,ctypes.c_size_t,ctypes.c_void_p,ctypes.c_void_p,ctypes.c_size_t]
gcm.restype=ctypes.c_int
def decrypt(key,nonce,ciphertext,tag):
    output=ctypes.create_string_buffer(len(ciphertext))
    status=gcm(0,key,len(key),nonce,len(nonce),None,0,ciphertext,len(ciphertext),output,tag,len(tag))
    if status:raise ValueError('GCM authentication failed: '+str(status))
    return output.raw
TABLE=read(0x10009f058,256)
def b64decode(encoded,size):
    values=[((c*9+0xb5)&255)^TABLE[c] for c in encoded]
    values=[v for v in values if v!=0xca]
    out=bytearray()
    for start in range(0,len(values)-3,4):
        a,b,c,d=values[start:start+4]
        val=(a<<18)|(b<<12)|(c<<6)|d
        out.extend((val&0xffffff).to_bytes(3,'big'))
        if len(out)>=size:return bytes(out[:size])
    raise ValueError('short base64 input')
def decode_chunks(key,infobase,modebase,sizebase,ptrbase,tagbase,count):
    result=bytearray();manifest=[]
    for i in range(count):
        nonce=hkdf(key,b'',infobase+b'\0\0\0'+bytes([i]),12)
        n=u64(sizebase+8*i)
        cipher=b64decode(read(u64(ptrbase+8*i),n*3+128),n)
        plain=decrypt(key,nonce,cipher,read(u64(tagbase+8*i),16))
        mode=read(modebase+i,1)
        manifest.append({'index':i,'mode':mode.hex(),'bytes':n,'sha256':hashlib.sha256(plain).hexdigest()})
        if mode==b'7':result.extend(plain)
    return bytes(result),manifest
def recover_bootstrap():
    seed=xor(0x1000a0010,0x1000a0018,8)
    salt=xor(0x1000a00d4,0x1000a00f4,32)
    key=hkdf(seed,salt,read(0x10009e8c8,18),32)
    bootstrap,manifest=decode_chunks(key,xor(0x1000a0154,0x1000a015e,10),0x10009e8da,0x10009e8e0,0x1001027e0,0x100102808,5)
    (ROOT/'bootstrap.scpt').write_bytes(bootstrap)
    (ROOT/'bootstrap-chunks.json').write_text(json.dumps(manifest,indent=2)+'\n')
    expected=xor(0x1000a05a1,0x1000a05c1,32)
    assert hashlib.sha256(bootstrap).digest()==expected
    print('Authenticated bootstrap:',len(bootstrap),'bytes; SHA-256',hashlib.sha256(bootstrap).hexdigest())

def recover_main():
    # Parse only the on-disk 64-bit Mach-O load-command/section tables.
    assert DATA[:4] == bytes.fromhex('cffaedfe')
    cursor=32; text=None
    for _ in range(struct.unpack_from('<I',DATA,16)[0]):
        command, size=struct.unpack_from('<II',DATA,cursor)
        assert size >= 8 and cursor+size <= len(DATA)
        if command == 0x19:
            count=struct.unpack_from('<I',DATA,cursor+64)[0]
            assert 72+80*count <= size
            for index in range(count):
                section=cursor+72+80*index
                if DATA[section:section+16].rstrip(b'\0') == b'__text':
                    length=struct.unpack_from('<Q',DATA,section+40)[0]
                    offset=struct.unpack_from('<I',DATA,section+48)[0]
                    assert offset+length <= len(DATA)
                    text=DATA[offset:offset+length]
        cursor+=size
    assert text is not None
    digest=hashlib.sha256(text).digest()
    masked=bytes(x^y for x,y in zip(digest,read(0x1000a0034,32)))
    salt=xor(0x1000a0114,0x1000a0134,32)
    seed=int.from_bytes(xor(0x1000a0010,0x1000a0018,8)[:4],'little')
    callback=((0x3db57053*0xe621fe9a)&0xffffffff)^0x314aebee
    n=u64(0x10009e5c0)
    cipher=b64decode(read(u64(0x1001021d0),n*3+128),n)
    tag=read(u64(0x1001024d8),16)
    info=xor(0x1000a0168,0x1000a0175,13)
    for cb in [0,callback,0x276df8ea]:
        word=seed^int.from_bytes(masked[:4],'little')^cb
        password=word.to_bytes(4,'big')+masked
        key=hashlib.pbkdf2_hmac('sha256',password,salt,0x1757e,32)
        nonce=hkdf(key,b'',info+b'\0\0\0\0',12)
        try:first=decrypt(key,nonce,cipher,tag)
        except ValueError:continue
        plain,manifest=decode_chunks(key,info,0x10009e558,0x10009e5c0,0x1001021d0,0x1001024d8,0x61)
        assert len(plain)==0x3fe14
        assert hashlib.sha256(plain).digest()==xor(0x1000a05e1,0x1000a0601,32)
        (ROOT/'payload.scpt').write_bytes(plain)
        (ROOT/'payload-chunks.json').write_text(json.dumps(manifest,indent=2)+'\n')
        (ROOT/'key-recovery.json').write_text(json.dumps({'text_sha256':digest.hex(),'password_hex':password.hex(),'iterations':0x1757e,'callback_result':hex(cb),'key_hex':key.hex(),'payload_sha256':hashlib.sha256(plain).hexdigest()},indent=2)+'\n')
        print('Authenticated payload:',len(plain),'bytes; SHA-256',hashlib.sha256(plain).hexdigest());return
    raise ValueError('No normal-environment key candidate authenticated')

if __name__ == "__main__":
    recover_bootstrap()
    recover_main()
