import json
from pathlib import Path
import subprocess
import sys

root = Path(__file__).resolve().parents[3]
spec = json.loads(Path(__file__).with_name("cases.json").read_text())
engine = sys.argv[1] if len(sys.argv) > 1 else "cleave"
proc = subprocess.run([engine, "--traits-dir", str(root), "--json", *[str(root / c["path"]) for c in spec["cases"]]], capture_output=True, text=True, check=True)
observed = {}
for line in proc.stdout.splitlines():
    for file in json.loads(line)["files"]:
        observed[Path(file["path"]).name] = {t["id"] for t in file.get("traits", [])}
for case in spec["cases"]:
    actual = observed[Path(case["path"]).name] & set(spec["rules"])
    assert actual == set(case["expect"]), (case["path"], actual, case["expect"])
print(f"{len(spec['cases'])} HTA response/eval cases passed")
