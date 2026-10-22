#!/usr/bin/env python3
"""Independent ELF fixtures for operand-resolved encrypted-table rules.
Run: uv run --with pyyaml --with yara-python python check.py
No specimen, external URL, native execution or committed binary is needed.
"""
from pathlib import Path
import random
import struct
import yaml
import yara

ROOT = Path(__file__).resolve().parents[3]
SOURCES = {
    "commands": "objectives/command-and-control/botnet/dispatch/xor-table-protocol.yaml",
    "cron": "micro-behaviors/os/service/config/xor-cron-template.yaml",
    "systemd": "micro-behaviors/os/service/config/xor-systemd-template.yaml",
    "antivirus": "micro-behaviors/os/service/stop/xor-security-template.yaml",
    "flood": "objectives/impact/dos/multi-vector/xor-mode-table.yaml",
}
RECORDS = [
    b"!ATK ", b"!EXEC ", b"EXECR %s",
    b"*/5 * * * * root %s %s >/dev/null 2>&1",
    b"[Unit]\nDescription=%s\nAfter=network-online.target\n\n[Service]",
    b"systemctl stop %s 2>/dev/null; systemctl disable %s",
    b"/usr/bin/clamscan", b"/usr/bin/chkrootkit",
    b"udpboom", b"tcpbypass", b"udppps",
]


def fixture(records, key, seed=0, rodata_offset=1024, stride=128):
    """Build inert ELF bytes, with separate code/data sections and valid operands."""
    records = list(records)
    random.Random(seed).shuffle(records)
    base, text_offset = 0x09000000, 512
    lengths = rodata_offset
    key_offset = lengths + len(records) + 19
    table = key_offset + len(key) + 23
    data_end = table + stride * len(records)
    names = b"\0.text\0.rodata\0.shstrtab\0"
    names_offset = data_end
    shoff = (names_offset + len(names) + 3) & ~3
    buf = bytearray(shoff + 4 * 40)
    buf[:16] = b"\x7fELF\x01\x01\x01" + bytes(9)
    struct.pack_into("<HHIIIIIHHHHHH", buf, 16,
                     2, 3, 1, base + text_offset, 52, shoff, 0,
                     52, 32, 1, 40, 4, 3)
    struct.pack_into("<IIIIIIII", buf, 52,
                     1, 0, base, base, len(buf), len(buf), 5, 4096)
    prefix = (b"\x81\xfe" + struct.pack("<I", len(records)-1) +
              b"\x77\x6b\x80\xbe" + struct.pack("<I", base+data_end+4096) +
              b"\x00\x75\x57")
    decoder = bytearray.fromhex(
        "0f b6 be 00 00 00 00 31 d2 eb 00 69 c6 00 00 00 00 "
        "b9 00 00 00 00 89 45 ec 89 d0 31 d2 f7 f1 8a 82 00 00 00 00 "
        "8b 55 ec 32 84 13 00 00 00 00 88 84 13 00 00 00 00")
    for offset, value in ((3, base+lengths), (13, stride), (18, len(key)),
                          (33, base+key_offset), (43, base+table-1),
                          (50, base+data_end+8192)):
        struct.pack_into("<I", decoder, offset, value)
    code = prefix + decoder + b"\xc3"
    buf[text_offset:text_offset+len(code)] = code
    for i, record in enumerate(records):
        assert len(record) <= min(255, stride)
        buf[lengths+i] = len(record)
        start = table+i*stride
        buf[start:start+len(record)] = bytes(c ^ key[j % len(key)]
                                           for j, c in enumerate(record))
    buf[key_offset:key_offset+len(key)] = key
    buf[names_offset:names_offset+len(names)] = names
    for i, args in enumerate([
        (1, 1, 6, base+text_offset, text_offset, len(code), 0, 0, 16, 0),
        (7, 1, 2, base+rodata_offset, rodata_offset,
         data_end-rodata_offset, 0, 0, 1, 0),
        (15, 3, 0, 0, names_offset, len(names), 0, 0, 1, 0),
    ], 1):
        struct.pack_into("<IIIIIIIIII", buf, shoff+i*40, *args)
    return bytes(buf)


def main():
    rules = {}
    for name, path in SOURCES.items():
        doc = yaml.safe_load((ROOT / path).read_text())
        rules[name] = yara.compile(source=doc["traits"][0]["if"]["source"])
    cases = [
        ("original-configuration", RECORDS, b"ordinary-key-24-bytes!!!!", 0, 1024, set(rules)),
        ("new-key-order-and-location", RECORDS, bytes(range(1, 18)), 47, 2048, set(rules)),
        ("no-shell-task", [s for s in RECORDS if s != b"!EXEC "],
         b"key-two", 3, 1536, set(rules)-{"commands"}),
        ("benign-config-same-decoder", [b"local setting", b"display preference"],
         b"preferences", 5, 1024, set()),
        ("task-prefix-near-miss", [b"!ATK ", b"!EXE ", b"EXECR %s"],
         b"preferences", 4, 1024, set()),
    ]
    for label, records, key, seed, offset, expected in cases:
        data = fixture(records, key, seed, offset)
        matches = {name for name, rule in rules.items() if rule.match(data=data)}
        assert matches == expected, (label, matches, expected)
        print(label, sorted(matches))


if __name__ == "__main__":
    main()
