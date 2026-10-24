"""Check static findings on renamed controls; never execute their commands."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent


def main():
    cases = json.loads((HERE / "cases.json").read_text())["fixtures"]
    # Existing encoded-shell rules suppress test-directory paths. A temporary
    # copy exercises executable content independently of the collector's path.
    with tempfile.TemporaryDirectory(prefix="inline-shell-controls-") as tmp:
        paths = []
        for case in cases:
            path = Path(tmp) / Path(case["path"]).name
            shutil.copyfile(ROOT / case["path"], path)
            paths.append(str(path))
        result = subprocess.run(
            [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT),
             "--json", *paths], check=True, capture_output=True, text=True)
        reports = {}
        for line in result.stdout.splitlines():
            for file in json.loads(line)["files"]:
                reports[Path(file["path"]).name] = {
                    trait["id"] for trait in file.get("traits", [])}
        for case in cases:
            name = Path(case["path"]).name
            found = reports[name]
            missing = set(case["matched"]) - found
            unexpected = set(case["not_matched"]) & found
            assert not missing, (name, "missing", sorted(missing))
            assert not unexpected, (name, "unexpected", sorted(unexpected))
    print(f"Passed {len(cases)} static controls")


if __name__ == "__main__":
    main()
