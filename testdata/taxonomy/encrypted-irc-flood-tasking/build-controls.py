"""Generate inert ELF string-table controls; none contains executable code."""
from pathlib import Path
import struct

root = Path(__file__).parent
irc = b'PRIVMSG #channel :%s\0USER %s 0 * :client\0'
crypt = b'handshake ok, crypt active\0'
flood = (b'[%s] start_flood: usage: <mode> <ip> <port> [args]\0'
         b'tcpbypass\0ovhflood\0udp_legit\0udpcustom\0raw socket failed\0')

def elf(name, payload):
    names = b'\0.rodata\0.shstrtab\0'
    name_offset = 4096 + len(payload)
    section_offset = (name_offset + len(names) + 7) & ~7
    header = struct.pack('<16sHHIQQQIHHHHHH',
                         b'\x7fELF\x02\x01\x01' + bytes(9), 2, 62, 1,
                         0, 0, section_offset, 0, 64, 0, 0, 64, 3, 2)
    data = header.ljust(4096, b'\0') + payload + names
    data = data.ljust(section_offset, b'\0') + bytes(64)
    data += struct.pack('<IIQQQQIIQQ', 1, 1, 2, 0x401000, 4096,
                        len(payload), 0, 0, 1, 0)
    data += struct.pack('<IIQQQQIIQQ', 9, 3, 0, 0, name_offset,
                        len(names), 0, 0, 1, 0)
    (root / name).write_bytes(data)

elf('encrypted-irc-client.elf', irc + crypt)
elf('flood-without-irc.elf', flood + crypt)
elf('plaintext-irc-flood.elf', irc + flood)
elf('encrypted-irc-flood.elf', irc + crypt + flood)
(root / 'hidden-service.zig').write_text('const path = "/etc/systemd/system/.agent.service";\n')
(root / 'ordinary-service.zig').write_text('const path = "/etc/systemd/system/agent.service";\n')

def arm_wrapper(name, code):
    names = b'\0.text\0.shstrtab\0'
    name_offset = 4096 + len(code)
    section_offset = (name_offset + len(names) + 3) & ~3
    header = struct.pack('<16sHHIIIIIHHHHHH',
                         b'\x7fELF\x01\x01\x01' + bytes(9), 2, 40, 1,
                         0, 0, section_offset, 0x5000000, 52, 0, 0, 40, 3, 2)
    data = header.ljust(4096, b'\0') + code + names
    data = data.ljust(section_offset, b'\0') + bytes(40)
    data += struct.pack('<IIIIIIIIII', 1, 1, 6, 0x9000, 4096,
                        len(code), 0, 0, 4, 0)
    data += struct.pack('<IIIIIIIIII', 7, 3, 0, 0, name_offset,
                        len(names), 0, 0, 1, 0)
    (root / name).write_bytes(data)

arm_wrapper('dup2-wrapper.elf', bytes.fromhex('3f70a0e3000000ef1eff2fe1'))
arm_wrapper('execve-wrapper.elf', bytes.fromhex('0b70a0e3000000ef1eff2fe1'))
