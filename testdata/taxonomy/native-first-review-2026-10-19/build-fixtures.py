"""Generate inert ELF section fixtures for native rule boundaries."""
import json
import struct
from pathlib import Path

root = Path(__file__).resolve().parent
relative = Path('testdata/taxonomy/native-first-review-2026-10-19')
cases = []

def elf(name, machine=40, text=b'', rodata=b''):
    names = b'\0.text\0.rodata\0.shstrtab\0'
    offsets = (0x100, 0x1100, 0x1700)
    header = struct.pack('<16sHHIIIIIHHHHHH',
        b'\x7fELF\x01\x01\x01' + b'\0' * 9, 2, machine, 1,
        0, 0, 0x1800, 0, 52, 0, 0, 40, 4, 3)
    data = bytearray(0x18a0)
    data[:len(header)] = header
    for off, content in zip(offsets, (text, rodata, names)):
        assert len(content) < 0x400
        data[off:off + len(content)] = content
    for index, fields in enumerate([
        (0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        (1, 1, 6, 0x10100, offsets[0], len(text), 0, 0, 4, 0),
        (7, 1, 2, 0x11100, offsets[1], len(rodata), 0, 0, 1, 0),
        (15, 3, 0, 0, offsets[2], len(names), 0, 0, 1, 0),
    ]):
        struct.pack_into('<10I', data, 0x1800 + index * 40, *fields)
    (root / name).write_bytes(data)

def case(name, matched=(), absent=()):
    cases.append({'path': str(relative / name), 'matched': list(matched),
                  'not_matched': list(absent)})

kill = 'micro-behaviors/process/terminate/command::killall'
discord = 'micro-behaviors/os/application/target::discord-client-name-reference'
signal = 'micro-behaviors/process/control/signal::arm-oabi-kill-syscall'
xor = 'micro-behaviors/data/encoding::arm-thumb-bytewise-xor-loop'
aplib = 'micro-behaviors/data/decompress/aplib::x86-aplib-depacker'
crypt = 'micro-behaviors/communications/irc/command::crypt-directional-channel-labels'
encrypted = 'objectives/command-and-control/channel/irc/bot::encrypted-irc-multivector-flood-tasking'
plain = 'objectives/command-and-control/channel/irc/bot::irc-start-flood-commanded-bot-elf'
vshell = 'well-known/malware/backdoor/vshell::vshell-rebased-nps-implant'

(root / 'killall-command.sh').write_text('killall sleep\n')
case('killall-command.sh', [kill])
elf('attack-mode-labels.elf', rodata=b'killall\0[%s] killall done\0discord\0')
case('attack-mode-labels.elf', absent=[kill, discord])
elf('discord-client-path.elf', rodata=b'/home/user/.config/discord/Local Storage\0')
case('discord-client-path.elf', [discord])
elf('kworker-reference.elf', rodata=b'[kworker/0:2]\0')
case('kworker-reference.elf', ['micro-behaviors/process/info/name::bracketed-kworker-name-reference'], [vshell])
elf('arm-signal-wrapper.elf', text=bytes.fromhex('25 00 90 EF'))
case('arm-signal-wrapper.elf', [signal])
loop = bytes.fromhex('19 78 81 F0 77 01 03 F8 01 1B 59 1B 91 42 F7 DB')
elf('arm-xor-loop.elf', text=loop)
case('arm-xor-loop.elf', [xor])
elf('arm-no-xor.elf', text=loop.replace(b'\x81\xf0', b'\x81\xf1'))
case('arm-no-xor.elf', absent=[xor])
code = bytes.fromhex('60 8B 74 24 24 8B 7C 24 28 FC B2 80 8A 06 83 C6 01 88 07 83 C7 01 BB 02 00 00 00 00 D2 75 05 8A 16 46 10 D2 73 E6')
elf('aplib-depacker.elf', machine=3, text=code)
case('aplib-depacker.elf', [aplib])
elf('aplib-wrong-bit-operation.elf', machine=3, text=code.replace(b'\x10\xd2', b'\x30\xd2'))
case('aplib-wrong-bit-operation.elf', absent=[aplib])
irc = b'PRIVMSG %s :%s\0USER %s 0 * :client\0'
labels = b'CRYPT \0\0ircd-tx\0ircd-rx\0'
flood = b'[%s] start_flood: usage: <mode> <ip> <port> [args]\0tcpbypass\0ovhflood\0ovhbypass\0'
elf('encrypted-irc-client.elf', rodata=irc + labels)
case('encrypted-irc-client.elf', [crypt], [encrypted, plain])
elf('encrypted-irc-flood-tasking.elf', rodata=irc + labels + flood)
case('encrypted-irc-flood-tasking.elf', [crypt, encrypted], [plain])
elf('plaintext-irc-flood-tasking.elf', rodata=irc + labels.replace(b'ircd-rx', b'other-r') + flood)
case('plaintext-irc-flood-tasking.elf', [plain], [crypt, encrypted])
(root / 'cases.json').write_text(json.dumps({'id_map': {}, 'fixtures': cases}, indent=2) + '\n')
