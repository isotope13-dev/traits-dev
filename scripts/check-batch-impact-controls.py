#!/usr/bin/env python3
"""Check the DOS batch wipe rules against recovered samples and a safe control."""
import argparse
import hashlib
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {
    "system-file-wipe.bat": (
        "cad54fa04633eaab0e1426cc0fe87a09e51c94f87012bc730c274862a8d83da4",
        "objectives/impact/wipe/user-data::batch-attribute-clear-and-system-file-wipe",
        5,
    ),
    "windows-ini-wipe.bat": (
        "403ed4bbc40a7d305a377fc13814c2e9d8ac6dc4905433aefee73067f3b2f548",
        "objectives/impact/wipe/user-data::batch-windows-ini-wipe",
        5,
    ),
    "scheduled-shutdown.bat": (
        "bcdb86a0c13e70129831fa1210ef74b5e5eb2df66843850a98e07e3371505dd9",
        "micro-behaviors/os/event/shutdown::shutdown-command-source",
        3,
    ),
    "shimmer-boot-sector.d": (
        "f07c78bef2de3da5e3113a6c1e8ed97a1bb6430c7d7dfd53185597496f503d99",
        "objectives/impact/infect/boot-sector::dos-boot-sector-infector",
        5,
    ),
}


def findings(binary: str, path: Path) -> dict[str, int]:
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

    for name, (sha, expected_trait, minimum_crit) in EXPECTED.items():
        path = ROOT / "testdata/hostile/batch" / name
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        assert actual == sha, f"{name}: fixture bytes changed ({actual})"
        traits = findings(args.cleave, path)
        assert traits.get(expected_trait, 0) >= minimum_crit, (
            name,
            "missing hostile wipe finding",
            traits,
        )
        print(f"{name}: passed", flush=True)

    control = ROOT / "testdata/benign/batch-ordinary-delete-control.bat"
    traits = findings(args.cleave, control)
    assert not any(
        trait.startswith("objectives/impact/wipe/user-data::") and crit >= 4
        for trait, crit in traits.items()
    ), (control.name, "ordinary temp-file cleanup matched a wipe objective", traits)
    print(f"{control.name}: passed", flush=True)


if __name__ == "__main__":
    main()
