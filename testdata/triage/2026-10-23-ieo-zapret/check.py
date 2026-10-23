"""Focused controls for concealed APIs, guest lists, and command precision.

Generated PE files are inert carriers. Existing disk-wiper fixtures exercise
retained attack coverage; actual sample/upstream comparisons are in review.json.
Run: python3 check.py --output /absolute/scratch/directory
"""
import argparse
import json
from pathlib import Path
import struct
import subprocess
import zlib

REPO = Path(__file__).resolve().parents[3]
API = "objectives/anti-static/obfuscation/imports/concealment::xor-section-apc-api-names"
VM = "objectives/anti-analysis/vm-detect/artifact::xor-vm-guest-artifact-list"
DD = "micro-behaviors/fs/write/file/redirect::shell-dd-file-write"
MTR = "micro-behaviors/communications/icmp/trace::mtr-binary-command"
OPTION = "micro-behaviors/process/argument/option::scan-host-file-option"
ARCHIVE = "metadata/file/archive::rar-large-member-with-code-member"


def pe(data, section=b".data"):
    size = (len(data) + 511) & ~511
    b = bytearray(1024 + size)
    b[:2] = b"MZ"
    struct.pack_into("<I", b, 0x3C, 0x80)
    b[0x80:0x84] = b"PE\0\0"
    struct.pack_into("<HHIIIHH", b, 0x84, 0x8664, 2, 0, 0, 0, 240, 0x22)
    o = 0x98
    struct.pack_into("<H", b, o, 0x20B)
    struct.pack_into("<I", b, o + 16, 0x1000)
    struct.pack_into("<Q", b, o + 24, 0x140000000)
    struct.pack_into("<II", b, o + 32, 0x1000, 512)
    struct.pack_into("<II", b, o + 56, 0x2000 + ((size + 4095) & ~4095), 512)
    struct.pack_into("<H", b, o + 68, 3)
    struct.pack_into("<I", b, o + 108, 16)
    for off, name, va, raw, count, flags in [
        (0x188, b".text", 0x1000, 512, 512, 0x60000020),
        (0x1B0, section, 0x2000, 1024, size, 0xC0000040),
    ]:
        struct.pack_into("<8sIIIIIIHHI", b, off, name, count, va, count, raw, 0, 0, 0, 0, flags)
    b[512] = 0xC3
    b[1024:1024 + len(data)] = data
    return bytes(b)


def xor(text, key):
    return bytes([key]) + bytes(x ^ key for x in text.encode()) + b"\0"


def rar_header(kind, flags, data):
    b = struct.pack("<BHH", kind, flags, 7 + len(data)) + data
    return struct.pack("<H", zlib.crc32(b) & 0xFFFF) + b


def rar(members):
    b = b"Rar!\x1a\x07\0" + rar_header(0x73, 0, b"\0" * 6)
    for name, data in members:
        name = name.encode()
        h = struct.pack("<IIBIIBBHI", len(data), len(data), 3,
                        zlib.crc32(data), 0, 20, 0x30, len(name), 0x20)
        b += rar_header(0x74, 0x8000, h + name) + data
    return b + rar_header(0x7B, 0, b"")


def scan(paths):
    r = subprocess.run(["cleave", "--traits-dir", str(REPO), "--format", "json", *map(str, paths)],
                       check=True, capture_output=True, text=True)
    if "Failed to initialize" in r.stderr or "validation failed" in r.stderr:
        raise RuntimeError(r.stderr)
    decoder = json.JSONDecoder()
    text = r.stdout.lstrip()
    reports = {}
    while text:
        j, end = decoder.raw_decode(text)
        for f in j["files"]:
            reports[str(Path(f["path"]).resolve())] = {t["id"] for t in f.get("traits", [])}
        text = text[end:].lstrip()
    return reports


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    apis = ["NtCreateSection", "NtMapViewOfSection", "NtProtectVirtualMemory", "QueueUserAPC", "ResumeThread"]
    guests = r"C:\Windows\System32\drivers\vboxguest.sys;C:\Program Files\VMware\VMware Tools;C:\Program Files\Qemu-ga"
    cases = [
        ("api-key-a.exe", pe(b"".join(xor(x, 0x5A) for x in apis)), {API}, {VM}),
        ("renamed.exe", pe(b"".join(xor(x, 0x23) for x in apis), b".pool"), {API}, {VM}),
        ("api-missing-apc.exe", pe(b"".join(xor(x, 0x5A) for x in apis if x != "QueueUserAPC")), set(), {API}),
        ("api-plaintext.exe", pe("\0".join(apis).encode()), set(), {API}),
        ("vm-list.exe", pe(xor(guests, 0xA7)), {VM}, {API}),
        ("vm-plaintext.exe", pe(guests.encode()), set(), {VM}),
        ("vm-one-vendor.exe", pe(xor(r"C:\Windows\System32\drivers\vboxguest.sys;", 0xA7)), set(), {VM}),
        ("commands.exe", pe(b"mtr -rw 1.1.1.1\0dd if=/tmp/payload of=/tmp/output\0dd > /tmp/result\0"), {MTR, DD}, set()),
        ("dd-input-redirect.exe", pe(b"dd < /tmp/payload > /tmp/output\0"), {DD}, set()),
        ("dd-adjacent-redirect.exe", pe(b"dd>/tmp/output\0"), {DD}, set()),
        ("noise.exe", pe(b"words mtr 6e more words\0dd r 2tfdl muh > xa\0"), set(), {MTR, DD}),
        ("host-options.bat", b'winws.exe --hostlist="list-general.txt"\r\n', {OPTION}, set()),
        ("source-options.py", b'parser.add_argument("--scan-file")\n', {OPTION}, set()),
        ("large-plus-exe.rar", rar([("large.txt", b"x" * 300000), ("program.exe", pe(b"hello"))]), {ARCHIVE}, set()),
        ("large-plus-batch.rar", rar([("large.txt", b"x" * 1100000), ("run.bat", b"@echo off\r\n")]), {ARCHIVE}, set()),
        ("large-no-code.rar", rar([("large.txt", b"x" * 300000)]), set(), {ARCHIVE}),
        ("destructive-batch.rar", rar([
            ("large.txt", b"x" * 300000),
            ("action.bat", b"@echo off\r\n" + b"rd C:\\victim /s /q\r\n" * 24
             + b"del /f /q C:\\Windows\\System32\\cmd.exe\r\nwevtutil cl System\r\n"),
        ]), {"objectives/command-and-control/dropper/delivery/rar::rar-fat-batch-destructive-cleaner"}, set()),
        ("cve-runner.py", b'import requests\nfrom concurrent.futures import ThreadPoolExecutor\n'
         b'CVE = "CVE-2025-12345"\nparser.add_argument("--scan-file")\n'
         b'with ThreadPoolExecutor(max_workers=8) as pool:\n'
         b'    pool.map(lambda url: requests.post(url, data={"code": "test"}), hosts)\n',
         {"objectives/lateral-movement/exploit/scanner::mass-cve-exploitation-runner"}, set()),
        ("management-scan.py", b'import requests\nparser.add_argument("--host-file")\n'
         b'paths = ["/admin", "/ucp", "/pbx"]\n'
         b'for path in paths:\n    requests.get(host + path)\n',
         {"objectives/discovery/network/scan/http::bulk-http-management-path-scan"}, set()),
    ]
    checks = []
    for name, data, required, forbidden in cases:
        path = args.output / name
        path.write_bytes(data)
        checks.append((name, path, required, forbidden))
    for name in ["testdata/impact-wipe/08-linux-hardcoded-sda.sh",
                 "testdata/version-drift/active-device.sh"]:
        checks.append((name, REPO / name, {DD}, set()))
    reports = scan([path for _, path, _, _ in checks])
    results = []
    for name, path, required, forbidden in checks:
        got = reports[str(path.resolve())]
        assert required <= got, (name, "missing", sorted(required - got))
        assert not forbidden & got, (name, "unexpected", sorted(forbidden & got))
        results.append({"case": name, "required": sorted(required), "forbidden": sorted(forbidden), "passed": True})
    (args.output / "results.json").write_text(json.dumps(results, indent=2) + "\n")
    print(f"Passed {len(results)} focused controls")


if __name__ == "__main__":
    main()
