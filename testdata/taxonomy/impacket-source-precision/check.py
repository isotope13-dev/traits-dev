import json, pathlib, subprocess
ROOT = pathlib.Path(__file__).resolve().parents[3]
BASE = pathlib.Path(__file__).resolve().parent
cases = json.loads((BASE / "cases.json").read_text())
run = subprocess.run(["cleave", "--traits-dir", str(ROOT), "--json", *[str(BASE/name) for name in cases]], capture_output=True, text=True)
if run.returncode:
    raise RuntimeError(run.stderr)
reports = [json.loads(line) for line in run.stdout.splitlines() if line.strip()]
observed = {}
for report in reports:
    for artifact in report["files"]:
        observed[pathlib.Path(artifact["path"]).name] = {trait["id"] for trait in artifact["traits"]}
for name, checks in cases.items():
    ids = observed[name]
    for expected in checks.get("matched", []):
        assert expected in ids, (name, "missing", expected, sorted(ids))
    for forbidden in checks.get("not_matched", []):
        assert forbidden not in ids, (name, "unexpected", forbidden)
    print("PASS", name)
