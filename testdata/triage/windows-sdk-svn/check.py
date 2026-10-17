"""Static controls for SDK resolver syntax and Subversion property records."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
cases = json.loads((HERE / "cases.json").read_text())
traced = {"metadata/file/profile/string-population::source-strings-per-line-at-most-0-9"}
scratch = os.environ.get("TRAIT_CONTROL_SCRATCH", str(ROOT))
with tempfile.TemporaryDirectory(prefix="sdk-svn-controls-", dir=scratch) as directory:
    paths = []
    for filename in cases:
        target = Path(directory) / filename
        shutil.copyfile(HERE / filename, target)
        paths.append(str(target))
    env = dict(os.environ, CLEAVE_TRAITS_DIR=str(ROOT), SCAN_HOPPER="")
    result = subprocess.run(
        ["atomscan", "--no-update", "--mode=slow", "--follow=none",
         "--format=json", "path", *paths],
        env=env, text=True, capture_output=True, check=True,
    )
    checked = set()
    for line in result.stdout.splitlines():
        for report in json.loads(line)["raw"]["files"]:
            name = Path(report["path"]).name
            if name not in cases:
                continue
            case = cases[name]
            traits = {item["id"]: item["crit"] for item in report.get("traits", [])}
            assert set(case.get("matched", [])) - traced <= traits.keys(), (name, traits)
            assert not (set(case.get("not_matched", [])) - traced) & traits.keys(), (name, traits)
            assert all(value < 4 for value in traits.values()), (name, traits)
            # Baseline findings can be stripped when no fired composite
            # references them. Trace evaluation rather than its presentation.
            for expectation in ("matched", "not_matched"):
                for trait in set(case.get(expectation, [])) & traced:
                    trace = subprocess.run(
                        ["cleave", "--traits-dir", str(ROOT), "test-rules",
                         "--rules", trait, str(Path(directory) / name)],
                        env=env, text=True, capture_output=True, check=True,
                    )
                    status = "MATCHED" if expectation == "matched" else "NOT MATCHED"
                    assert f"\n{status} {trait} " in trace.stdout, trace.stdout + trace.stderr
            checked.add(name)
    assert checked == cases.keys(), checked
print(f"Passed {len(cases)} static SDK/Subversion controls")
