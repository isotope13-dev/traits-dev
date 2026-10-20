"""Check a Cleave JSON/JSONL report against the focused regression cases."""
import json
import sys
from pathlib import Path


cases = json.loads(Path(__file__).with_name("cases.json").read_text())["fixtures"]
data = Path(sys.argv[1]).read_text()
decoder = json.JSONDecoder()
reports = {}
while data.strip():
    document, end = decoder.raw_decode(data.lstrip())
    data = data.lstrip()[end:]
    for report in document["files"]:
        reports[Path(report["path"]).name] = report

for case in cases:
    name = Path(case["path"]).name
    traits = {trait["id"] for trait in reports[name].get("traits", [])}
    missing = set(case["matched"]) - traits
    unexpected = set(case["not_matched"]) & traits
    assert not missing and not unexpected, (name, missing, unexpected)
    print(f"PASS {name}")
