"""Pin the vendored-sabotage genuine-package guard at full-scan criticality.

`npm-bundled-sweetalert2-regional-sabotage` is archive-scoped while `unless:`
is file-scoped, so a manifest-name guard can never fire from a member .js
bucket. The rule therefore carries an archive-scoped `downgrade:` on the
publish-root-bound sweetalert2 manifest instead. These fixtures pin both
sides: a third-party package vendoring the routine stays hostile, while the
genuine publication is de-emphasized to suspicious (its own protestware
verdicts still convict it).
"""
import json
import os
import pathlib
import subprocess

root = pathlib.Path(__file__).resolve().parents[3]
fixtures = pathlib.Path(__file__).resolve().parent

BUNDLED = "objectives/supply-chain/impersonation/clone-and-rename::npm-bundled-sweetalert2-regional-sabotage"
RELEASE = "well-known/unwanted/sweetalert2-protestware::sweetalert2-npm-protestware-release"


def top_traits(tarball):
    env = dict(os.environ, CLEAVE_SKIP_CACHE="1")
    result = subprocess.run(
        ["cleave", "--traits-dir", str(root), "--format", "json",
         str(fixtures / tarball)],
        check=True, capture_output=True, text=True, env=env,
    )
    report = json.loads(result.stdout)
    for item in report["files"]:
        if item["path"] == str(fixtures / tarball):
            return item["traits"]
    raise AssertionError("no top-level report for " + tarball)


def crits(traits, identifier):
    return [trait["crit"] for trait in traits if trait["id"] == identifier]


third_party = top_traits("third-party-bundler.tgz")
assert crits(third_party, BUNDLED) == [5], third_party
assert crits(third_party, RELEASE) == [], third_party

genuine = top_traits("genuine-sweetalert2.tgz")
assert crits(genuine, BUNDLED) == [4], genuine
assert crits(genuine, RELEASE) == [5], genuine

print("PASS: third-party bundling stays hostile; genuine release is de-emphasized")
