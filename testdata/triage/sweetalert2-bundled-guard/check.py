"""Pin the vendored-sabotage genuine-package guard at full-scan criticality.

Leniency here is disclosure, not identity. The canonical release documents
its region-differentiated behavior in its README, so both the bundling
verdict and the release verdict lift there (via the disclosed-routine
exception). An undisclosed routine sabotages its users whoever published
it, so the genuine publication without that notice stays hostile.
`unless:` is file-scoped, so the bundling rule carries a named-manifest leg
to share an evidence file (package.json) with the disclosure suppressor --
a member-.js-only rule could never see it.

These fixtures pin all three sides: a third-party package vendoring the
routine stays hostile, the undisclosed genuine publication stays hostile,
and the disclosed genuine publication keeps only a suspicious glance at
the documented routine.
"""
import json
import os
import pathlib
import subprocess

root = pathlib.Path(__file__).resolve().parents[3]
fixtures = pathlib.Path(__file__).resolve().parent

BUNDLED = "objectives/impact/ui/manipulation/browser::npm-bundled-sweetalert2-regional-sabotage"
RELEASE = "well-known/unwanted/sweetalert2-protestware::sweetalert2-npm-protestware-release"
REGIONAL = "objectives/impact/ui/manipulation/browser::regional-pointer-events-audio-sabotage"


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
assert crits(genuine, BUNDLED) == [5], genuine
assert crits(genuine, RELEASE) == [5], genuine

disclosed = top_traits("disclosed-sweetalert2.tgz")
assert crits(disclosed, BUNDLED) == [], disclosed
assert crits(disclosed, RELEASE) == [], disclosed
assert crits(disclosed, REGIONAL) == [4], disclosed

print("PASS: undisclosed bundling stays hostile; disclosed release is de-emphasized")
