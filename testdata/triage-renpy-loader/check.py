"""Analyze inert source fixtures; never import or execute them."""
import json
import pathlib
import subprocess


ROOT = pathlib.Path(__file__).resolve().parents[2]
FIXTURES = pathlib.Path(__file__).resolve().parent
ARCHIVE = "objectives/execution/payload/file-exec::obfuscated-zip-forfiles-launcher"
ZONE = "objectives/evasion/security-bypass/policy/execution::local-zone-record-with-forfiles-launch"
OPEN = "micro-behaviors/fs/file/open::python-zone-stream-open-write"
WRITE = "micro-behaviors/fs/write/content::python-write-local-zone-record"
EVAL = "micro-behaviors/process/interpreter/eval/direct::eval-builtin"
RETIRED = {
    "objectives/execution/interpreter/eval/remote::config-string-execution",
    "objectives/execution/interpreter/eval/remote::eval-config-access-1",
    "objectives/execution/interpreter/eval/remote::eval-config-access-2",
    "objectives/execution/interpreter/eval/remote::eval-config-access",
    "objectives/command-and-control/backdoor/dispatch/eval::remote-config-eval",
    "objectives/command-and-control/backdoor/dispatch/eval::client-config-execution",
}
CASES = {
    "launcher.py": ({ARCHIVE, ZONE, OPEN, WRITE}, set()),
    "read-zone.py": ({ARCHIVE, WRITE}, {ZONE, OPEN}),
    "internet-zone.py": ({ARCHIVE, OPEN}, {ZONE, WRITE}),
    "no-command.py": ({OPEN, WRITE}, {ARCHIVE, ZONE}),
    "plain-launch.py": ({ZONE, OPEN, WRITE}, {ARCHIVE}),
    "local-menu.py": ({EVAL}, {ARCHIVE, ZONE}),
    "renamed-field.py": ({EVAL}, {ARCHIVE, ZONE}),
    "quoted-eval.py": (set(), {EVAL, ARCHIVE, ZONE}),
}


def main():
    result = subprocess.run(
        ["cleave", "--traits-dir", str(ROOT), "--format", "jsonl"]
        + [str(FIXTURES / name) for name in CASES],
        cwd=ROOT, capture_output=True, text=True,
    )
    if result.returncode or result.stderr.strip():
        raise AssertionError(result.stderr)
    decoder = json.JSONDecoder()
    remaining = result.stdout
    checked = set()
    while remaining.strip():
        remaining = remaining.lstrip()
        report, end = decoder.raw_decode(remaining)
        remaining = remaining[end:]
        for file in report["files"]:
            name = pathlib.Path(file["path"]).name
            matched = {trait["id"] for trait in file.get("traits", [])}
            required, forbidden = CASES[name]
            assert required <= matched, (name, "missing", required - matched)
            assert not matched & (forbidden | RETIRED), (name, "unexpected", matched & (forbidden | RETIRED))
            if name in {"local-menu.py", "renamed-field.py", "quoted-eval.py"}:
                assert not any(t.get("crit", 0) >= 4 for t in file.get("traits", [])), name
            checked.add(name)
    assert checked == set(CASES), checked
    print(f"{len(checked)} fixture controls passed")


if __name__ == "__main__":
    main()
