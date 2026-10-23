import json,pefile,struct,hashlib,hmac,re
from pathlib import Path
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305,AESGCM
row=next(s for s in json.load(open('/tmp/endpoint-review-20261023/inventory.json')) if s['sha256'].startswith('41a562'));p=pefile.PE(row['local_path']);im=p.get_memory_mapped_image();base=p.OPTIONAL_HEADER.ImageBase
secret=b'eb198d9a-2577-42b2-9bf2-a78a13bfa091|4d|f273da607169f21f60e7677d0d0139e59aad9aaee2e54630296a0dbd0709fa3b'
salt=b'zenconnekt-v2|windows|amd64'
outer=HKDF(algorithm=hashes.SHA256(),length=32,salt=salt,info=b'agent-config-chacha20-poly1305-v2').derive(secret)
inner=HKDF(algorithm=hashes.SHA256(),length=32,salt=salt,info=b'agent-config-aes-256-gcm-v2').derive(secret)
seen=set();found=[]
for at in range(0,len(im)-16,8):
 addr,n=struct.unpack_from('<QQ',im,at)
 if not (base<=addr<base+len(im) and 56<=n<=20000 and n%2==0):continue
 blob=im[addr-base:addr-base+n]
 if blob in seen or not re.fullmatch(b'[0-9a-fA-F]+',blob):continue
 seen.add(blob)
 try:
  data=bytes.fromhex(blob.decode());mid=ChaCha20Poly1305(outer).decrypt(data[:12],data[12:],None);plain=AESGCM(inner).decrypt(mid[:12],mid[12:],None)
 except Exception:continue
 found.append({'header_va':hex(base+at),'ciphertext_va':hex(addr),'length':n,'plaintext':plain.decode(errors='replace')});print(found[-1])
result={'method':'HKDF-SHA256 with statically recovered build/tenant/token secret and platform salt; ChaCha20-Poly1305 outer and AES-256-GCM inner authenticated decryption','candidate_strings':len(seen),'decoded':found}
Path('/tmp/endpoint-review-20261023/native/41a5625a68c0/decrypted-config.json').write_text(json.dumps(result,indent=2)+'\n')
# root certificate URL is passed from this raw Go string header by main.main.
a,n=struct.unpack_from('<QQ',im,0x140728b20-base);print('CERT GLOBAL',hex(a),n,im[a-base:a-base+min(n,400)])
