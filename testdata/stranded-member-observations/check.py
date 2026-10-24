#!/usr/bin/env python3
"""Check HTTP header and Android query observations against source near misses."""
import json
from pathlib import Path
import subprocess

here = Path(__file__).resolve().parent
root = here.parent.parent
paths = [here / name for name in (
    "cache.pl", "cache-near-miss.pl", "android.py", "android-near-miss.py",
)]
output = subprocess.check_output([
    "cleave", "--traits-dir", str(root), "--format", "json", *map(str, paths),
], text=True)
decoder = json.JSONDecoder()
observed = {}
while output.strip():
    report, consumed = decoder.raw_decode(output.lstrip())
    output = output.lstrip()[consumed:]
    for file in report["files"]:
        observed[Path(file["path"]).name] = {
            trait["id"] for trait in file.get("traits", [])
        }
cache = "micro-behaviors/communications/http/header/cache::cache-control-no-cache-header"
debug = "micro-behaviors/process/debug/detect::python-android-debuggable-flag-test"
package = "micro-behaviors/os/package-manager/management::android-dumpsys-package-command"
expected = {
    "cache.pl": {cache},
    "cache-near-miss.pl": set(),
    "android.py": {debug, package},
    "android-near-miss.py": set(),
}
for name, present in expected.items():
    actual = observed[name] & {cache, debug, package}
    assert actual == present, (name, actual, present)
    print("PASS", name)
