"""Generate non-executed byte mutations outside the repo and check new traits.

Usage: python3 check.py UNPACKED_PE --out /tmp/triage/eupdate-controls
The input is the original b814 sample or the unpacked 64de sample.
"""
import argparse
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[3]
XOR = "micro-behaviors/data/decode/xor::x86-index-affine-key-xor-copy-loop"
PORT = "micro-behaviors/process/terminate/kill::listener-port-owner-termination"
RUN = "micro-behaviors/os/autorun/login-items::hklm-run-set-diagnostic"
PATTERN = bytes.fromhex("b01f8a55e732140f0fafc183c00731c28b038814084139ce75e6")


def replace(data, old, new):
    assert len(old) == len(new)
    assert old in data, old
    return data.replace(old, new)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("sample", type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--cleave", default="cleave")
    args = parser.parse_args()
    data = args.sample.read_bytes()
    args.out.mkdir(parents=True, exist_ok=True)
    assert data.count(PATTERN) == 1
    alternate = bytearray(PATTERN)
    alternate[1], alternate[13] = 0x17, 0x0B
    no_xor = bytearray(PATTERN)
    no_xor[5] = 0x02  # ADD instead of XOR: arithmetic alone is not this decoder.
    utf16 = lambda text: text.encode("utf-16le")
    cases = [
        ("positive", data, {XOR, PORT, RUN}),
        ("affine-constant-variation", replace(data, PATTERN, bytes(alternate)), {XOR, PORT, RUN}),
        ("arithmetic-near-miss", replace(data, PATTERN, bytes(no_xor)), {PORT, RUN}),
        ("no-kill-api", replace(data, b"TerminateProcess\0", b"Term1nateProcess\0"), {XOR, RUN}),
        ("no-bind-api", replace(data, b"bind\0", b"b1nd\0"), {XOR, RUN}),
        ("no-attempt-diagnostic", replace(data, utf16("busy, killing owner"), utf16("busy, waiting owner")), {XOR, RUN}),
        ("no-success-diagnostic", replace(data, utf16("killed pid"), utf16("joined pid")), {XOR, RUN}),
        ("no-run-diagnostic", replace(data, utf16("HKLM Run set ->"), utf16("HKLM Run ask ->")), {XOR, PORT}),
    ]
    def scan(case):
        name, content, expected = case
        path = args.out / (name + ".exe")
        path.write_bytes(content)
        env = {**os.environ, "CLEAVE_CACHE_DIR": str(args.out / "cache")}
        result = subprocess.run(
            [args.cleave, "--traits-dir", str(ROOT), "--disable", "third-party,yara",
             "--format", "json", str(path)], capture_output=True, text=True,
            check=True, env=env, timeout=300)
        parsed = json.loads(result.stdout)
        findings = {t["id"] for t in parsed["files"][0]["traits"]}
        observed = findings & {XOR, PORT, RUN}
        assert observed == expected, (name, observed, expected)
        return {"case": name, "matched": sorted(observed), "passed": True}
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(scan, cases))
    (args.out / "results.json").write_text(json.dumps(results, indent=2) + "\n")
    print(f"Passed {len(results)} positive, variation and near-miss controls")


if __name__ == "__main__":
    main()
