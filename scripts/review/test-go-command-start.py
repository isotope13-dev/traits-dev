#!/usr/bin/env python3
"""Check that configuring a Go command is distinct from starting it."""

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
    setup_source = "micro-behaviors/process/create/subprocess/configure::go-inline-interpreter-command"
    run_source = "micro-behaviors/process/deploy/interpreter-command::go-inline-source-launch"
    setup_command = "micro-behaviors/process/create/subprocess/configure::go-generated-command-construction"
    run_command = "micro-behaviors/process/create/exec::go-generated-command-launch"
    cases = {}
    for label, variable, command, setup_id, run_id in [
        ("source", "pythonSource", 'exec.Command("python", "-c", pythonSource)', setup_source, run_source),
        ("command", "generatedCommand", 'exec.Command("sh", "-c", generatedCommand)', setup_command, run_command),
    ]:
        for started in (False, True):
            name = f"{label}-{'run' if started else 'setup'}.go"
            body = f'package main\nimport "os/exec"\nfunc main() {{\n  {variable} := "text"\n  cmd := {command}\n'
            body += "  _ = cmd.Run()\n}\n" if started else "  _ = cmd\n}\n"
            cases[name] = (body, setup_id, run_id, started)
    with tempfile.TemporaryDirectory(prefix="go-command-start-") as tmp:
        paths = []
        for name, (source, _, _, _) in cases.items():
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
        for name, (_, setup_id, run_id, started) in cases.items():
            ids = {trait["id"] for trait in roots[name].get("traits", [])}
            assert setup_id in ids, (name, "missing setup", setup_id)
            assert (run_id in ids) == started, (name, "incorrect launch", run_id)
            print("PASS", name)


if __name__ == "__main__":
    main()
