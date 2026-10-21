#!/usr/bin/env python3
"""Static PE controls: API co-occurrence does not prove injection or theft."""
import argparse
import json
from pathlib import Path
import struct
import subprocess
import tempfile


def pe(imports, text=b"", data=b""):
    """Build an inert PE64; only a RET is reachable from its entry point."""
    image = bytearray(0x1200)
    image[:2] = b"MZ"
    struct.pack_into("<I", image, 0x3C, 0x80)
    image[0x80:0x84] = b"PE\0\0"
    struct.pack_into("<HHIIIHH", image, 0x84, 0x8664, 3, 0, 0, 0, 0xF0, 0x22)
    o = 0x98
    struct.pack_into("<H", image, o, 0x20B)
    struct.pack_into("<I", image, o + 16, 0x1000)
    struct.pack_into("<Q", image, o + 24, 0x140000000)
    struct.pack_into("<II", image, o + 32, 0x1000, 0x200)
    struct.pack_into("<HH", image, o + 40, 6, 1)
    struct.pack_into("<HH", image, o + 48, 6, 1)
    struct.pack_into("<II", image, o + 56, 0x4000, 0x200)
    struct.pack_into("<HH", image, o + 68, 2, 0x8160)
    struct.pack_into("<QQQQ", image, o + 72, 0x100000, 0x1000, 0x100000, 0x1000)
    struct.pack_into("<I", image, o + 108, 16)
    struct.pack_into("<II", image, o + 120, 0x3000, (len(imports) + 1) * 20)
    for i, (name, va, off, size, flags) in enumerate([
        (b".text", 0x1000, 0x200, 0x200, 0x60000020),
        (b".rdata", 0x2000, 0x400, 0x600, 0x40000040),
        (b".idata", 0x3000, 0xA00, 0x800, 0xC0000040),
    ]):
        struct.pack_into("<8sIIIIIIHHI", image, 0x188 + i * 40,
                         name, size, va, size, off, 0, 0, 0, 0, flags)
    image[0x200] = 0xC3
    image[0x220:0x220 + len(text)] = text
    assert len(data) < 0x600
    image[0x400:0x400 + len(data)] = data
    cursor = 0xA00 + 20 * (len(imports) + 1)

    def store(raw, align=1):
        nonlocal cursor
        cursor = (cursor + align - 1) // align * align
        offset = cursor
        image[offset:offset + len(raw)] = raw
        cursor += len(raw)
        return offset - 0xA00 + 0x3000

    for i, (dll, names) in enumerate(imports.items()):
        name_rva = store(dll.encode() + b"\0")
        functions = [store(b"\0\0" + name.encode() + b"\0", 2) for name in names]
        thunks = b"".join(struct.pack("<Q", rva) for rva in functions + [0])
        lookup = store(thunks, 8)
        iat = store(thunks, 8)
        struct.pack_into("<IIIII", image, 0xA00 + i * 20, lookup, 0, 0, name_rva, iat)
    assert cursor <= len(image)
    return image


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cleave", default="cleave")
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    repo = here.parents[2]
    timer = "micro-behaviors/time/schedule/callback::timer-queue-with-memory-api-references"
    patch = "objectives/evasion/anti-av/blinding::encoded-etw-zero-return-patch"
    shell = "micro-behaviors/communications/ipc/pipe::winsock-child-stdio-pipe-api-context"
    amsi = "objectives/evasion/anti-av/amsi::encoded-amsi-invalidarg-patch"
    capture = "micro-behaviors/hardware/display/screenshot::powershell-hidden-capture-api-references"
    task = "micro-behaviors/os/autorun/control::schtasks-elevated-logon-action-format"
    dual = "micro-behaviors/os/autorun/control::run-key-and-logon-task-command-references"
    names = bytes(c ^ 0x5A for c in b"amsi.dllAmsiScanBuffer") + b"\0"
    names += bytes(c ^ 0x5A for c in b"EtwEventWrite") + b"\0"
    names += bytes(c ^ 0x5A for c in b"cmd.exe") + b"\0"
    stub = bytes.fromhex("C7 03 48 33 C0 C3")
    amsi_stub = bytes.fromhex("C7 84 24 80 00 00 00 B8 57 00 07 66 C7 84 24 84 00 00 00 80 C3")
    layout = bytes.fromhex(
        "C7 84 24 80 00 00 00 68 00 00 00 "
        "C7 84 24 BC 00 00 00 00 01 00 00 "
        "0F 16 84 24 40 00 00 00 48 89 84 24 E0 00 00 00 "
        "31 C0 0F 11 84 24 D0 00 00 00")
    imports = {
        "KERNEL32.dll": ["VirtualProtect", "CreateTimerQueueTimer", "CreatePipe",
                         "PeekNamedPipe", "SetHandleInformation", "CreateProcessA"],
        "WS2_32.dll": ["WSAStartup", "socket", "connect", "send", "recv"],
    }
    task_text = (b'schtasks /create /tn "Fixture" /tr "%s" /sc onlogon /rl highest /f\0'
                 b'reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run '
                 b'/v Fixture /t REG_SZ /d "%s" /f\0')
    fixtures = {
        "timer-and-network.pe": (pe(imports), {timer}, {patch, shell}),
        "names-without-write.pe": (pe(imports, data=names), {timer}, {patch, shell}),
        "patch-without-child-stdio.pe": (pe(imports, stub, names), {patch}, {shell}),
        "child-stdio-and-patches.pe": (pe(imports, stub + amsi_stub + b"\x90" * 16 + layout, names), {patch, amsi, shell}, set()),
        "capture-and-hidden-option.pe": (
            pe({}, data=b"CopyFromScreen\0powershell -WindowStyle Hidden\0"), {capture}, {patch, shell}),
        "task-command-formats.pe": (pe({}, data=task_text), {task, dual}, {patch, shell}),
    }
    retired = {
        "objectives/evasion/process/injection/callback::timer-callback-execution",
        "objectives/evasion/anti-av/amsi::amsi-patch-name-pair-binary",
        "objectives/collection/screenshot::hidden-powershell-screen-capture",
        "objectives/persistence/login/multi-technique::dual-run-key-scheduled-task-persistence",
        "objectives/persistence/login/scheduled-task/cli::schtasks-self-payload-command",
        "objectives/command-and-control/reverse-shell/stream-bridge::winsock-pipe-reverse-shell-pe",
    }
    with tempfile.TemporaryDirectory(prefix=".controls-", dir=here) as temp:
        for name, (binary, required, forbidden) in fixtures.items():
            path = Path(temp, name)
            path.write_bytes(binary)
            result = subprocess.run([args.cleave, "--traits-dir", str(repo), "--format", "json", str(path)],
                                    capture_output=True, text=True)
            assert result.returncode == 0, result.stderr
            report = json.loads(result.stdout)
            traits = {t["id"]: t for f in report["files"] for t in f.get("traits", [])}
            assert required <= traits.keys(), (name, "missing", required - traits.keys())
            assert not (forbidden | retired) & traits.keys(), (name, "unexpected", (forbidden | retired) & traits.keys())
            if name in {"timer-and-network.pe", "capture-and-hidden-option.pe", "task-command-formats.pe"}:
                # The deliberately tiny PE can retain structural warnings.
                assert all(t["crit"] < 5 for t in traits.values()), (name, "false hostile")
            print("PASS", name)


if __name__ == "__main__":
    main()
