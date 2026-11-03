#!/usr/bin/env python3
"""Check Lua compilation and invocation evidence without executing the inputs."""

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
    cleave = (repo / args.cleave).resolve()
    compile_id = "micro-behaviors/metaprogramming/generation/function::lua-loadstring-source-name-context"
    invoke_id = "micro-behaviors/process/interpreter/eval/constructed::lua-generated-source-invocation"
    direct_id = "micro-behaviors/process/interpreter/eval/constructed::lua-loadstring-result-invoked"
    cases = {
        "compile.lua": ('local model_output = "return 1"\nlocal f = loadstring(model_output)\n', {compile_id}, {direct_id, invoke_id}),
        "invoke.lua": ('local model_output = "return 1"\nloadstring(model_output)()\n', {compile_id, direct_id, invoke_id}, set()),
        "other-name.lua": ('local value = "return 1"\nloadstring(value)()\n', {direct_id}, {compile_id, invoke_id}),
        "quoted.lua": ('local model_output = "loadstring(model_output)()"\n', set(), {compile_id, direct_id, invoke_id}),
    }
    with tempfile.TemporaryDirectory(prefix="lua-generated-source-") as tmp:
        paths = []
        for name, (source, _, _) in cases.items():
            path = Path(tmp) / name
            path.write_text(source)
            paths.append(str(path))
        result = subprocess.run(
            [str(cleave), "--traits-dir", str(repo), "--format=json", *paths],
            check=True,
            capture_output=True,
            text=True,
        )
        reports = [json.loads(line) for line in result.stdout.splitlines() if line]
        roots = {Path(report["files"][0]["path"]).name: report["files"][0] for report in reports}
        assert set(roots) == set(cases), (set(roots), set(cases))
        for name, (_, required, forbidden) in cases.items():
            ids = {trait["id"] for trait in roots[name].get("traits", [])}
            assert required <= ids, (name, "missing", required - ids)
            assert not forbidden & ids, (name, "unexpected", forbidden & ids)
            print("PASS", name)


if __name__ == "__main__":
    main()
