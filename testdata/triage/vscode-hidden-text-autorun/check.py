"""Check automatic hidden-text Node launches without executing task commands."""
import copy
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
TRAIT = "objectives/execution/trigger/ide::vscode-folder-open-hidden-text-node-target"
sample = json.loads((ROOT / "testdata/hostile/vscode-task-masquerade-controls.json").read_text())
cases = []


def changed(name, expected, **fields):
    document = copy.deepcopy(sample)
    document["tasks"][0].update(fields)
    cases.append((name, document, expected))


cases.append(("original", sample, True))
changed("renamed", True, label="prepare-project", command="node ${workspaceFolder}/.cache/worker.txt")
changed("relative", True, command="node ./.stage/boot.txt")
changed("absolute", True, command="node /opt/work/.cache/boot.txt")
changed("ordinary-script", False, command="node ${workspaceFolder}/scripts/build.js")
changed("hidden-script", False, command="node ${workspaceFolder}/.deps/build.js")
changed("visible-text", False, command="node ${workspaceFolder}/scripts/build.txt")
changed("data-argument", False, command="node scripts/build.js ${workspaceFolder}/.deps/input.txt")
changed("inline-text", False, command="node -e 'console.log(123)'")
changed("manual", False, runOptions={})
changed("default-trigger", False, runOptions={"runOn": "default"})
changed("wrong-trigger-case", False, runOptions={"runOn": "FolderOpen"})
changed("different-suffix", False, command="node ${workspaceFolder}/.deps/chunk.txt.js")
changed("other-program", False, command="echo ${workspaceFolder}/.deps/chunk.txt")
changed("description-only", False, command="npm run build", description="node ${workspaceFolder}/.deps/chunk.txt")

reordered = copy.deepcopy(sample)
task = reordered["tasks"][0]
reordered["tasks"][0] = {key: task[key] for key in ("runOptions", "type", "command", "label")}
cases.append(("reverse-key-order", reordered, True))

manual = copy.deepcopy(sample["tasks"][0])
manual.pop("runOptions")
build = {"label": "build", "type": "shell", "command": "npm run build", "runOptions": {"runOn": "folderOpen"}}
cases.append(("separate-tasks", {"version": "2.0.0", "tasks": [build, manual]}, False))
cases.append(("separate-tasks-reversed", {"version": "2.0.0", "tasks": [manual, build]}, False))
cases.append(("string-task-impostor", {"tasks": [json.dumps(sample["tasks"][0], separators=(",", ":"))]}, False))
cases.append(("outside-tasks", {"example": sample["tasks"][0]}, False))
nested = copy.deepcopy(sample)
nested["tasks"][0]["command"] = "npm run build"
nested["tasks"][0]["options"] = {"command": sample["tasks"][0]["command"]}
cases.append(("nested-command", nested, False))
changed("nested-trigger", False, runOptions={"example": {"runOn": "folderOpen"}})

with tempfile.TemporaryDirectory(prefix="vscode-entry-controls-") as scratch:
    scratch = Path(scratch)
    paths = []
    for name, document, _ in cases:
        path = scratch / (name + ".json")
        path.write_text(json.dumps(document, indent=2) + "\n")
        paths.append(str(path))
    # One rules load, independent static reports for each file. Scratch paths
    # prevent generic testdata exclusions from hiding a false positive.
    result = subprocess.run(
        [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT), "--format", "json", *paths],
        capture_output=True, text=True, check=True,
        env={**os.environ, "CLEAVE_SKIP_CACHE": "1"},
    )
    remaining = result.stdout.lstrip()
    decoder = json.JSONDecoder()
    reports = {}
    while remaining:
        report, end = decoder.raw_decode(remaining)
        for file in report["files"]:
            reports[Path(file["path"]).stem] = file
        remaining = remaining[end:].lstrip()
    for name, _, expected in cases:
        traits = {t["id"]: t for t in reports[name]["traits"]}
        assert (TRAIT in traits) == expected, (name, expected, list(traits))
        if expected:
            assert traits[TRAIT]["crit"] == 5, (name, traits[TRAIT])
        else:
            assert not any(t["crit"] == 5 for t in traits.values()), (name, traits)
        print(name, "hostile" if expected else "no hostile finding")

print(f"Passed {len(cases)} hidden-text task controls")
