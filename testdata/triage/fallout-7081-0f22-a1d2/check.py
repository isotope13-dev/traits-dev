#!/usr/bin/env python3
"""Generate inert controls and mutant samples outside the trait checkout."""
import argparse
import concurrent.futures
import json
import struct
import subprocess
from pathlib import Path

WATCH = "micro-behaviors/fs/device/ioctl::x64-watchdog-disable-call"
XOR = "micro-behaviors/data/decode/xor::x64-four-lane-table-xor-loop"
CONN = "micro-behaviors/communications/socket/connect::socket-create-and-connect-syscalls"
EXPLOIT = "objectives/lateral-movement/exploit/network-device/upnp::huawei-hg532-upnp-exploit"
OLD = "objectives/lateral-movement/brute-force/iot-creds::xor-credential-table-watchdog-bot"
IMPORT = "metadata/import/package::node-net-namespace-import"
NAMED = "metadata/import/package::node-net-createconnection-import"


def elf(code, data=b""):
    # One RX load segment, with distinct executable and read-only sections.
    names = b"\0.text\0.rodata\0.shstrtab\0"
    shoff = (0x200 + len(code) + len(data) + len(names) + 7) & ~7
    b = bytearray(shoff + 4 * 64)
    ident = b"\x7fELF\x02\x01\x01" + bytes(9)
    struct.pack_into("<16sHHIQQQIHHHHHH", b, 0, ident, 2, 62, 1,
                     0x400200, 64, shoff, 0, 64, 56, 1, 64, 4, 3)
    struct.pack_into("<IIQQQQQQ", b, 64, 1, 5, 0, 0x400000, 0x400000,
                     shoff, shoff, 0x1000)
    b[0x200:0x200+len(code)] = code
    doff = 0x200 + len(code)
    b[doff:doff+len(data)] = data
    noff = doff + len(data)
    b[noff:noff+len(names)] = names
    for i, record in enumerate([
        (1, 1, 6, 0x400200, 0x200, len(code), 0, 0, 16, 0),
        (7, 1, 2, 0x400000+doff, doff, len(data), 0, 0, 1, 0),
        (15, 3, 0, 0, noff, len(names), 0, 0, 1, 0),
    ], 1):
        struct.pack_into("<IIQQQQIIQQ", b, shoff+i*64, *record)
    return bytes(b)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sample", type=Path, required=True)
    ap.add_argument("--scratch", type=Path, required=True)
    ap.add_argument("--cleave", default="cleave")
    args = ap.parse_args()
    args.scratch.mkdir(parents=True, exist_ok=True)
    source = args.sample.read_bytes()
    cases = []

    def add(name, content, expected, no_hostile=False):
        path = args.scratch / name
        path.write_bytes(content)
        cases.append((path, expected, no_hostile))

    add("original.elf", source, {WATCH: True, XOR: True, CONN: True, EXPLOIT: True, OLD: False})
    old = bytes.fromhex("be0457048031c04889eac744243001000000")
    assert source.count(old) == 1
    add("watchdog-enable.elf", source.replace(old, old[:-4] + bytes.fromhex("02000000")),
        {WATCH: False, XOR: True, EXPLOIT: True})
    old = bytes.fromhex("443009488b0a4801c14883c001443001")
    assert source.count(old) == 1
    add("xor-lane-removed.elf", source.replace(old, old.replace(bytes.fromhex("443009"), b"\x90"*3, 1)),
        {WATCH: True, XOR: False, EXPLOIT: True})
    old = b"<NewStatusURL>$("
    assert source.count(old) == 1
    add("soap-no-substitution.elf", source.replace(old, b"<NewStatusURL>xx"),
        {WATCH: True, XOR: True, EXPLOIT: False})
    dictionary = b"\0".join(bytes(c ^ 0x22 for c in word) for word in
                            [b"juantech", b"smcadmin", b"xmhdipc"]) + b"\0"
    add("dictionary-watchdog-only.elf", elf(b"\xc3", dictionary+b"/dev/watchdog\0/dev/misc/watchdog\0"),
        {WATCH: False, XOR: False, CONN: False, OLD: False}, True)
    socket = bytes.fromhex("b8290000000f05")
    connect = bytes.fromhex("b82a0000000f05")
    add("socket-and-connect.elf", elf(socket+connect+b"\xc3"), {CONN: True, WATCH: False, XOR: False}, True)
    add("socket-only.elf", elf(socket+b"\xc3"), {CONN: False}, True)
    add("connect-only.elf", elf(connect+b"\xc3"), {CONN: False}, True)
    add("net-import.js", b"const net = require('node:net');\n", {IMPORT: True, NAMED: False}, True)
    add("net-named-import.js", b"import {createConnection} from 'net';\n", {IMPORT: False, NAMED: True}, True)

    def check(case):
        path, expected, no_hostile = case
        proc = subprocess.run([args.cleave, "--traits-dir", str(Path.cwd()), "--format", "json", str(path)],
                              capture_output=True, text=True, check=True)
        report = json.loads(proc.stdout)
        findings = [f for r in report["files"] for f in r.get("traits", [])]
        ids = {f["id"] for f in findings}
        for trait, present in expected.items():
            assert (trait in ids) == present, (path.name, trait, present)
        if no_hostile:
            assert not any(f.get("crit") == 5 for f in findings), path.name
        return {"case": path.name, "passed": True, "expected": expected}

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
        results = list(pool.map(check, cases))
    (args.scratch / "results.json").write_text(json.dumps(results, indent=2)+"\n")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
