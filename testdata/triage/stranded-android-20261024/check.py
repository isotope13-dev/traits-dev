"""Assert focused boundaries from an atomscan JSONL report; never run fixtures."""
import json
from pathlib import Path
import sys

cases = json.loads(Path(__file__).with_name("cases.json").read_text())
observed = {}
for line in Path(sys.argv[1]).read_text().splitlines():
    report = json.loads(line)
    file = report["raw"]["files"][0]
    observed[Path(file["path"]).name] = {t["id"] for t in file.get("traits", [])}
for name, case in cases.items():
    traits = observed[name]
    missing = set(case.get("matched", [])) - traits
    unexpected = set(case.get("not_matched", [])) & traits
    assert not missing and not unexpected, (name, missing, unexpected)
    print("PASS", name)
