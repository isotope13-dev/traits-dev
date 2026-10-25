"""Check packet-filter evidence against compiler data and source near misses."""
import argparse
import json
from pathlib import Path
import struct
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[3]
BPF = "micro-behaviors/os/bpf/program/icmp::"
ICMP = "micro-behaviors/communications/ip/services::services-icmp"
BOUNDARY = "micro-behaviors/communications/http/header/custom::boundary-param"
EXPLOIT = "objectives/execution/exploit/network-service/shell-handoff::exploiting-status"
ARM = "micro-behaviors/fs/path/binary::architecture-executable-arm-suffix"


def elf(rodata):
    """A small ELF64 with a real .rodata section, independent of host tools."""
    names = b"\0.rodata\0.shstrtab\0"
    shoff = (64 + len(rodata) + len(names) + 7) & ~7
    header = struct.pack(
        "<16sHHIQQQIHHHHHH", b"\x7fELF\x02\x01\x01" + bytes(9),
        3, 62, 1, 0, 0, shoff, 0, 64, 0, 0, 64, 3, 2,
    )
    sections = bytes(64) + struct.pack(
        "<IIQQQQIIQQ", 1, 1, 2, 64, 64, len(rodata), 0, 0, 8, 0,
    ) + struct.pack(
        "<IIQQQQIIQQ", 9, 3, 0, 0, 64 + len(rodata), len(names), 0, 0, 1, 0,
    )
    return (header + rodata + names).ljust(shoff, b"\0") + sections


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cleave", default="cleave")
    args = parser.parse_args()
    le = bytes.fromhex("15 00 00 01 D2 04 00 00")
    be = bytes.fromhex("15 00 00 01 04 D2 00 00")
    load = bytes.fromhex("28 00 00 00 28 00 00 00")
    indirect = bytes.fromhex("48 00 00 00 06 00 00 00")
    cases = {
        "packet-le.so": (elf(b"ICMP packet\0" + load + le),
                         {BPF + "cbpf-jeq-1234-le", BPF + "icmp-sequence-1234"}, set()),
        "packet-be.so": (elf(b"ICMP packet\0" + load + be),
                         {BPF + "cbpf-jeq-1234-be", BPF + "icmp-sequence-1234"}, set()),
        "packet-indirect.so": (elf(b"ICMP packet\0" + indirect + le),
                               {BPF + "cbpf-jeq-1234-le"}, set()),
        "unrelated-table.so": (elf(b"ICMP packet\0" + bytes.fromhex(
            "10 24 00 00 D2 04 00 00 15 00 00 00 D2 04 00 00 15 00 00 00 FF FF FF FF")),
            {ICMP}, {BPF + "cbpf-jeq-1234-le", BPF + "icmp-sequence-1234"}),
        "compiler-vocabulary.so": (elf(
            b"LHS in icmp needs nsw for equality predicates\0" + load + le),
            {BPF + "cbpf-jeq-1234-le"}, {ICMP, BPF + "icmp-sequence-1234"}),
        "compiler-options.so": (elf(
            b"-x86-align-branch-boundary=\0hwdiv-arm\0elf_i386\0elf32-mips\0"
            b"Optimization exploiting distributive property).\0objc_msgSend\0"),
            set(), {BOUNDARY, ARM, EXPLOIT,
                    "micro-behaviors/process/interpreter/runtime/dynamic::objc-runtime-msgsend"}),
        "network-banner.so": (elf(b"multipart/form-data; boundary=abc\0"
                                  b"Exploiting target...\0payload-arm\0"),
                              {BOUNDARY, ARM, EXPLOIT}, set()),
        "events.c": (b"typedef enum { start, stop } event_type_t;\n",
                     {"metadata/lang/source/naming/declaration::event-type-name"},
                     {"micro-behaviors/os/bpf/program/loader::event-type-enum"}),
        "header.hpp": (b"#ifndef _LIBCPP_EXPERIMENTAL_SIMD\n#define _LIBCPP_EXPERIMENTAL_SIMD\n#endif\n",
                       {"metadata/lang/upstream::libcpp-header-guard"},
                       {"well-known/lib/development/zig-stdlib::zig-libcxx-header-guard"}),
        "file-size.c": (b"unsigned long query(void *h) { return GetFileSize(h, 0); }\n",
                        {"micro-behaviors/fs/file/stat::source-getfilesize-reference"},
                        {"objectives/command-and-control/backdoor/native-source::source-getfilesize-call"}),
        "compiler-header.c": (b"/* Intel compiler header section */\nint main(void) { return 0; }\n",
                              {"metadata/lang/compiler/systems::intel-header-section-text"},
                              {"objectives/impact/degrade/calculation::compiler-artifact-targeting--rx-4",
                               "objectives/impact/degrade/calculation::compiler-artifact-targeting"}),
    }
    with tempfile.TemporaryDirectory() as temp:
        paths = []
        for name, (data, _, _) in cases.items():
            path = Path(temp) / name
            path.write_bytes(data)
            paths.append(str(path))
        result = subprocess.run(
            [args.cleave, "--disable", "radare2", "--traits-dir", str(ROOT),
             "analyze", "--format", "json", *paths],
            check=True, capture_output=True, text=True,
        )
        reports = []
        remaining = result.stdout.strip()
        while remaining:
            report, end = json.JSONDecoder().raw_decode(remaining)
            reports.append(report)
            remaining = remaining[end:].lstrip()
        observed = {Path(f["path"]).name: {t["id"] for t in f.get("traits", [])}
                    for report in reports for f in report["files"]}
        for name, (_, required, absent) in cases.items():
            actual = observed[name]
            assert required <= actual, (name, "missing", required - actual)
            assert not absent & actual, (name, "unexpected", absent & actual)
        # Scan output intentionally omits transparent OR groups. Check this
        # group's evaluation separately to preserve its sabotage consumer.
        group = "metadata/lang/compiler/systems::intel-artifact-text-reference"
        trace = subprocess.run(
            [args.cleave, "--disable", "radare2", "--traits-dir", str(ROOT),
             "test-rules", str(Path(temp) / "compiler-header.c"), "--rules", group],
            check=True, capture_output=True, text=True,
        )
        assert "MATCHED " + group in trace.stdout, trace.stdout
    print(f"Passed {len(cases)} compiler/packet-filter boundary controls")


if __name__ == "__main__":
    main()
