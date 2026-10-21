"""Check assignment placement, count thresholds, and consuming composites."""
import json
import os
import subprocess
from pathlib import Path

root = Path(__file__).resolve().parents[3]
fixtures = Path(__file__).resolve().parent
single = "metadata/lang/source/syntax/assignment::js-addition-assignment-identifier"
counted = "metadata/lang/source/syntax/assignment::four-identifier-add-assignments"
eval_rule = "micro-behaviors/process/interpreter/eval/direct::js-accumulator-eval-cooccurrence"
growth = "objectives/impact/dos/resource::counted-multiple-fill-buffer-growth"
output = "objectives/impact/dos/resource::counted-fill-growth-document-output"
cases = {
    "four.js": ({single, counted}, {eval_rule, growth, output}),
    "three.js": ({single}, {counted, eval_rule, growth, output}),
    "near-miss.js": (set(), {single, counted, eval_rule, growth, output}),
    # The existing JavaScript-specific query does not parse script children
    # of a real HTML file. Retain and document that preexisting boundary.
    "four.html": (set(), {single, counted}),
    "accumulator.js": ({single, eval_rule}, {counted, growth, output}),
    "fill-growth.js": ({single, counted, growth, output}, {eval_rule}),
}
result = subprocess.run(
    [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(root),
     "--format", "json", *[str(fixtures / name) for name in cases]],
    check=True, capture_output=True, text=True,
)
remaining = result.stdout
reports = []
decoder = json.JSONDecoder()
while remaining.strip():
    report, length = decoder.raw_decode(remaining.lstrip())
    remaining = remaining.lstrip()[length:]
    reports.append(report)
assert len(reports) == len(cases), len(reports)
retired = {
    "micro-behaviors/data/arithmetic::js-addition-assignment-identifier",
    "metadata/file/arithmetic::four-identifier-add-assignments",
}
for (name, (expected, absent)), report in zip(cases.items(), reports):
    ids = {trait["id"] for file in report["files"] for trait in file["traits"]}
    assert expected <= ids, (name, "missing", expected - ids)
    assert not (absent | retired) & ids, (name, "unexpected", (absent | retired) & ids)
print("Six assignment placement and consumer controls passed")
