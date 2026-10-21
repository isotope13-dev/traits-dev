"""Build inert controls and check emitted findings; never execute a fixture.

Usage: python3 check.py /absolute/path/to/output [cleave]
"""
import json
from pathlib import Path
import struct
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(sys.argv[1]).resolve()
OUT.mkdir(parents=True, exist_ok=True)
CLEAVE = sys.argv[2] if len(sys.argv) > 2 else "cleave"
cases = []
old_cab = {
    "objectives/command-and-control/dropper/cabinet-payload::" + name
    for name in ["cab-extensionless-crowd", "cab-tiny-extensionless"]
} | {
    "objectives/command-and-control/dropper/delivery/cab::" + name
    for name in ["cab-dotnet-exe-dropper", "cab-exe-entry-stub",
                 "cab-extensionless-dropper", "cab-minimal-load-dropper",
                 "cab-stub-exe-dropper"]
}
old_refs = {
    "objectives/command-and-control/dropper/sideload::" + name
    for name in ["office-click2run-mso-sideload-ref", "office-click2run-mso-core-dll-ref",
                 "office-msosync-pdb-path", "office-postc2r-pdb-path"]
} | {"objectives/evasion/masquerade/binary/loader::office-msosync-appendage"}
xor_id = "micro-behaviors/data/encoding/xor::x86-constant-byte-xor-copy-loop"
old_xor = "micro-behaviors/data/decode/xor::x86-constant-byte-xor-copy-loop"
user_id = "micro-behaviors/os/user/lookup::get-user-name"


def pe(code=b"", data=b"", imported=None):
    image = bytearray(0x800)
    image[:2] = b"MZ"
    struct.pack_into("<I", image, 0x3c, 0x80)
    image[0x80:0x84] = b"PE\0\0"
    struct.pack_into("<HHIIIHH", image, 0x84, 0x14c, 2, 0, 0, 0, 224, 0x102)
    opt = 0x98
    struct.pack_into("<H", image, opt, 0x10b)
    struct.pack_into("<III", image, opt + 4, 512, 1024, 0)
    struct.pack_into("<III", image, opt + 16, 0x1000, 0x1000, 0x2000)
    struct.pack_into("<III", image, opt + 28, 0x400000, 0x1000, 512)
    struct.pack_into("<HH", image, opt + 40, 4, 0)
    struct.pack_into("<II", image, opt + 56, 0x3000, 512)
    struct.pack_into("<H", image, opt + 68, 3)
    struct.pack_into("<I", image, opt + 92, 16)
    for i, (name, va, size, offset, flags) in enumerate([
        (b".text", 0x1000, 512, 512, 0x60000020),
        (b".rdata", 0x2000, 1024, 1024, 0x40000040),
    ]):
        struct.pack_into("<8sIIIIIIHHI", image, opt + 224 + i * 40,
                         name, size, va, size, offset, 0, 0, 0, 0, flags)
    # The only entry-point instruction returns. Test sequences are inert data.
    image[0x200:0x201 + len(code)] = b"\xc3" + code
    image[0x500:0x500 + len(data)] = data
    if imported:
        dll, symbol = imported
        struct.pack_into("<II", image, opt + 104, 0x2000, 40)
        struct.pack_into("<5I", image, 0x400, 0x2060, 0, 0, 0x2050, 0x2070)
        image[0x450:0x451 + len(dll)] = dll + b"\0"
        struct.pack_into("<II", image, 0x460, 0x2080, 0)
        struct.pack_into("<II", image, 0x470, 0x2080, 0)
        image[0x482:0x483 + len(symbol)] = symbol + b"\0"
    return bytes(image)


def cab(members):
    table = bytearray()
    data = bytearray()
    for name, contents in members:
        table += struct.pack("<IIHHHH", len(contents), len(data), 0, 0, 0, 0x20)
        table += name.encode() + b"\0"
        data += contents
    start = 44 + len(table)
    header = struct.pack("<4sIIIII BBHHHHH", b"MSCF", 0, start + 8 + len(data),
                         0, 44, 0, 3, 1, 1, len(members), 0, 0, 0)
    return header + struct.pack("<IHH", start, 1, 0) + table + struct.pack(
        "<IHH", 0, len(data), len(data)) + data


def case(name, contents, matched=(), absent=()):
    path = OUT / name
    path.write_bytes(contents)
    cases.append((path, set(matched), set(absent) | old_cab | old_refs | {old_xor}))


debug_ids = {"metadata/binary/debug::" + name for name in [
    "office-msosync-pdb-name-reference", "office-msosync-pdb-path-reference",
    "office-postc2r-pdb-path-reference"]}
library_ids = {"micro-behaviors/fs/path/library::" + name for name in [
    "office-mso-win32client-dll-reference", "office-mso-dll-reference"]}
path = r"F:\Office\Target\ship\postc2r\x-none\msosync.pdb"
case("office-references.fixture", pe(data=b"MSO.dll\0mso20win32client.dll\0\0" +
     path.encode("utf-16le") + b"\0\0"), debug_ids | library_ids)
case("office-near-miss.fixture", pe(data=b"MSO.txt\0mso20win32client.txt\0" +
     path.replace("msosync.pdb", "msosync.txt").encode("utf-16le")), absent=debug_ids | library_ids)
case("username-import.fixture", pe(imported=(b"ADVAPI32.dll", b"GetUserNameW")), [user_id])
case("username-text-only.fixture", pe(data=b"GetUserNameW\0"), absent=[user_id])

down = bytes.fromhex("8A 1C 08 80 F3 42 88 19 41 4A 75 F4")
up = bytes.fromhex("8A 14 01 80 F2 42 47 88 10 40 3B 3E 72 F2")
for name, sequence in [("countdown", down), ("countup", up)]:
    for key in (1, 0x42, 0xff):
        case(f"xor-{name}-{key}.fixture", pe(code=sequence[:5] + bytes([key]) + sequence[6:]), [xor_id])
    case(f"xor-{name}-zero.fixture", pe(code=sequence[:5] + b"\0" + sequence[6:]), absent=[xor_id])
    case(f"xor-{name}-forward.fixture", pe(code=sequence[:-1] + b"\x02"), absent=[xor_id])
case("xor-wrong-store.fixture", pe(code=down.replace(b"\x88\x19", b"\x88\x11")), absent=[xor_id])
case("xor-data-section.fixture", pe(data=down + up), absent=[xor_id])
case("extensionless.cab", cab([("Member" + chr(97 + i), b"abc") for i in range(10)]), [
    "metadata/file/archive::cab-extensionless-member-entry",
    "metadata/file/archive::archive-at-least-10-members"])
case("named-source.cab", cab([(f"source{i}.txt", b"abc") for i in range(10)]), [
    "metadata/file/archive::archive-at-least-10-members"], [
    "metadata/file/archive::cab-extensionless-member-entry"])
case("managed-import.cab", cab([("example.exe", pe(data=b"mscorlib\0",
     imported=(b"mscoree.dll", b"_CorExeMain")))]))
case("export-lookup.cab", cab([("example.exe", pe(
     imported=(b"KERNEL32.dll", b"GetProcAddress")))]))

result = subprocess.run([CLEAVE, "--traits-dir", str(ROOT), "--format", "json",
                         *[str(path) for path, _, _ in cases]],
                        check=True, capture_output=True, text=True)
(OUT / "report.json").write_text(result.stdout)
reports = []
remaining = result.stdout.lstrip()
decoder = json.JSONDecoder()
while remaining:
    report, end = decoder.raw_decode(remaining)
    reports.extend(report["files"])
    remaining = remaining[end:].lstrip()
for path, expected, absent in cases:
    files = [f for f in reports if f["path"] == str(path)]
    assert len(files) == 1, (path.name, "missing root report")
    ids = {t["id"] for t in files[0].get("traits", [])}
    assert expected <= ids, (path.name, "missing", sorted(expected - ids))
    assert not ids & absent, (path.name, "unexpected", sorted(ids & absent))
print(f"Passed {len(cases)} inert PE/CAB controls.")
