"""Scan inert fixtures outside testdata so directory exclusions cannot pass them."""

import json
from pathlib import Path
import shutil
import subprocess
import tempfile


root = Path(__file__).resolve().parents[2]
cases = json.loads(Path(__file__).with_name("cases.json").read_text())["fixtures"]
with tempfile.TemporaryDirectory(prefix=".literal-source-", dir=root) as directory:
    for case in cases:
        shutil.copyfile(root / case["path"], Path(directory) / Path(case["path"]).name)
    result = subprocess.run(
        ["cleave", "--traits-dir", str(root), "--format", "jsonl", directory],
        check=True,
        capture_output=True,
        text=True,
    )
    reports = {}
    for line in result.stdout.splitlines():
        for report in json.loads(line)["files"]:
            reports[Path(report["path"]).name] = {t["id"] for t in report["traits"]}
    for case in cases:
        name = Path(case["path"]).name
        actual = reports[name]
        expected = set(case.get("matched", []) + case.get("required_emitted", []))
        forbidden = set(case.get("not_matched", []))
        assert expected <= actual, (name, "missing", expected - actual)
        assert not forbidden & actual, (name, "unexpected", forbidden & actual)
        print(f"PASS {name}")
