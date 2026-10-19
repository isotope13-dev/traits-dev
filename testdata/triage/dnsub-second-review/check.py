"""Keep PowerShell concealment tied to the launched call, using static scans."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[3]
PADDED = "objectives/anti-static/obfuscation/instruction/insertion-junk::go-whitespace-padded-powershell-launch"
GENERIC = "objectives/anti-static/obfuscation/instruction/insertion-junk::go-extreme-inline-whitespace-run"
HOSTILE = {
    "objectives/execution/payload/file-exec::go-powershell-certutil-stage",
    "objectives/evasion/security-bypass/policy/execution::go-hidden-powershell-policy-bypass",
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--work-dir", type=Path, required=True)
    parser.add_argument("--cleave", default="cleave")
    args = parser.parse_args()
    args.work_dir.mkdir(parents=True, exist_ok=True)
    fixture = (ROOT / "testdata/hostile/go-powershell-certutil-stager.go").read_text()
    command = next(line.strip() for line in fixture.splitlines() if "exec.Command" in line)
    visible = re.sub(r" {500,}", " ", command)
    padded_echo = 'exec.Command' + ' ' * 600 + '("echo", "hello").Run()'
    cases = []

    def case(name, body, required=(), forbidden=()):
        cases.append((name, 'package main\nimport "os/exec"\nfunc main() {\n' + body + '\n}\n',
                      set(required), set(forbidden)))

    case("padded-run", command, HOSTILE | {PADDED}, {GENERIC})
    for method in ("Start", "Output", "CombinedOutput"):
        case("padded-" + method, command.replace(".Run()", f".{method}()"), HOSTILE | {PADDED})
    case("visible-launch", visible, forbidden=HOSTILE | {PADDED, GENERIC})
    case("unrelated-padded-call", padded_echo + '\n' + visible, {GENERIC}, HOSTILE | {PADDED})
    case("unrelated-padding-before", padded_echo + '\n' + visible + '\n' + padded_echo,
         {GENERIC}, HOSTILE | {PADDED})
    case("constructor-only", command.replace(".Run()", ""), {GENERIC}, HOSTILE | {PADDED})
    case("unrelated-run", command.replace(".Run()", "") + '\nexec.Command("echo").Run()',
         {GENERIC}, HOSTILE | {PADDED})
    case("program-is-argument", command.replace('("powershell",', '("echo", "powershell",', 1),
         {GENERIC}, HOSTILE | {PADDED})
    case("comment-only", "// " + command, forbidden=HOSTILE | {PADDED, GENERIC})
    case("below-padding-threshold", re.sub(r" {500,}", " " * 499, command),
         forbidden=HOSTILE | {PADDED, GENERIC})

    def scan(item):
        name, source, required, forbidden = item
        path = args.work_dir / (name + ".go")
        path.write_text(source)
        result = subprocess.run([args.cleave, "--traits-dir", str(ROOT), "--format", "json", str(path)],
                                capture_output=True, text=True, check=True)
        report = json.loads(result.stdout)
        found = {t["id"] for f in report["files"] for t in f.get("traits", [])}
        assert required <= found, (name, "missing", sorted(required - found))
        assert not forbidden & found, (name, "unexpected", sorted(forbidden & found))
        return {"case": name, "passed": True}

    with ThreadPoolExecutor(max_workers=3) as pool:
        results = list(pool.map(scan, cases))
    (args.work_dir / "results.json").write_text(json.dumps(results, indent=2) + "\n")
    print(f"Passed {len(results)} static controls")


if __name__ == "__main__":
    main()
