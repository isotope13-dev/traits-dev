#!/usr/bin/env python3
"""Ensure separate Python files cannot combine into a shellcode-loader finding."""
import argparse
import importlib.util
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
spec = importlib.util.spec_from_file_location(
    "taxonomy_memory_map", ROOT / "scripts/check-taxonomy-memory-map.py"
)
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cleave", default=str(ROOT.parent / "cleave/target/release/cleave"))
    parser.add_argument("--traits-dir", type=Path, default=ROOT)
    args = parser.parse_args()
    cleave = shutil.which(args.cleave)
    if not cleave:
        raise SystemExit(f"Cannot find cleave: {args.cleave}")

    fixtures = Path(__file__).resolve().parent
    source_names = (
        "ctypes-mmap-no-executable-memory.py",
        "mmap-executable-memory-no-ctypes.py",
    )
    command = [
        str(Path(cleave).resolve()),
        "--no-update-check",
        "--traits-dir",
        str(args.traits_dir.resolve()),
        "--disable",
        "yara,radare2,upx",
        "--format",
        "json",
    ]
    with tempfile.TemporaryDirectory(prefix="tax-run-") as temp:
        directory = Path(temp) / "split-source"
        directory.mkdir()
        for name in source_names:
            shutil.copy2(fixtures / name, directory / name)
        result = subprocess.run(
            [*command, "analyze", str(directory)],
            text=True,
            capture_output=True,
            check=True,
            env={**os.environ, "CLEAVE_SKIP_CACHE": "1"},
        )
        reports = list(runner.reports(result.stdout))
        by_name = {Path(report["path"]).name: report for report in reports}
        assert set(source_names) <= by_name.keys(), ("missing source reports", by_name.keys())

        imports_only = by_name[source_names[0]]
        imports = {trait["id"] for trait in imports_only.get("traits", [])}
        assert "metadata/import/python/ctypes::ctypes" in imports, imports
        assert "metadata/import/python/mmap::mmap" in imports, imports
        assert "micro-behaviors/mem/map::python-mmap-prot-exec" not in imports, imports

        executable_only = by_name[source_names[1]]
        executable_traits = {trait["id"] for trait in executable_only.get("traits", [])}
        assert "metadata/import/python/mmap::mmap" in executable_traits, executable_traits
        assert "metadata/import/python/ctypes::ctypes" not in executable_traits, executable_traits
        assert "micro-behaviors/mem/map::python-mmap-prot-exec" in executable_traits, executable_traits

        composite = "objectives/supply-chain/hidden-payload/imports::shellcode-loader-imports"
        for report in reports:
            found = {trait["id"] for trait in report.get("traits", [])}
            assert composite not in found, (report["path"], found)
    print("shellcode-loader split-source control passed: separate imports and executable mmap stay separate")


if __name__ == "__main__":
    main()
