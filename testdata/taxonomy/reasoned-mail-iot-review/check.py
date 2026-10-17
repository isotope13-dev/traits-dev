#!/usr/bin/env python3
"""Static rule controls. Construct fixtures; never execute their contents."""
import argparse
import os
from pathlib import Path
import struct
import subprocess
import tempfile


def elf(code, strings):
    names = b"\0.text\0.rodata\0.shstrtab\0"
    text_offset = 0x100
    ro_offset = (text_offset + len(code) + 3) & ~3
    rodata = b"\0".join(s.encode() for s in strings) + b"\0"
    names_offset = ro_offset + len(rodata)
    section_offset = (names_offset + len(names) + 3) & ~3
    header = b"\x7fELF\x01\x01\x01" + b"\0" * 9
    header += struct.pack("<HHIIIIIHHHHHH", 2, 40, 1,
                          0x10100, 0, section_offset, 0x05000000,
                          52, 0, 0, 40, 4, 3)
    data = bytearray(section_offset + 4 * 40)
    data[:len(header)] = header
    data[text_offset:text_offset + len(code)] = code
    data[ro_offset:ro_offset + len(rodata)] = rodata
    data[names_offset:names_offset + len(names)] = names
    sections = [(1, 1, 6, 0x10000 + text_offset, text_offset, len(code), 0, 0, 4, 0),
                (7, 1, 2, 0x10000 + ro_offset, ro_offset, len(rodata), 0, 0, 1, 0),
                (15, 3, 0, 0, names_offset, len(names), 0, 0, 1, 0)]
    for i, values in enumerate(sections, 1):
        struct.pack_into("<10I", data, section_offset + i * 40, *values)
    return data


WRITE = bytes.fromhex("02 30 A0 E1 08 C0 8D E5 01 20 A0 E1 04 C0 8D E5 "
                      "00 10 A0 E1 00 C0 8D E5 04 00 A0 E3 00 00 00 EB")
SIGNAL = bytes.fromhex("04 70 2D E5 25 70 A0 E3 00 00 00 EF 04 70 9D E4")
XOR = bytes.fromhex("82 36 A0 E1 8C 16 2C E0 AC 39 83 E1 02 30 23 E0 "
                    "A1 23 A0 E1 83 2C 82 E1 01 20 22 E0 01 E0 F0 E5 "
                    "A3 33 23 E0 82 C8 22 E0 83 18 A0 E1 A2 17 81 E1 "
                    "0C E0 2E E0 00 00 54 E1 03 20 21 E0 00 E0 C0 E5 EE FF FF 1A")
ARM_RULES = ["micro-behaviors/fs/write/file/descriptor::arm-libc-write-syscall-forwarder",
             "micro-behaviors/process/control/signal::arm-eabi-kill-signal-syscall",
             "micro-behaviors/crypto/symmetric/xor/stream::arm-xorshift64-byte-stream"]
CRON = "objectives/persistence/system/cron/job::native-root-reboot-hidden-stage"
C2 = "objectives/command-and-control/botnet/iot::ping-pong-ddos-mode-elf-bot"
OWNER = "micro-behaviors/fs/proc/socket-owner::tcp-table-pid-fd-inode-paths"
RIVAL = "objectives/impact/degrade/rival-bot/competitor::procfs-bot-name-and-signal-capabilities"
COOKIE = "micro-behaviors/communications/http/cookie-name::cookie-request-header-token"
MAIL = "micro-behaviors/communications/email/access/exchange::python-ews-hidden-zip-capabilities"
UPLOAD = "micro-behaviors/communications/http/upload::python-ews-zip-aes-file-post-capabilities"
FLOW = "micro-behaviors/communications/http/upload::file-http-body-flow"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cleave", default=os.environ.get("CLEAVE", "cleave"))
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[3]
    common = ["/proc/self/exe", "/etc/cron.d/agent", "@reboot root /tmp/.agent\n",
              "/proc/net/tcp", "/proc/%d/fd", "socket:[%d]", "/proc/%s/comm",
              "/proc/%s/cmdline", "mirai", "gafgyt", "kaiten", "kimwolf", "aisuru",
              "PING", "PONG", "45.67.89.123"]
    attack = common + ["tcpbypass", "tlsplus", "tlsplusbypass"]
    code = WRITE + SIGNAL + XOR
    near = bytearray(code)
    near[24] = 3  # SYS_read, not SYS_write.
    near[len(WRITE) + 4] = 20  # SYS_getpid, not SYS_kill.
    near[len(WRITE) + len(SIGNAL) + 7] = 0xE1  # ORR, not xorshift EOR.
    mail = '''import base64, zipfile, requests
from pathlib import Path
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
def collect(endpoint, destination, key, iv):
    operation = '<FindItem xmlns="http://schemas.microsoft.com/exchange/services/2006/messages">'
    reply = requests.post(endpoint, data=operation)
    archive = zipfile.ZipFile('/var/tmp/.backup.zip', 'w')
    archive.writestr('message.eml', base64.b64decode(reply.content))
    archive.close()
    cipher = AES.new(key, AES.MODE_CBC, iv)
    payload = cipher.encrypt(pad(Path('/var/tmp/.backup.zip').read_bytes(), AES.block_size))
    requests.post(destination, data=payload)
'''
    controls = [
        ("capabilities.elf", elf(code, attack), ARM_RULES + [CRON, C2, OWNER, RIVAL], []),
        ("ordinary.elf", elf(near, common), [OWNER], ARM_RULES + [CRON, C2, RIVAL]),
        ("heartbeat.elf", elf(b"\x1e\xff\x2f\xe1", ["PING", "PONG", "45.67.89.123"]), [], [C2]),
        ("request.c", b'char *header = "Cookie: sid=value\\r\\n";\n', [COOKIE], []),
        ("escaped-request.c", b'char *header = "GET / HTTP/1.1\\r\\nCookie: sid=value\\r\\n";\n', [COOKIE], []),
        ("response.c", b'char *header = "HTTP/1.1 302 Found\\r\\nSet-Cookie: sid=value\\r\\n";\n', [], [COOKIE]),
        ("mail.py", mail.encode(), [MAIL, UPLOAD, FLOW], []),
        ("read-only.py", mail.replace("'w')", "'r')").encode(), [FLOW], [MAIL, UPLOAD]),
        ("banner.elf", elf(b"\x1e\xff\x2f\xe1", ["SSH-2.0-dropbear_2022.83", "mozi", "/proc/self/comm"]),
         ["micro-behaviors/communications/ssh/server::dropbear-protocol-banner",
          "micro-behaviors/process/info/name::mozi-process-name-reference",
          "micro-behaviors/fs/proc/info/path::self-comm-or-cmdline-path"],
         ["well-known/app/network/dropbear::server-binary", C2]),
    ]
    with tempfile.TemporaryDirectory(prefix=".mail-iot-controls-", dir=root) as temp:
        for name, data, required, forbidden in controls:
            path = Path(temp) / name
            path.write_bytes(data)
            run = subprocess.run([args.cleave, "--traits-dir", str(root), "test-rules", str(path),
                                  "--rules", ",".join(required + forbidden)],
                                 text=True, capture_output=True, cwd=root)
            if run.returncode:
                raise AssertionError(run.stdout + run.stderr)
            matched = {line.split()[1] for line in run.stdout.splitlines()
                       if line.startswith("MATCHED ")}
            assert set(required) <= matched, (name, "missing", set(required) - matched, run.stdout)
            assert not set(forbidden) & matched, (name, "unexpected", set(forbidden) & matched)
            print(f"PASS {name}")
    print(f"{len(controls)} static controls passed")


if __name__ == "__main__":
    main()
