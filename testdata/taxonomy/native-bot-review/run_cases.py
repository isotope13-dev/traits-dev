#!/usr/bin/env python3
"""Scan inert mutations; requires the three review samples as positional inputs.

No specimen or generated shell script is executed. Work products stay in the
explicit work directory. The specimens themselves are never modified.
"""
import argparse
import json
from pathlib import Path
import subprocess


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("windows", type=Path)
    parser.add_argument("elf", type=Path)
    parser.add_argument("loader", type=Path)
    parser.add_argument("--work-dir", required=True, type=Path)
    parser.add_argument("--cleave", default="cleave")
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[3]
    args.work_dir.mkdir(parents=True, exist_ok=True)
    cases = []
    dos = "objectives/impact/dos/attack/botnet::i386-attack-parser-gre-flood"
    bot = "objectives/command-and-control/botnet/iot::static-x86-procfs-socketcall-bot"
    edr = "objectives/impact/degrade/edr/targeting::socket-tasking-security-process-killer"
    launch = "micro-behaviors/process/deploy::multiarch-fallback-launch-profile"
    hidden = "objectives/evasion/file-hiding/staging::hidden-temp-fallback-fetch-exec"

    def case(name, data, present=(), absent=(), no_hostile=False):
        path = args.work_dir / name
        path.write_bytes(data)
        cases.append((path, set(present), set(absent), no_hostile))

    elf = args.elf.read_bytes()
    case("positive.elf", elf, (dos, bot))
    # Keep the original static/uClibc/procfs evidence, remove one behavioral
    # requirement at a time. File offsets are documented disassembly sites.
    for name, offset, expected, replacement in [
        ("no-frame.elf", 0x4C8D, bytes.fromhex("66 c1 c8 08"), b"\x90" * 4),
        ("no-parser.elf", 0x2B0, bytes.fromhex("8b 2e"), b"\x90" * 2),
        ("no-gre.elf", 0x1615, bytes.fromhex("c6 43 09 2f"), bytes.fromhex("c6 43 09 06")),
        ("unrelated-send.elf", 0x17CD, bytes.fromhex("e8 a1 68 00 00"), b"\xe8\x00\x00\x00\x00"),
    ]:
        assert elf[offset:offset + len(expected)] == expected, name
        data = bytearray(elf)
        data[offset:offset + len(expected)] = replacement
        case(name, data, absent=(dos, bot))
    data = bytearray(elf)
    data[0xB0:0xAFE6] = b"\x00" * (0xAFE6 - 0xB0)
    case("static-metadata-only.elf", data, absent=(dos, bot))
    old = bytes(c ^ 0x3A for c in b"scan.yerco.xyz")
    new = bytes(c ^ 0x3A for c in b"news.other.xyz")
    assert old in elf and len(old) == len(new)
    case("renamed-host.elf", elf.replace(old, new), (dos, bot))
    old = bytes.fromhex("2d 87 c1 6f")
    assert elf.count(old) == 1
    case("changed-c2.elf", elf.replace(old, bytes.fromhex("08 08 08 08")), (dos, bot))

    windows = args.windows.read_bytes()
    case("positive.exe", windows, (edr,))
    data = windows
    for target in [b"KSafeTray.exe", b"KSWebShield.exe", b"kislive.exe"]:
        assert target in data
        data = data.replace(target, b"x" * (len(target) - 4) + b".exe")
    case("ordinary-process-names.exe", data, absent=(edr,))
    data = bytearray(windows)
    assert data[0x7A26:0x7A2C] == bytes.fromhex("ff 15 b8 10 40 00")
    data[0x7A26:0x7A2C] = b"\x90" * 6
    case("no-openprocess-helper.exe", data, absent=(edr,))

    loader = args.loader.read_bytes()
    case("loader.sh", loader, (launch, hidden), no_hostile=True)
    # Legitimate, visible localhost bootstrap; only host/cwd differ from the
    # loader. Downloader fallbacks and chmod must not imply bot membership.
    visible = loader.replace(b"103.210.144.11", b"127.0.0.1").replace(b"/tmp/.x", b"/tmp/bootstrap")
    visible = b"\n".join(line for line in visible.splitlines() if not line.startswith(b"# Cosmic"))
    case("visible-localhost-bootstrap.sh", visible, (launch,), (hidden,), True)
    no_launch = visible.replace(b'./"$f" "$A" 2>/dev/null &', b'sleep 1 &')
    case("download-chmod-background-sleep.sh", no_launch, absent=(launch, hidden), no_hostile=True)
    case("hidden-path-only.sh", b'#!/bin/sh\nd="/tmp/.cache"\nmkdir -p "$d"\n', absent=(launch, hidden), no_hostile=True)
    cleanup = "micro-behaviors/process/deploy::multiarch-fallback-launch-cleanup"
    fixture = repo / "testdata/benign/unverified-multiarch-stager-controls.sh"
    case("unverified-launch-cleanup.sh", fixture.read_bytes(),
         (launch, cleanup), no_hostile=True)

    command = [args.cleave, "--traits-dir", str(repo), "--format", "json"]
    command += [str(c[0]) for c in cases]
    result = subprocess.run(command, text=True, capture_output=True, check=True)
    (args.work_dir / "scan.json").write_text(result.stdout)
    (args.work_dir / "scan.log").write_text(result.stderr)
    files = []
    remaining = result.stdout.lstrip()
    decoder = json.JSONDecoder()
    while remaining:
        document, end = decoder.raw_decode(remaining)
        files.extend(document["files"])
        remaining = remaining[end:].lstrip()
    by_path = {f["path"]: f for f in files}
    results = []
    for path, present, absent, no_hostile in cases:
        findings = by_path[str(path)].get("traits", [])
        ids = {t["id"] for t in findings}
        hostile = [t["id"] for t in findings if t["crit"] == 5]
        assert present <= ids, (path.name, "missing", present - ids)
        assert not absent & ids, (path.name, "unexpected", absent & ids)
        assert not no_hostile or not hostile, (path.name, "hostile", hostile)
        results.append({"case": path.name, "passed": True})
    (args.work_dir / "results.json").write_text(json.dumps(results, indent=2) + "\n")
    print(f"{len(results)} focused cases passed")


if __name__ == "__main__":
    main()
