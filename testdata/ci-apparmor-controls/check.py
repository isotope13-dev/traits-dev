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
env = dict(os.environ, CLEAVE_TRAITS_DIR=str(ROOT), SCAN_HOPPER="")
checked = set()
with tempfile.TemporaryDirectory(prefix="trait-controls-") as directory:
    for relpath, case in cases.items():
        src = HERE / Path(relpath).name
        dst = Path(directory) / relpath
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)
        # Scan each staged file directly: directory walks skip dot-dirs such
        # as .github/, which the workflow-context case needs in its path.
        result = subprocess.run(
            ["atomscan", "--no-update", "--follow=none", "--format=json", "path", str(dst)],
            env=env, text=True, capture_output=True, check=False,
        )
        assert result.returncode == 0, result.stderr
        assert "warning" not in result.stderr.lower(), result.stderr
        found = False
        for line in result.stdout.splitlines():
            for report in json.loads(line)["raw"]["files"]:
                if Path(report["path"]).name != Path(relpath).name:
                    continue
                # Embedded workflow run steps share their parent's basename
                # pattern ("run"); only judge the top-level fixture node,
                # whose path has no !!-joined child suffix.
                if "!!" in report["path"]:
                    continue
                traits = {item["id"]: item["crit"] for item in report.get("traits", [])}
                assert set(case.get("matched", [])) <= traits.keys(), (relpath, traits)
                assert not set(case.get("not_matched", [])) & traits.keys(), (relpath, traits)
                assert sum(value >= 4 for value in traits.values()) == case.get("suspicious", 0), (relpath, traits)
                assert sum(value >= 5 for value in traits.values()) == case.get("hostile", 0), (relpath, traits)
                found = True
        assert found, relpath
        checked.add(relpath)
    assert checked == set(cases.keys()), checked
print(f"Passed {len(cases)} static trait controls")
