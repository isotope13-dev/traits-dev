#!/usr/bin/env python3
"""Check that a generic command response does not establish an LLM source."""

import argparse
import json
from pathlib import Path
import subprocess
import tempfile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cleave", default="../cleave/target/release/cleave")
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[2]
    body = (
        'import json, subprocess\n'
        'data = json.loads(response)["command"]\n'
        'generated_command = data\n'
        'subprocess.run(generated_command)\n'
    )
    cases = {
        "generic.py": (body, False),
        "model.py": ('api_url = "https://api.openai.com/v1/chat/completions"\n' + body, True),
    }
    generic_id = "micro-behaviors/data/parse/json::response-json-command-clues"
    model_id = "objectives/execution/interpreter/eval/generated::llm-response-command-clues"
    with tempfile.TemporaryDirectory(prefix="response-model-context-") as tmp:
        paths = []
        for name, (source, _) in cases.items():
            path = Path(tmp) / name
            path.write_text(source)
            paths.append(str(path))
        result = subprocess.run(
            [str((repo / args.cleave).resolve()), "--traits-dir", str(repo), "--format=json", *paths],
            check=True,
            capture_output=True,
            text=True,
        )
        reports = [json.loads(line) for line in result.stdout.splitlines() if line]
        roots = {Path(report["files"][0]["path"]).name: report["files"][0] for report in reports}
        assert set(roots) == set(cases), (set(roots), set(cases))
        for name, (_, expect_model) in cases.items():
            ids = {trait["id"] for trait in roots[name].get("traits", [])}
            assert generic_id in ids, (name, "missing generic JSON evidence")
            assert (model_id in ids) == expect_model, (name, "incorrect model attribution")
            print("PASS", name)


if __name__ == "__main__":
    main()
