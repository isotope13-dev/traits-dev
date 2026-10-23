from pathlib import Path
import json,struct
root=Path('testdata/taxonomy/capability-server-review')
rel=str(root)
base=Path('testdata/taxonomy/native-byte-evidence-review/names-in-prose.elf').read_bytes()
def elf(name,strings):
 b=bytearray(base); data=b'\0'.join(strings)+b'\0';assert len(data)<0x500
 b[0x400:0x900]=bytes(0x500);b[0x400:0x400+len(data)]=data
 struct.pack_into('<I',b,0xd00+2*40+20,len(data));(root/name).write_bytes(b)
def macho(name,strings):
 data=b'\0'.join(strings)+b'\0';b=bytearray(0x200+len(data))
 struct.pack_into('<8I',b,0,0xfeedfacf,0x100000c,0,2,1,152,0,0)
 struct.pack_into('<II16sQQQQiiII',b,32,0x19,152,b'__TEXT',0x100000000,len(b),0,len(b),7,5,1,0)
 struct.pack_into('<16s16sQQIIIIIIII',b,104,b'__cstring',b'__TEXT',0x100000200,len(data),0x200,0,0,0,2,0,0,0)
 b[0x200:]=data;(root/name).write_bytes(b)
D='micro-behaviors/process/info/name::daemon-helper-name-token'
H='micro-behaviors/os/service/daemon::httpd-name'
A='micro-behaviors/os/service/daemon::apache2-name-reference'
B='micro-behaviors/communications/http/auth::basic-realm-challenge'
P='micro-behaviors/os/security/auth/password::password-dictionary-file-reference'
G='micro-behaviors/data/parse/payment::managed-gateway-private-key-field'
C='objectives/credential-access/cracking/password::remote-service-dictionary-password-cracking'
M='objectives/evasion/masquerade/process/system-name::daemon-helper-name-masquerade'
cases=[]
def case(n,p=(),a=()):cases.append({'path':rel+'/'+n,'present':list(p),'absent':list(a)})
elf('http-vocabulary.elf',[b'application/x-httpd-php',b'agealt-svc',b'Basic realm="test"']);case('http-vocabulary.elf',[B],[D,H,A])
elf('daemon-names.elf',[b'/usr/sbin/httpd',b'apache2.service',b'system-helper']);case('daemon-names.elf',[D,H,A],[M])
elf('helper-masquerade.elf',[b'system-helper',b'Description=System Helper Service']);case('helper-masquerade.elf',[D,M])
macho('auth-config.macho',[b'Invalid user-password dictionary file: invalid format.',b'connect_private_keyconnect_certificatesearch_dirsgateway',b'Basic realm="test"']);case('auth-config.macho',[P,B],[G,C])
macho('online-cracking.macho',[b'Uses POP3 protocol to crack passwords.',b'Uses FTP protocol to crack passwords.',b'username dictionary file',b'password dictionary file',b'login attempts per series',b'_MethodsAndProperties.TCPCrackingInit',b'_MethodsAndProperties.WFCracking']);case('online-cracking.macho',[P,C])
cases.append({'path':'testdata/hostile/braintree-net-nuget-typosquat.nupkg.xz','present':['objectives/credential-access/financial/account::dotnet-gateway-credential-exfil',G],'absent':[]})
for name, content, yes in [
 ('conpty-reference.js', 'const note = "ConPTY delegates terminal hosting to conhost.exe.";\n', True),
 ('conhost-only.js', 'const note = "conhost.exe is a Windows executable.";\n', False)]:
 (root/name).write_text(content)
 ident='micro-behaviors/process/tty/pty::conpty-conhost-reference'
 case(name,[ident] if yes else [],[] if yes else [ident])
(root/'cases.json').write_text(json.dumps(cases,indent=2)+'\n')
