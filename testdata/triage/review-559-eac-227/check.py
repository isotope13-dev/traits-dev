"""Check that quoted rejection is inert while separate live overrides fire."""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import json
import subprocess

base = Path(__file__).resolve().parent
root = base.parents[2]
suites = [base, base.parent / "passive-review", base.parent / "skill-override-prose"]

def check(item):
    directory, name, expected = item
    run = subprocess.run(
        ["cleave", "--traits-dir", str(root), "--format", "json", str(directory / name)],
        capture_output=True, text=True, check=True,
    )
    report = json.loads(run.stdout)
    observed = {t["id"] for f in report["files"] for t in f.get("traits", [])}
    for trait, want in expected.items():
        assert (trait in observed) == want, (name, trait, want)
    return len(expected)

items = []
for suite in suites:
    cases = json.loads((suite / "cases.json").read_text())
    for name, expected in cases.items():
        expected = {trait: want for trait, want in expected.items()
                    if suite == base or trait.endswith(("::agent-skill-tool-prior-instruction-bypass",
                                       "::skill-tool-prompt-injection-agent-hijack"))}
        if not expected:
            continue
        paths = list(suite.rglob(name)) if "/" not in name else [suite / name]
        assert len(paths) == 1, (suite, name, paths)
        items.append((suite, str(paths[0].relative_to(suite)), expected))

with ThreadPoolExecutor(max_workers=3) as pool:
    print(f"{sum(pool.map(check, items))} assertions passed")
