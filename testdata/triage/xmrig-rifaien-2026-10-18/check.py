#!/usr/bin/env python3
"""Static placement controls; builds fixtures but never executes them."""
import argparse
import json
import os
from pathlib import Path
import struct
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
SIGNAL = "micro-behaviors/process/control/signal::aarch64-kill-syscall"
EXEC = "micro-behaviors/process/create/exec::aarch64-execve-syscall-sequence"
FORK = "micro-behaviors/process/create/fork::fork-syscall"
CLONE = "micro-behaviors/process/create/fork::syscall-clone"
OLD = {
    "micro-behaviors/process/terminate/signal::aarch64-kill-syscall",
    "micro-behaviors/process/create/direct::aarch64-execve-syscall-sequence",
    "micro-behaviors/process/fork/clone::fork-syscall",
    "micro-behaviors/os/syscall/invoke::syscall-clone",
    "micro-behaviors/process/create/exec::csharp-cmd-exe-startinfo",
}


def elf(code):
    """Small executable AArch64 ELF with a real text section and load segment."""
    text_off = 0x1000
    names = b"\0.text\0.shstrtab\0"
    names_off = text_off + len(code)
    shoff = (names_off + len(names) + 7) & ~7
    header = struct.pack(
        "<16sHHIQQQIHHHHHH", b"\x7fELF\x02\x01\x01" + bytes(9),
        2, 183, 1, 0x401000, 64, shoff, 0, 64, 56, 1, 64, 3, 2,
    )
    ph = struct.pack("<IIQQQQQQ", 1, 5, 0, 0x400000, 0x400000,
                     names_off, names_off, 0x1000)
    data = bytearray(header + ph)
    data.extend(bytes(text_off - len(data)))
    data.extend(code + names)
    data.extend(bytes(shoff - len(data)))
    data.extend(bytes(64))
    data.extend(struct.pack("<IIQQQQIIQQ", 1, 1, 6, 0x401000,
                            text_off, len(code), 0, 0, 4, 0))
    data.extend(struct.pack("<IIQQQQIIQQ", 7, 3, 0, 0,
                            names_off, len(names), 0, 0, 1, 0))
    return bytes(data)


def arm_syscall(number):
    return struct.pack("<III", 0xd2800008 | number << 5, 0xd4000001, 0xd65f03c0)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cleave", default=os.environ.get("CLEAVE", "cleave"))
    args = parser.parse_args()

    def check(path, required, absent):
        result = subprocess.run(
            [args.cleave, "--traits-dir", str(ROOT), "--format", "json", str(path)],
            capture_output=True, text=True, check=True,
        )
        report = json.loads(result.stdout)
        ids = {t["id"] for f in report["files"] for t in f.get("traits", [])}
        assert required <= ids, (path.name, "missing", required - ids)
        assert not (absent | OLD) & ids, (path.name, "unexpected", (absent | OLD) & ids)
        print("PASS", path.name)

    with tempfile.TemporaryDirectory(prefix="syscall-placement-") as tmp:
        tmp = Path(tmp)
        controls = [
            ("signal-probe", arm_syscall(129), {SIGNAL}, {EXEC, FORK, CLONE}),
            ("execve", arm_syscall(221), {EXEC}, {SIGNAL, FORK, CLONE}),
            ("clone", arm_syscall(220), {FORK, CLONE}, {SIGNAL, EXEC}),
            ("near-miss", arm_syscall(128), set(), {SIGNAL, EXEC, FORK, CLONE}),
            ("signal-and-exec", arm_syscall(129) + arm_syscall(221),
             {SIGNAL, EXEC}, {FORK, CLONE}),
        ]
        for name, code, required, absent in controls:
            path = tmp / (name + ".elf")
            path.write_bytes(elf(code))
            check(path, required, absent)

        relay = "objectives/command-and-control/reverse-shell/stream-bridge::csharp-connected-cmd-stream-relay"
        cmd = "micro-behaviors/fs/path/application/executable::cmd-exe-image-name"
        for relative, expected in [
            ("testdata/reverse-shell/Revshell.cs", True),
            ("testdata/hostile/csharp-variable-endpoint-relay.cs", True),
            ("testdata/benign/csharp-independent-pipes.cs", False),
            ("testdata/benign/csharp-local-stream-transfer.cs", False),
        ]:
            check(ROOT / relative, {cmd, relay} if expected else {cmd},
                  set() if expected else {relay})



if __name__ == "__main__":
    main()
