"""Check parser test-corpus fixture context without executing sample code.

saferwall/pe ships password-protected ("infected") malware PEs under test/
as parser regression fixtures. Findings on those members must not convict
the vendoring library: file-scoped `unless:` removes them where the member
path keeps its directories, and `scope: archive` `downgrade:` softens them
where nesting strips ancestor directories.

Controls (all three share the same Shikata Ga Nai stub bytes):
- corpus-direct.zip holds test/direct-stub.exe: the finding is removed.
- corpus-nested.zip holds test/nest.7z holding nested-stub.exe: the finding
  survives only softened to notable at every level, never hostile/suspicious.
- plain-stub.exe sits outside any fixture directory: the finding still
  convicts at suspicious, proving the context (not the matcher) moved. It
  is scanned by relative path on purpose: invoked absolutely its path would
  run under this repo's own testdata/ tree, which is itself a fixture dir.
"""
import json
import pathlib
import subprocess

root = pathlib.Path(__file__).resolve().parents[3]
fixtures = pathlib.Path(__file__).resolve().parent


def scan(*args, cwd=None):
    result = subprocess.run(
        ["cleave", "--traits-dir", str(root), "--format", "json", *args],
        check=True, capture_output=True, text=True, cwd=cwd,
    )
    remaining = result.stdout.lstrip()
    decoder = json.JSONDecoder()
    reports = {}
    while remaining:
        report, end = decoder.raw_decode(remaining)
        remaining = remaining[end:].lstrip()
        for item in report["files"]:
            reports[pathlib.Path(item["path"]).name] = item["traits"]
    return reports


def crits(reports, name, rule_id):
    return [t["crit"] for t in reports[name] if t["id"] == rule_id]


def hot(reports, name):
    return [t for t in reports[name] if t["crit"] >= 4]


shikata = "objectives/anti-static/obfuscation/payload/encrypted::shikata-ga-nai-stub"
zips = scan(str(fixtures))
assert shikata not in {t["id"] for t in zips["corpus-direct.zip"]}, "direct"
assert not hot(zips, "corpus-direct.zip"), "direct"
assert crits(zips, "corpus-nested.zip", shikata) == [3], "nested"
assert not hot(zips, "corpus-nested.zip"), "nested"
plain = scan("plain-stub.exe", cwd=str(fixtures))
assert crits(plain, "plain-stub.exe", shikata) == [4], "plain"
print("PASS: fixture context removes direct members, softens nested ones")
