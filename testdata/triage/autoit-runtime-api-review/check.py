"""Check runtime API false positives without executing the private specimen.

Supply the SPAT/AutoIt CAPE dump with --sample and a scratch --work-dir.
Mutants remove one required observation at a time; they are static controls,
not executable fixtures or independently authenticated software releases.
"""

import argparse
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import subprocess


RUNTIME = "metadata/lang/runtime::autoit-compiled-script-support-diagnostic"
INI = "micro-behaviors/fs/config/system::ini-copy-process-api-set"
CLIPBOARD = "micro-behaviors/hardware/display/screen::gdi-bitmap-clipboard-desktop-api-set"
NETWORK = "micro-behaviors/hardware/display/screen::gdi-desktop-network-delete-api-set"
TIMERS = "micro-behaviors/hardware/input/keyboard/poll::key-state-ui-timer-pe-api-set"
WINDOWS = "micro-behaviors/ui/window/enumerate::shell-window-process-api-set"
UPX = "metadata/build/protector::upx-packing-token-reference"
BANNER = (b"This is a compiled AutoIt script. AV researchers please email "
          b"avsupport@autoitscript.com for support.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sample", type=Path, required=True)
    parser.add_argument("--work-dir", type=Path, required=True)
    parser.add_argument("--atomscan", default="atomscan")
    args = parser.parse_args()
    args.work_dir.mkdir(parents=True, exist_ok=True)
    original = args.sample.read_bytes()
    expected = {RUNTIME: True, INI: True, CLIPBOARD: True, NETWORK: True,
                TIMERS: True, WINDOWS: True, UPX: True}
    cases = [("runtime", original, expected)]

    def remove(name, token, missing):
        assert token in original, (name, token)
        replacement = b"X" * len(token)
        cases.append((name, original.replace(token, replacement),
                      {**expected, missing: False}))

    remove("no-runtime-diagnostic", BANNER, RUNTIME)
    remove("no-desktop-open", b"OpenDesktopW", CLIPBOARD)
    remove("no-winsock-init", b"WSAStartup", NETWORK)
    remove("no-file-copy", b"CopyFileW", INI)
    remove("no-key-state", b"GetKeyState", TIMERS)
    remove("no-window-enumeration", b"EnumWindows", WINDOWS)
    assert b"UPX0" in original and b"UPX1" in original
    cases.append(("no-upx-tokens", original.replace(b"UPX0", b"NOV0").replace(b"UPX1", b"NOV1"),
                  {**expected, UPX: False}))
    token = "SPAT".encode("utf-16le")
    assert token in original
    cases.append(("changed-product", original.replace(token, "TEST".encode("utf-16le")), expected))

    def scan(case):
        name, data, wanted = case
        directory = args.work_dir / name
        directory.mkdir(exist_ok=True)
        # Preserve the collector filename to isolate content-dependent results.
        path = directory / args.sample.name
        path.write_bytes(data)
        result = subprocess.run(
            [args.atomscan, "--no-update", "-f", "json", str(path)],
            check=True, capture_output=True, text=True,
        )
        (directory / "scan.json").write_text(result.stdout)
        (directory / "scan.stderr").write_text(result.stderr)
        report = json.loads(result.stdout)
        traits = {trait["id"]: trait for trait in report["raw"]["files"][0]["traits"]}
        actual = {trait: trait in traits for trait in wanted}
        elevated = [trait["id"] for trait in traits.values() if trait["crit"] >= 4]
        passed = actual == wanted and not elevated
        return {"case": name, "pass": passed, "expected": wanted,
                "actual": actual, "suspicious_or_hostile": elevated}

    with ThreadPoolExecutor(max_workers=3) as executor:
        results = list(executor.map(scan, cases))
    summary = {"passed": sum(case["pass"] for case in results),
               "total": len(results), "cases": results}
    (args.work_dir / "results.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))
    if summary["passed"] != summary["total"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
