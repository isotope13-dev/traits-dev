#!/usr/bin/env python3
"""Check the YAML function-tag and dynamic-evaluator combination."""

import json
import pathlib
import subprocess
import tempfile

CASES = {
    "both": ("const t='tag:yaml.org,2002:js/function'; new Function(`return ${code}`)();\n", True),
    "tag": ("const t='tag:yaml.org,2002:js/function';\n", False),
    "function": ("new Function(`return ${code}`)();\n", False),
}

with tempfile.TemporaryDirectory() as tmp:
    for name, (source, expected) in CASES.items():
        path = pathlib.Path(tmp) / f"{name}.js"
        path.write_text(source)
        result = subprocess.check_output(
            ["../cleave/target/release/cleave", "--traits-dir", ".", "--format", "json", str(path)]
        )
        file = json.loads(result)["files"][0]
        actual = any(
            trait["id"].endswith("::yaml-function-tag-dynamic-evaluator")
            for trait in file.get("traits", [])
        )
        assert actual == expected, (name, actual, expected)

print("YAML JavaScript function-tag boundaries passed.")
