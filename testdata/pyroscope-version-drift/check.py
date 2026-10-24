#!/usr/bin/env python3
"""Build inert ELF controls; analyze their bytes without loading the libraries."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
ELEVATION = "objectives/privilege-escalation/elevation-control/sudo::native-sudo-relaunch-marker"
ADVICE = "micro-behaviors/ui/help::native-sudo-retry-advice"
READ = "micro-behaviors/mem/read/cross-process::process-vm-readv-import"
GZIP = "micro-behaviors/data/compress/gzip::libflate-gzip-encoder-type"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--scratch", type=Path, required=True)
    args = parser.parse_args()
    cases = [
        ("permission-advice", 'const char *message = "Permission denied when reading from process. '
         "If you're not running as root, try again with sudo." + '";', {ADVICE}),
        ("reworded-advice", 'const char *message = "Please rerun using sudo.";', {ADVICE}),
        ("restart-advice", 'const char *message = "Not running as root, try restarting with sudo.";',
         {ADVICE}),
        ("status-only", 'const char *message = "Not running as root; sudo is unavailable.";', set()),
        ("relaunch", 'const char *message = "[!] Not running as root, attempting to restart with sudo...";',
         {ELEVATION}),
        ("escalation", 'const char *message = "Attempting to escalate privileges using sudo";',
         {ELEVATION}),
        ("advice-and-relaunch", 'const char *advice = "Please rerun using sudo."; '
         'const char *action = "Not running as root, attempting to relaunch with sudo";',
         {ADVICE, ELEVATION}),
        ("read-import", 'extern long process_vm_readv(int, void *, long, void *, long, long); '
         'long read_memory(int pid, void *local, void *remote) {'
         'return process_vm_readv(pid, local, 1, remote, 1, 0);}', {READ}),
        ("read-export", 'long process_vm_readv(int pid, void *a, long b, void *c, long d, long e) '
         '{return 0;}', set()),
        ("read-text", 'const char *message = "process_vm_readv";', set()),
        ("gzip-encoder-type", 'const char *type = "libflate..gzip..Encoder";', {GZIP}),
        ("gzip-decoder-type", 'const char *type = "libflate..gzip..Decoder";', set()),
    ]
    with tempfile.TemporaryDirectory(prefix="pyroscope-controls-", dir=args.scratch) as work:
        work = Path(work)
        binaries = work / "binaries"
        binaries.mkdir()
        for name, source, _ in cases:
            path = work / (name + ".c")
            path.write_text(source + "\n")
            subprocess.run(["zig", "cc", "-target", "x86_64-linux-gnu", "-shared", "-nostdlib",
                            "-O1", str(path), "-o", str(binaries / (name + ".elf"))], check=True)
        result = subprocess.run([os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT),
                                 "--format", "json", str(binaries)],
                                capture_output=True, text=True)
        if result.returncode:
            raise RuntimeError(result.stderr)
        decoder = json.JSONDecoder()
        remaining = result.stdout
        observed = {}
        while remaining.strip():
            remaining = remaining.lstrip()
            report, end = decoder.raw_decode(remaining)
            remaining = remaining[end:]
            for file in report["files"]:
                observed[Path(file["path"]).stem] = {
                    trait["id"]: trait["crit"] for trait in file.get("traits", [])}
        for name, _, expected in cases:
            traits = observed[name]
            for trait in (ELEVATION, ADVICE, READ, GZIP):
                assert (trait in traits) == (trait in expected), (name, trait, traits)
                if trait in expected:
                    assert traits[trait] == (4 if trait == ELEVATION else 3), (name, trait, traits)
    print("48 presence/absence checks passed across twelve ELF controls; severities verified")


if __name__ == "__main__":
    main()
