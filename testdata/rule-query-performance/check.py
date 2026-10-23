"""Run semantic controls for the four source-query performance repairs."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
cleave = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("CLEAVE", "cleave")
cases = json.loads((HERE / "cases.json").read_text())
table_id = "metadata/lang/source/shape::javascript-literal-tables-pure-helpers"
positive_tables = {"both-record-orders.js", "forward.js", "reverse.js",
                   "sparse-arrays.js", "three-arrays.js"}
with tempfile.TemporaryDirectory(prefix="source-query-controls-") as tmp:
    paths = []
    expected = {}
    for case in cases:
        path = Path(tmp) / case["name"]
        path.write_text(case["source"])
        paths.append(str(path))
        expected[str(path)] = (case["must"], case["forbidden"])
    for path in sorted((HERE.parent / "static-table-patterns").glob("*.js")):
        paths.append(str(path))
        positive = path.name in positive_tables
        expected[str(path)] = ([table_id] if positive else [],
                               [] if positive else [table_id])
    result = subprocess.run(
        [cleave, "--traits-dir", str(REPO), "--format", "jsonl", *paths],
        check=True, capture_output=True, text=True,
    )
    seen = set()
    errors = []
    for line in result.stdout.splitlines():
        for report in json.loads(line).get("files", []):
            path = report["path"]
            if path not in expected:
                continue
            seen.add(path)
            traits = {trait["id"] for trait in report.get("traits", [])}
            must, forbidden = expected[path]
            for trait in must:
                if trait not in traits:
                    errors.append(f"{path}: missing {trait}")
            for trait in forbidden:
                if trait in traits:
                    errors.append(f"{path}: unexpected {trait}")
    errors.extend(f"missing report: {path}" for path in expected.keys() - seen)
    if errors:
        raise SystemExit("\n".join(errors))
print(f"Passed {len(expected)} source-query controls")
