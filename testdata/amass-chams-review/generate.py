"""Generate inert PE controls for Chams labels versus hyphenated place names."""
from pathlib import Path
import struct

HERE = Path(__file__).parent


def pe(strings):
    raw = bytearray(0x800)
    raw[:2] = b"MZ"
    struct.pack_into("<I", raw, 60, 128)
    raw[128:132] = b"PE\0\0"
    struct.pack_into("<HHIIIHH", raw, 132, 0x8664, 2, 0, 0, 0, 240, 0x22)
    opt = 152
    struct.pack_into("<H", raw, opt, 0x20B)
    struct.pack_into("<I", raw, opt + 16, 0x1000)
    struct.pack_into("<Q", raw, opt + 24, 0x140000000)
    struct.pack_into("<II", raw, opt + 32, 0x1000, 512)
    struct.pack_into("<II", raw, opt + 56, 0x3000, 512)
    struct.pack_into("<H", raw, opt + 68, 3)
    struct.pack_into("<I", raw, opt + 108, 16)
    for index, (name, rva, start, size, flags) in enumerate([
        (b".text", 0x1000, 0x200, 0x200, 0x60000020),
        (b".rdata", 0x2000, 0x400, 0x400, 0x40000040),
    ]):
        at = 392 + index * 40
        raw[at:at + 8] = name.ljust(8, b"\0")
        struct.pack_into("<IIII", raw, at + 8, size, rva, size, start)
        struct.pack_into("<I", raw, at + 36, flags)
    raw[0x200] = 0xC3
    data = b"\0".join(s.encode() for s in strings) + b"\0"
    assert len(data) <= 0x400
    raw[0x400:0x400 + len(data)] = data
    return raw


cases = {
    "country": ["Munizip an-Nuqat al-Chams"],
    "country-uppercase": ["MUNIZIP AN-NUQAT AL-CHAMS"],
    "unrelated-word": ["chamstone"],
    "chams-label": ["Chams"],
    "chams-mode": ["CHAMS V1", "chams mode"],
    "qualified-chams": ["esp.chams"],
    "hyphenated-chams": ["Enemy-Chams"],
    "wallhack": ["Wallhack"],
    "ghost-hack": ["Ghost Hack - Enable !"],
    "country-and-control": ["Munizip an-Nuqat al-Chams", "Chams"],
    "sql-index": ["idx_ipnetrecord_start_address", "idx_otherrecord_start_address"],
    "rd-commands": ["rd_start: first", "rd_start: second", "rd_block: first", "rd_block: second"],
    "shutdown-symbol": ["shutdownRemainingLocked-range1"],
    "shutdown-command": ["shutdown -r -t 0 -f"],
    "postgres-method": ["*postgres.execJob"],
    "postgres-program": ["postgres.exe"],
    "session-auth": ["session auth"],
    "cv-token-population": ["babababababababa"] * 12,
    "projectdiscovery-endpoint": ["https://dns.projectdiscovery.io/dns/"],
    "dns-exchange": ["github.com/miekg/dns.(*Client).ExchangeWithConnContext"],
    "dns-unrelated-exchange": ["example.org/client.(*Client).ExchangeWithConnContext"],
}
for name, strings in cases.items():
    category = "hostile" if name in {
        "chams-label", "chams-mode", "qualified-chams", "hyphenated-chams", "wallhack",
        "ghost-hack", "country-and-control",
    } else "benign"
    dest = HERE.parent / category / HERE.name
    dest.mkdir(parents=True, exist_ok=True)
    (dest / (name + ".exe")).write_bytes(pe(strings))
