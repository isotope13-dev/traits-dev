"""Static-only controls; copy outside testdata to avoid test-context exclusions."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
cases = json.loads((HERE / "cases.json").read_text())
with tempfile.TemporaryDirectory(prefix="trait-controls-") as directory:
    for filename in cases:
        shutil.copyfile(HERE / filename, Path(directory) / filename)
    env = dict(os.environ, CLEAVE_TRAITS_DIR=str(ROOT), SCAN_HOPPER="")
    result = subprocess.run(
        ["atomscan", "--no-update", "--follow=none", "--format=json", "path", directory],
        env=env, text=True, capture_output=True, check=False,
    )
    assert result.returncode == 0, result.stderr
    assert "warning" not in result.stderr.lower(), result.stderr
    checked = set()
    for line in result.stdout.splitlines():
        for report in json.loads(line)["raw"]["files"]:
            name = Path(report["path"]).name
            if name not in cases:
                continue
            case = cases[name]
            traits = {item["id"]: item["crit"] for item in report.get("traits", [])}
            assert set(case.get("matched", [])) <= traits.keys(), (name, traits)
            assert not set(case.get("not_matched", [])) & traits.keys(), (name, traits)
            assert sum(value >= 4 for value in traits.values()) == case.get("suspicious", 0), (name, traits)
            assert sum(value >= 5 for value in traits.values()) == case.get("hostile", 0), (name, traits)
            checked.add(name)
    assert checked == cases.keys(), checked
print(f"Passed {len(cases)} static trait controls")
