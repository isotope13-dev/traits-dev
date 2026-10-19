"""Generate inert format fixtures; none of these files is executed."""
import json
import struct
from pathlib import Path

root = Path(__file__).resolve().parent
relative = Path("testdata/taxonomy/native-byte-evidence-review")
cases = []

def elf(name, text=b"", rodata=b"", symbols=b""):
    labels = b"\0.text\0.rodata\0.strtab\0.shstrtab\0"
    b = bytearray(0x9000)
    b[:52] = struct.pack("<16sHHIIIIIHHHHHH",
        b"\x7fELF\x01\x01\x01" + b"\0"*9, 2, 40, 1,
        0, 0, 0xd00, 0, 52, 0, 0, 40, 5, 4)
    sections = [(0,0,0,0,0,0,0,0,0,0)]
    for nm, off, typ, flags, content in [
        (1,0x100,1,6,text), (7,0x400,1,2,rodata),
        (15,0x900,3,0,symbols), (23,0xc00,3,0,labels)]:
        assert len(content) < 0x300
        b[off:off+len(content)] = content
        sections.append((nm,typ,flags,0x8000+off,off,len(content),0,0,4,0))
    for i, row in enumerate(sections):
        struct.pack_into("<10I",b,0xd00+i*40,*row)
    (root/name).write_bytes(b)

def pe(name, text, entry=0x1000):
    b=bytearray(0x400)
    b[:2]=b"MZ";struct.pack_into("<I",b,0x3c,0x80)
    b[0x80:0x84]=b"PE\0\0"
    struct.pack_into("<HHIIIHH",b,0x84,0x14c,1,0,0,0,0xe0,0x102)
    o=0x98
    struct.pack_into("<H",b,o,0x10b)
    struct.pack_into("<I",b,o+16,entry)
    struct.pack_into("<I",b,o+20,0x1000)
    struct.pack_into("<I",b,o+28,0x400000)
    struct.pack_into("<II",b,o+32,0x1000,0x200)
    struct.pack_into("<II",b,o+56,0x2000,0x200)
    struct.pack_into("<H",b,o+68,3)
    struct.pack_into("<I",b,o+92,16)
    struct.pack_into("<8sIIIIIIHHI",b,0x178,b".text\0\0\0",0x200,
        0x1000,0x200,0x200,0,0,0,0,0x60000020)
    b[0x200:0x200+len(text)]=text
    (root/name).write_bytes(b)

def case(name, matched=(), absent=()):
    cases.append({"path":str(relative/name), "matched":list(matched),
                  "not_matched":list(absent)})

network="micro-behaviors/communications/socket/syscall::"
names="metadata/binary/symbols/name::"
mirai="well-known/malware/botnet/mirai/identity::mirai-unstripped-stdhex-bot"
# Real literal loads point exactly to the syscall number 0x38 bytes later.
for name,num in [("socket",281),("connect",283),("send",289),("recv",291),("sendto",290)]:
    code=bytes.fromhex("30 70 9F E5 00 00 00 EF")+b"\0"*48+struct.pack("<I",num)
    elf(name+"-wrapper.elf",text=code)
    case(name+"-wrapper.elf",[network+"arm-"+name+"-literal-syscall-wrapper"])
    # A number present in text without the LDR/SVC relationship is not a syscall.
    elf(name+"-integer.elf",text=b"\0"*8+struct.pack("<I",num))
    case(name+"-integer.elf",absent=[network+"arm-"+name+"-literal-syscall-wrapper"])
elf("wrong-literal-load.elf",text=bytes.fromhex("2C 70 9F E5 00 00 00 EF")+b"\0"*48+struct.pack("<I",290))
case("wrong-literal-load.elf",absent=[network+"arm-sendto-literal-syscall-wrapper"])
syms=b"\0table_unlock_val\0attack_parse\0attack_udp_stdhex\0attack_tcp_stomp\0attack_socket\0attack_ongoing\0"
elf("mirai-symbol-cluster.elf",symbols=syms)
case("mirai-symbol-cluster.elf",[mirai,names+"tcp-bypass-stomp-handler-name",names+"socket-tcpflood-handler-name",names+"attack-ongoing-symbol-name"])
elf("missing-udp-handler.elf",symbols=syms.replace(b"attack_udp_stdhex",b"ordinary_handler"))
case("missing-udp-handler.elf",absent=[mirai])
elf("names-in-prose.elf",rodata=syms)
case("names-in-prose.elf",absent=[mirai,names+"tcp-bypass-stomp-handler-name",names+"socket-tcpflood-handler-name",names+"attack-ongoing-symbol-name"])
elf("kill-log-only.elf",rodata=b"Killed process: %s, PID: %d\0")
case("kill-log-only.elf",["micro-behaviors/process/terminate/kill::killed-process-log"],
     ["objectives/impact/degrade/rival-bot/competitor::multiarch-bot-procfs-rival-killer"])
ssdp=(b'M-SEARCH * HTTP/1.1\r\nHOST: 255.255.255.255:1900\r\nMAN: "ssdp:discover"\r\n'
      b'MX: 1\r\nST: urn:dial-multiscreen-org:service:dial:1\r\n'
      b'USER-AGENT: Google Chrome/60.0.3112.90 Windows\r\n\r\n\0')
elf("ssdp-architecture-references.elf",rodata=ssdp+b"main_x86\0main_mips\0main_arm\0")
case("ssdp-architecture-references.elf",
     ["micro-behaviors/communications/http/request/ssdp::multiarch-ssdp-template-references"],
     ["objectives/impact/dos/amplification::ssdp-amplification-bot"])
skip="objectives/anti-static/obfuscation/control-flow/stack::x86-return-address-junk-skip"
code=bytes.fromhex("50 8B 44 24 04 83 C0 04 50 8B 44 24 04 C2 08 00")
pe("return-skip.exe",code)
case("return-skip.exe",[skip])
pe("return-unchanged.exe",code.replace(bytes.fromhex("83 C0 04"),bytes.fromhex("83 C0 00")))
case("return-unchanged.exe",absent=[skip])
zero="metadata/binary/section/header::pe-entry-region-zeroed"
pe("zero-entry.exe",b"\0"*32)
case("zero-entry.exe",[zero])
pe("entry-byte-31-set.exe",b"\0"*31+b"\x90")
case("entry-byte-31-set.exe",absent=[zero])
pe("unmapped-entry.exe",b"\0"*32,entry=0x3000)
case("unmapped-entry.exe",absent=[zero])
(root/"cases.json").write_text(json.dumps({"id_map":{},"fixtures":cases},indent=2)+"\n")
