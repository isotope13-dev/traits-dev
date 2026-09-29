#!/usr/bin/env python3
"""Check the encrypted Artem COM infector and benign DOS controls."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPECIMEN_SHA256 = "af71e82c418536146864ca08475511cc610e1ab30212d1dd0375be80b84c1939"
HOSTILE = "objectives/impact/infect/binary/dos/com-bytes::dos-com-self-modifying-xor-infector"
DECODER = "objectives/anti-static/obfuscation/payload/polymorphic::dos-patched-retf-xor-decryptor"


def traits(binary: str, path: Path) -> dict[str, int]:
    result = subprocess.run(
        [binary, "--traits-dir", str(ROOT), "--format", "json", str(path)],
        capture_output=True,
        text=True,
        check=True,
    )
    report = json.loads(result.stdout)
    return {
        trait["id"]: trait["crit"]
        for file in report["files"]
        for trait in file.get("traits", [])
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cleave", default="cleave")
    args = parser.parse_args()

    sample = ROOT / "testdata/hostile/dos-com/artem-2165"
    digest = hashlib.sha256(sample.read_bytes()).hexdigest()
    assert digest == SPECIMEN_SHA256, f"specimen fixture changed: {digest}"
    matched = traits(args.cleave, sample)
    assert matched.get(HOSTILE, 0) >= 5, ("missing encrypted infector finding", matched)
    assert DECODER in matched, ("missing decoder evidence", matched)
    print("artem-2165: passed", flush=True)

    for name in (
        "dos-table-query.com",
        "dos-ah52-unrelated-call.com",
        "anton-97",
    ):
        folder = "testdata/hostile/dos-com" if name == "anton-97" else "testdata/benign"
        control = ROOT / folder / name
        matched = traits(args.cleave, control)
        assert HOSTILE not in matched, (name, "unrelated or direct-write control matched", matched)
        assert DECODER not in matched, (name, "decoder control matched", matched)
        print(f"{name}: passed", flush=True)


if __name__ == "__main__":
    main()
