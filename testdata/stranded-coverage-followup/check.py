"""Check static detector boundaries without executing fixture code."""
import json
import os
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
ARGV = "micro-behaviors/process/argument/positional::python-{}-argv-origin"
DESKTOP = "micro-behaviors/fs/directory/readdir::desktop-file-enumeration"
DOCUMENTS = "micro-behaviors/fs/directory/readdir::documents-file-enumeration"
SHORTCUT = "metadata/lang/source/literal::lnk-glob-pattern-source"
DESCRIPTOR = "metadata/binary/symbols/descriptor::jvm-file-filter-array-descriptor"
INFECTOR = "objectives/impact/infect/lnk::lnk-shortcut-infector-source"
LISTING = "micro-behaviors/fs/directory/readdir::directory-listing-evidence"
TOOLS = [ARGV.format("adb"), ARGV.format("objection")]
CASES = {
    "tools-argv.py": (TOOLS, []),
    "tools-data-argument.py": (TOOLS, []),
    "tools-unrelated.py": ([], TOOLS),
    "tools-reassigned.py": ([], TOOLS),
    "listing.applescript": ([DESKTOP, DOCUMENTS], []),
    "listing-embedded.sh": ([DOCUMENTS], [DESKTOP]),
    "listing-near-miss.applescript": ([], [DESKTOP, DOCUMENTS]),
    "shortcut-pattern.cpp": ([SHORTCUT], []),
    "shortcut-filter.cpp": ([], [SHORTCUT, INFECTOR]),
    "shortcut-rewrite.cpp": ([SHORTCUT, INFECTOR], []),
    "FilterDescriptor.class": ([DESCRIPTOR], []),
    "OrdinaryDescriptor.class": ([], [DESCRIPTOR]),
}
result = subprocess.run(
    ["atomscan", "--no-update", "--follow=none", "--analyze", "local",
     "--mode", "slow", "-f", "json", *[str(HERE / name) for name in CASES]],
    env=dict(os.environ, CLEAVE_TRAITS_DIR=str(ROOT)), text=True, capture_output=True,
)
# A deliberately hostile control produces atomscan's nonzero alert status.
assert result.returncode in (0, 1, 2), (result.returncode, result.stderr)
reports = {}
for line in result.stdout.splitlines():
    file = json.loads(line)["raw"]["files"][0]
    reports[Path(file["path"]).name] = {t["id"] for t in file.get("traits", [])}
checks = 0
for name, (present, absent) in CASES.items():
    assert set(present) <= reports[name], (name, "missing", set(present) - reports[name])
    assert not set(absent) & reports[name], (name, "unexpected", set(absent) & reports[name])
    checks += len(present) + len(absent)
for name in ["listing.applescript", "shortcut-pattern.cpp", "FilterDescriptor.class"]:
    # Baseline selector findings may be omitted from atomscan's rendered JSON.
    debug = subprocess.run(
        ["cleave", "--traits-dir", str(ROOT), "test-rules", str(HERE / name),
         "--rules", LISTING], text=True, capture_output=True,
    )
    assert debug.returncode == 0, debug.stderr
    assert f"MATCHED {LISTING}" in debug.stdout, (name, debug.stdout, debug.stderr)
    checks += 1
print(f"PASS: {checks} assertions across {len(CASES)} static boundary fixtures")
