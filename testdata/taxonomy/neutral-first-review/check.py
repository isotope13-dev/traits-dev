"""Check the saved atomscan JSONL from the first-review corpus and controls."""
import json
import sys

reports = [json.loads(line) for path in sys.argv[1:] for line in open(path) if line.strip()]
by_path = {f["path"]: f for report in reports for f in report.get("raw", {}).get("files", [])}
files = list(by_path.values())
assert files, "No scan results"

def traits(f):
    return {t["id"]: t for t in f.get("traits", []) or []}

def named(suffix):
    matches = [f for f in files if f["path"].endswith(suffix)]
    assert len(matches) == 1, (suffix, len(matches))
    return matches[0]

def clean(f):
    assert not [t for t in traits(f).values() if t["crit"] >= 4], f["path"]

for suffix in ["actions.py", "helpers.go", "near-miss.go", "browser.js", "config.lua"]:
    clean(named("neutral-first-review/" + suffix))

assert "metadata/lang/source/declaration::python-uppercase-actions-list" in traits(named("neutral-first-review/actions.py"))
expected = {
    "metadata/build/config::go-linux-only-build-constraint",
    "metadata/lang/source/declaration::register-listener-definition",
    "metadata/lang/source/declaration::go-variadic-string-builder-helper",
    "micro-behaviors/data/buffer/carve::go-named-buffer-prefix-slice",
}
assert expected <= traits(named("neutral-first-review/helpers.go")).keys()
assert not expected & traits(named("neutral-first-review/near-miss.go")).keys()

virlock = named("2026-10-19_ecb9479c8875fe9b696c1f52318052a3_elex_virlock")
assert sum(t["crit"] == 4 for t in traits(virlock).values()) >= 2
assert not any(t["crit"] == 5 for t in traits(virlock).values())
assert "micro-behaviors/mem/write/arbitrary::x86-arithmetic-immediate-store" in traits(virlock)

installer = named("2026-10-19_fc7cd05a29f77662d3c45f5d430f2b84_amadey_darkgate_elex_redline-stealer_rhadamanthys_smoke-loader_stealc_stop")
assert sum(t["crit"] == 5 for t in traits(installer).values()) >= 2
clean(named("github.laiyagushi.com-golusoris-golusoris-v0.10.1.zip"))

assets = [f for f in files if "/scratch/review/" in f["path"] and f["path"].endswith(".js") and "!!" not in f["path"]]
assert len(assets) == 8, len(assets)
for f in assets:
    clean(f)

positive = named("profile-controls/short-string-population.pe")
negative = named("profile-controls/long-string-population.pe")
profile = "metadata/file/profile/string-population::large-binary-short-max-and-average-strings"
assert profile in traits(positive)
assert profile not in traits(negative)
assert not any(t["crit"] == 5 for t in traits(positive).values())
assert sum(t["crit"] == 4 for t in traits(positive).values()) <= 1
clean(negative)

print("PASS: 3 samples, 8 isolated assets, 5 source controls, 2 PE profile controls")
