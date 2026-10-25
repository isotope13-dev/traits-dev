"""Keep the actual DLL-wipe technique while rejecting unrelated executors."""
import json
import os
from pathlib import Path
import subprocess

here = Path(__file__).resolve().parent
root = here.parents[1]
cases = {
    here / "dll-import-alias.js": True,
    here / "dll-direct-import.js": True,
    here / "dll-let-import.js": True,
    here / "dll-var-import.js": True,
    here / "dll-local-recorder.js": False,
    here / "dll-other-module.js": False,
    root / "testdata/hostile/stranded-current-review/dll-wipe.js": True,
    root / "testdata/stranded-current-review/dll-unrelated-executor.js": False,
    root / "testdata/stranded-current-review/dll-visible.js": False,
    root / "testdata/stranded-current-review/dll-logged-errors.js": False,
    root / "testdata/stranded-current-review/dll-specific-file.js": False,
}
result = subprocess.run(
    [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(root), "--json"] + list(map(str, cases)),
    capture_output=True, text=True,
)
assert result.returncode in (0, 1), result.stderr
remaining, found = result.stdout, {}
while remaining.strip():
    report, end = json.JSONDecoder(strict=False).raw_decode(remaining.lstrip())
    remaining = remaining.lstrip()[end:]
    for file in report["files"]:
        found[Path(file["path"])] = {trait["id"] for trait in file.get("traits", [])}
for path, expected in cases.items():
    for suffix in ["node-silent-system32-dll-delete-action", "node-silent-system32-dll-delete"]:
        rule = "objectives/impact/degrade/system/file::" + suffix
        assert (rule in found[path]) == expected, (path, rule, expected)
    print(path.name, "matched" if expected else "not matched", flush=True)
print("22 source assertions passed across 11 cases")
