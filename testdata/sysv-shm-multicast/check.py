#!/usr/bin/env python3
"""Analyze source fixtures and mutations; never run the exploit operations.

Checks binding, required evidence roles, comments, renaming, C++ and Rust.
The full published proof of concept is kept in the threat-feed scratch data.
"""
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PREFIX = "objectives/privilege-escalation/exploit/kernel::"
WRAP = PREFIX + "sysv-shm-fork-counter-wrap"
MULTICAST = PREFIX + "multicast-iovec-address-corruption"
IOV = PREFIX + "iovec-buffer-address-as-length"


def main():
    wrap = (HERE / "wrap.c").read_text()
    rust = (HERE / "wrap.rs").read_text()
    multicast = (HERE / "multicast.c").read_text()
    cases = []

    def add(name, source, matched=(), absent=(WRAP, MULTICAST)):
        cases.append((name, source, set(matched), set(absent)))

    add("positive.c", wrap, [WRAP], [MULTICAST])
    add("positive.cpp", wrap, [WRAP], [MULTICAST])
    add("positive.rs", rust, [WRAP], [MULTICAST])
    add("multicast-positive.c", multicast, [MULTICAST, IOV], [WRAP])
    add("multicast-positive.cpp", multicast, [MULTICAST, IOV], [WRAP])
    for suffix, source in (("c", wrap + multicast), ("rs", rust)):
        renamed = re.sub(r"\b(mapped|state|segment|child|entries|address|index)\b",
                         lambda m: "renamed_" + m[0], source)
        expected = [WRAP, MULTICAST] if suffix == "c" else [WRAP]
        add("renamed." + suffix, renamed, expected, [] if suffix == "c" else [MULTICAST])

    # Every required role must matter; ordinary teardown is a near miss.
    for name, old, new in (
        ("ordinary-detach", "munmap(mapped, page_size)", "shmdt(mapped)"),
        ("different-mapping", "munmap(mapped, page_size)", "munmap(unrelated, page_size)"),
        ("no-forks", "child = fork()", "child = getpid()"),
        ("negative-count-error", "state.shm_nattch > 0", "state.shm_nattch < 0"),
        ("no-destruction", "IPC_RMID", "IPC_STAT"),
    ):
        assert old in wrap
        add(name + ".c", wrap.replace(old, new))
    add("rust-normal-detach.rs", rust.replace("libc::munmap(mapped, page_size)",
                                             "libc::shmdt(mapped)"))

    for name, old, new in (
        ("ordinary-length", "(size_t)address", "sizeof(bucket)"),
        ("different-entry", "entries[index].iov_len", "entries[index + 1].iov_len"),
        ("different-address", "(size_t)address", "(size_t)other_address"),
        ("valid-descriptor", "readv(-1,", "readv(descriptor,"),
        ("no-join", "IP_ADD_MEMBERSHIP", "IP_DROP_MEMBERSHIP"),
        ("no-ttl", "IP_MULTICAST_TTL", "SO_RCVBUF"),
        ("no-allocator-selector", "KERN_MALLOCSTATS", "KERN_OSREV"),
        ("no-sysctl", "sysctl(mib,", "other_api(mib,"),
    ):
        assert old in multicast
        absent = [WRAP, MULTICAST]
        if name in {"ordinary-length", "different-entry", "different-address"}:
            absent.append(IOV)
        add(name + ".c", multicast.replace(old, new), absent=absent)

    # Code syntax in comments and string literals must not convict.
    combined = wrap + multicast
    add("comments.c", "\n".join("// " + line for line in combined.splitlines()),
        absent=[WRAP, MULTICAST, IOV])
    add("strings.c", "const char *documentation = " + json.dumps(combined) + ";\n",
        absent=[WRAP, MULTICAST, IOV])

    with tempfile.TemporaryDirectory(prefix="sysv-multicast-") as scratch:
        directory = Path(scratch)
        for name, source, _, _ in cases:
            (directory / name).write_text(source)
        command = [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT),
                   "--format", "json", str(directory)]
        result = subprocess.run(command, text=True, capture_output=True, check=True)
        decoder = json.JSONDecoder()
        remaining = result.stdout
        findings = {}
        while remaining.strip():
            report, end = decoder.raw_decode(remaining.lstrip())
            remaining = remaining.lstrip()[end:]
            for file in report["files"]:
                findings[Path(file["path"]).name] = {
                    trait["id"]: trait for trait in file.get("traits", [])}
        checks = 0
        for name, _, matched, absent in cases:
            observed = findings[name]
            for trait in matched:
                assert trait in observed, f"{name}: missing {trait}"
                if trait in {WRAP, MULTICAST}:
                    assert observed[trait]["crit"] == 5, (name, observed[trait])
                checks += 1
            for trait in absent:
                assert trait not in observed, f"{name}: unexpected {trait}"
                checks += 1
        print(f"{checks} assertions passed across {len(cases)} source fixtures")


if __name__ == "__main__":
    main()
