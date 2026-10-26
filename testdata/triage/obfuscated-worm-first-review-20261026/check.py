"""Scan regression data; never execute the JavaScript. Run from any directory."""
import json, os, subprocess, tempfile
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CLEAVE = os.environ.get("CLEAVE", "cleave")
cases = json.loads((HERE / "cases.json").read_text())
paths = [str(HERE / row["file"]) for row in cases]
result = subprocess.run([CLEAVE, "--traits-dir", str(ROOT), "--format", "json", *paths], capture_output=True, text=True, check=True)
decoder, remaining, files = json.JSONDecoder(), result.stdout, []
while remaining.strip():
    remaining = remaining.lstrip()
    report, end = decoder.raw_decode(remaining)
    files.extend(report.get("files", []))
    remaining = remaining[end:]
failures = []
for row in cases:
    matched = [f for f in files if f["path"] == str(HERE / row["file"])]
    traits = {t["id"]: t for f in matched for t in f.get("traits", [])}
    missing = set(row["matched"]) - traits.keys()
    unwanted = set(row["not_matched"]) & traits.keys()
    high = [id for id,t in traits.items() if t["crit"] >= 4] if row["no_high_findings"] else []
    if missing or unwanted or high:
        failures.append({"file":row["file"],"missing":sorted(missing),"unexpected":sorted(unwanted),"high":high})
if failures:
    raise SystemExit(json.dumps(failures, indent=2))
# Reproduce the unrelated-byte-array false chain without checking in megabytes.
with tempfile.TemporaryDirectory() as tmp:
    path=Path(tmp)/"generated.js"
    path.write_text("const data=["+",".join(str(i%256) for i in range(450000))+"];\n"+(HERE/"code-generator.js").read_text())
    output=subprocess.run([CLEAVE,"--traits-dir",str(ROOT),"--format","json",str(path)],capture_output=True,text=True,check=True)
    report=json.loads(output.stdout)
    high=[t["id"] for f in report["files"] for t in f.get("traits",[]) if t["crit"]>=4]
    assert not high, high
print("PASS",len(cases),"fixtures and large unrelated-byte-array control")
