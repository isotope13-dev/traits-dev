import json, os, pathlib, subprocess
root = pathlib.Path(__file__).parent
env = dict(os.environ, CLEAVE_TRAITS_DIR=str(pathlib.Path.cwd()))
env.pop("CLEAVE_VALIDATE", None)
for case in json.loads((root / "cases.json").read_text()):
    result = subprocess.run(["cleave", "--traits-dir", ".", "--format", "json", str(root / case["path"])], text=True, capture_output=True, env=env, check=True)
    report = json.loads(result.stdout)
    traits = {trait["id"] for file in report["files"] for trait in file.get("traits", [])}
    assert set(case.get("matched", [])) <= traits, case
    assert not set(case.get("not_matched", [])) & traits, case
    print(case["path"], "PASS")
