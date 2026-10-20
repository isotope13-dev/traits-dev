# /// script
# dependencies = ["pyyaml", "yara-x"]
# ///
"""Run with uv run check.py <session-root>; never contacts sample endpoints."""
import ast
import builtins
import code
import concurrent.futures
import json
import os
import re
from pathlib import Path
import subprocess
import sys
from types import SimpleNamespace

import yaml
import yara_x

root = Path(sys.argv[1])
scratch = root / "scratch/fallout-first-review/controls"
scratch.mkdir(parents=True, exist_ok=True)
go_sample = root / "samples/29d4d4ea447b/control-no-raton-helper.exe"
py_sample = root / "extract/528084/pyyi/cli.py"
rule = yaml.safe_load(Path("micro-behaviors/os/registry/write/go-native-string.yaml").read_text())
scanner = yara_x.compile(rule["traits"][0]["if"]["source"])
b = go_sample.read_bytes()
write = bytes.fromhex("48 89 08 48 8b 4c 24 70 48 89 48 08 48 c7 40 10")
site = b.index(write)
run_path = b"Software\\Microsoft\\Windows\\CurrentVersion\\Run"
run_at = b.index(run_path)
cases = [("original", b, True)]
for name, offset, value in [
    ("wrong-value-type", site + 24, b"\x04"),
    ("nonzero-reserved", site + 16, b"\x01"),
    ("wrong-api-object", site + 51, b"\x00\x00\x00\x00"),
    ("wrong-run-path", run_at + len(run_path) - 3, b"Tmp"),
]:
    changed = bytearray(b)
    changed[offset:offset + len(value)] = value
    cases.append((name, bytes(changed), False))
upper = bytearray(b)
upper[run_at:run_at + len(run_path)] = run_path.upper()
cases.append(("case-variant", bytes(upper), True))
for name, data, expected in cases:
    actual = bool(scanner.scan(data).matching_rules)
    assert actual == expected, (name, actual, expected)
    print("PASS native", name)

source = py_sample.read_text()
# Evaluate only the two class definitions, with every remote/state helper
# replaced. No sample top-level statements or HTTP helpers execute.
sent = []
namespace = {
    "code": code, "builtins": builtins,
    "sys": SimpleNamespace(stdin=SimpleNamespace(isatty=lambda: True)),
    "_WORD_RE": re.compile(r"[A-Za-z0-9_@#$%^&*!?+-]+"),
    "_PLAIN_RE": re.compile(r"[A-Za-z_]"), "_SKIP_WORDS": {"help"},
    "_GATE_TRIES": 5, "_quiet_config": lambda: {"server": "mock"},
    "_server_unlock": lambda cfg, word: sent.append(word) or {"status": 403},
    "_real_ok": lambda answer: False, "_server_broken": lambda answer: False,
    "_rekey": lambda cfg, word: None, "out": lambda msg: None,
}
nodes = [n for n in ast.parse(source).body
         if isinstance(n, ast.ClassDef) and n.name in ("_Veil", "_GateConsole")]
exec(compile(ast.Module(body=nodes, type_ignores=[]), "<class-only-test>", "exec"), namespace)
console = namespace["_GateConsole"]()
for word in ("captured_one", "captured_two", "captured_three", "captured_four", "captured_five", "sixth"):
    console.push(word)
assert sent == ["captured_one", "captured_two", "captured_three", "captured_four", "captured_five"]
print("PASS behavior: first five console tokens reach remote validation")
relay = "objectives/exfiltration/stealer/input::python-repl-input-password-relay"
export = "objectives/exfiltration/stealer/input::python-covert-repl-input-export"
payload = "objectives/command-and-control/dropper/script-eval/response-eval/remote-body-exec::urllib-base64-gzip-response-payload-exec"
cases = [
    ("numeric-operation", source, {relay, export, payload}),
    ("string-operation", source.replace("api_json(cfg, 2,", 'api_json(cfg, "check",'), {relay, export, payload}),
    ("different-input", source.replace("_server_unlock(cfg, s)", '_server_unlock(cfg, "fixed")'), {payload}),
    ("different-field", source.replace('"password": pw', '"message": pw'), {payload}),
    ("no-cbreak", source.replace("tty.setcbreak(fd)", "print(fd)"), {relay, payload}),
    ("honest-failure", source.replace("\n            _py_no_such_file(argv)", '\n            print("module failed")').replace("\n    _py_no_such_file(argv)", '\n    print("module failed")'), {relay, export}),
]


def check_python(case):
    name, text, expected = case
    target = scratch / (name + ".py")
    target.write_text(text)
    ast.parse(text)
    result = subprocess.run(
        ["cleave", "--traits-dir", ".", "--format", "json", str(target)],
        text=True, capture_output=True, check=True,
        env={**os.environ, "CLEAVE_SKIP_YARA_CACHE": "1"},
    )
    report = json.loads(result.stdout)
    ids = {t["id"] for f in report["files"] for t in f.get("traits", [])}
    actual = ids & {relay, export, payload}
    assert actual == expected, (name, actual, expected, result.stderr)
    return "PASS python " + name


with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    for result in pool.map(check_python, cases):
        print(result)
print("12 detection controls and 1 behavior check passed")
