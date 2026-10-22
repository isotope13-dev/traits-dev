"""Check same-call OAEP provenance and cloud-provider counting without execution."""
import json
import os
from pathlib import Path
import re
import subprocess

cases = json.loads(Path(__file__).with_name("cases.json").read_text())["fixtures"]
for case in cases:
    expected = {rule: True for rule in case["matched"]}
    expected.update({rule: False for rule in case["not_matched"]})
    command = [os.environ.get("CLEAVE", "cleave"), "--traits-dir", ".",
               "test-rules", case["path"], "--rules", ",".join(expected)]
    result = subprocess.run(command, text=True, capture_output=True, check=True)
    actual = {match[1]: not bool(match[0]) for match in
              re.findall(r"^(NOT )?MATCHED ([^ ]+)", result.stdout, re.MULTILINE)}
    for rule, matched in expected.items():
        assert actual.get(rule) == matched, (case["path"], rule, result.stdout)
    print("PASS", case["path"])
print(f"Passed {len(cases)} cases")
