"""Matcher controls for managed thread-information call layouts.

Generated PE stubs contain static evidence tables and return immediately.
Run: python3 testdata/managed-thread-hide-review/check.py <scratch-directory>
"""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location(
    "managed_controls", ROOT / "testdata/managed-records-review/verify.py")
controls = importlib.util.module_from_spec(spec)
spec.loader.exec_module(controls)

RULE = ("objectives/anti-analysis/debugger-detect/thread-hide::"
        "managed-thread-hide-class17-call-profile")
API = "micro-behaviors/process/thread/config::nt-set-information-thread-name"
LAYOUT = "metadata/binary/instruction::cil-helper-class17-field-zero-call"
CIL = bytes.fromhex("28 01 00 00 06 1f 11 7e 01 00 00 0a 16 28 02 00 00 06 26")

dest = Path(sys.argv[1])
dest.mkdir(parents=True, exist_ok=True)
cases = [
    ("hide-class17.exe", ["NtSetInformationThread"], CIL, True, True),
    ("zw-hide-class17.exe", ["ZwSetInformationThread"], CIL, True, True),
    ("fielddef-class17.exe", ["NtSetInformationThread"],
     CIL.replace(b"\x7e\x01\x00\x00\x0a", b"\x7e\x01\x00\x00\x04"), True, True),
    ("other-class.exe", ["NtSetInformationThread"],
     CIL.replace(b"\x1f\x11", b"\x1f\x10"), False, True),
    ("declaration-only.exe", ["NtSetInformationThread"], b"", False, True),
    ("unrelated-callee.exe", ["OtherFunction"], CIL, False, False),
    ("api-substring.exe", ["NotNtSetInformationThread"], CIL, False, False),
    ("missing-length.exe", ["NtSetInformationThread"],
     CIL.replace(b"\x16\x28", b"\x17\x28"), False, True),
]
for name, markers, cil, expected, api in cases:
    path = dest / name
    path.write_bytes(controls.build_pe(markers, cil))
    result = subprocess.run(
        [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT),
         "--disable", "third-party", "--format", "json", str(path)],
        capture_output=True, text=True, check=True)
    traits = {t["id"]: t for f in json.loads(result.stdout)["files"]
              for t in f.get("traits", [])}
    assert (RULE in traits) == expected, (name, sorted(traits))
    assert (API in traits) == api, (name, sorted(traits))
    if expected:
        assert LAYOUT in traits, name
        assert traits[RULE]["crit"] == 4, name
    if api:
        assert traits[API]["crit"] == 3, name
    print("PASS", name, flush=True)
