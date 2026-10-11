"""Check exploit and system-file distinctions without executing sample code."""
import json
import os
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parents[3]
fixtures = Path(__file__).resolve().parent
execution = "objectives/execution/activex/browser-control::"
persistence = "objectives/persistence/login/startup/folder::"
impact = "objectives/impact/degrade/system/file::"
expected = {
    "java-startup.html": {
        execution + "java-scriptlet-document-write-attempt",
        persistence + "java-scriptlet-startup-document-write-attempt",
    },
    "reset-system.html": {
        execution + "scriptlet-reset-file-write-exploit",
        impact + "scriptlet-system-files-reset-overwrite",
    },
    # A temporary destination still exploits the browser write boundary,
    # but supplies no evidence of system-file destruction.
    "temporary-output.html": {execution + "scriptlet-reset-file-write-exploit"},
    "java-no-write.html": set(),
    "system-paths-no-write.html": set(),
    "ordinary-object.html": set(),
    "commented-reset.html": set(),
}
env = dict(os.environ, CLEAVE_VALIDATE="0", CLEAVE_SKIP_CACHE="1")
result = subprocess.run(
    [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(root),
     "--format", "json", str(fixtures)],
    env=env, check=True, capture_output=True, text=True,
)
remaining = result.stdout
decoder = json.JSONDecoder()
seen = set()
while remaining.strip():
    remaining = remaining.lstrip()
    report, length = decoder.raw_decode(remaining)
    remaining = remaining[length:]
    for file in report["files"]:
        name = Path(file["path"]).name
        if name not in expected:
            continue
        actual = {trait["id"] for trait in file.get("traits", [])
                  if trait["crit"] >= 4}
        assert actual == expected[name], (name, actual, expected[name])
        seen.add(name)
assert seen == set(expected), ("Missing fixtures", set(expected) - seen)
print(f"Passed {len(seen)} Scriptlet boundary fixtures")
