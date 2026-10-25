"""Check file-body binding and distinguish browser authority from native APIs."""
import json
import os
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
UPLOAD = "micro-behaviors/communications/http/upload::csharp-file-bytes-put"
HANDLER = "metadata/lang/source/naming/interface::javascript-upload-handler-identifier"
OLD_HANDLER = "micro-behaviors/communications/http/upload::node-upload-handler"
PERMISSIONS = "micro-behaviors/os/security/webextension::extension-permissions-"

paths = sorted(HERE.glob("*.cs")) + sorted(HERE.glob("*.js"))
paths += sorted((ROOT / "testdata/hostile/cloud-managed-tasking").glob("*.cs"))
paths += sorted((ROOT / "testdata/benign/cloud-managed-tasking").glob("*.cs"))
paths += [Path(p).resolve() for p in sys.argv[1:]]
output = subprocess.check_output(
    [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT),
     "--format", "json", "analyze", *map(str, paths)], text=True,
)
decoder = json.JSONDecoder()
files = {}
while output.strip():
    report, end = decoder.raw_decode(output.lstrip())
    output = output.lstrip()[end:]
    files.update({Path(f["path"]): f for f in report["files"]})

for path in paths:
    traits = {t["id"]: t for t in files[path]["traits"]}
    assert OLD_HANDLER not in traits, path
    if path.parent == HERE:
        if path.suffix == ".cs":
            assert (UPLOAD in traits) == (path.name == "local-backup.cs"), path
        if path.name == "extension-permissions.js":
            assert all(PERMISSIONS + m in traits for m in ("request", "remove", "contains"))
        if path.name == "native-permissions.js":
            assert not any(t.startswith(PERMISSIONS) for t in traits), path
        if path.name.startswith("handler-"):
            assert HANDLER in traits, path
        assert not any(t["crit"] == 5 for t in traits.values()), path
    elif path.name == "page.js":
        # Optional outside-batch MDN permissions example, fetched with forager.
        assert PERMISSIONS + "request" in traits, path
        assert PERMISSIONS + "remove" in traits, path
    elif "/hostile/" in str(path):
        assert "objectives/command-and-control/remote-command/tasking::cloud-managed-task-results" in traits, path
    elif "/benign/" in str(path):
        assert not any(t["crit"] == 5 for t in traits.values()), path

print(f"Passed {len(paths)} file-body, permission and retained-task controls")
