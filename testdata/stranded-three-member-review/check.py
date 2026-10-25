"""Analyze boundary fixtures statically; never execute specimen commands."""
import json
import os
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
REF = "micro-behaviors/process/debug/tool-markers::python-frida-reference"
OLD = "well-known/tool/reverse-engineering/frida::python-source-reference"
ARGV = "micro-behaviors/process/argument/positional::python-frida-argv-origin"
LIST = "micro-behaviors/metaprogramming/reflection::objection-android-component-list-command"
ANTI = "objectives/anti-analysis/debugger-detect/combined-checks::python-process-anti-analysis"
CASES = {
    "frida-launch.py": ([REF, ARGV], [OLD, LIST]),
    "frida-reassigned.py": ([REF], [OLD, ARGV]),
    "frida-reference.py": ([REF], [OLD, ARGV]),
    "frida-comments.py": ([REF], [OLD, ARGV]),
    "frida-anti-analysis.py": ([REF, ANTI], [OLD, ARGV]),
    "frida-not-identity.py": ([REF, "micro-behaviors/process/hook/keywords::inline-hook-term"], [OLD, ARGV]),
    "objection-components.py": ([LIST], [ARGV]),
    "objection-docstring.py": ([], [LIST, ARGV]),
}
env = dict(os.environ, CLEAVE_TRAITS_DIR=str(ROOT), SCAN_HOPPER="", SCAN_FETCH="none")
result = subprocess.run(
    ["atomscan", "--no-update", "--follow=none", "--analyze", "local", "--mode", "slow", "-f", "json",
     *[str(HERE / name) for name in CASES]], env=env, text=True, capture_output=True)
assert result.returncode in (0, 1), result.stderr
reports = {}
for line in result.stdout.splitlines():
    report = json.loads(line)
    file = report["raw"]["files"][0]
    reports[Path(file["path"]).name] = {t["id"] for t in file.get("traits", [])}
assert set(reports) == set(CASES), ("incomplete scan output", set(CASES) - set(reports))
checks = 0
for name, (present, absent) in CASES.items():
    ids = reports[name]
    for trait in present:
        assert trait in ids, (name, "missing", trait)
        checks += 1
    for trait in absent:
        assert trait not in ids, (name, "unexpected", trait)
        checks += 1
print(f"PASS: {checks} assertions across {len(CASES)} static boundary fixtures")
