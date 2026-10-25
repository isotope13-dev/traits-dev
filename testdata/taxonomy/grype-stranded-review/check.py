#!/usr/bin/env python3
"""Check neutral CI execution and compiled SHA-256 coverage."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CLEAVE = os.environ.get("CLEAVE", "cleave")
PIPE = "micro-behaviors/process/deploy/interpreter-stdin::gha-run-curl-pipe-shell"
OLD_PIPE = "objectives/supply-chain/trojanized/ci-pipeline::gha-run-curl-pipe-shell"
DIGEST = "micro-behaviors/crypto/hash/digest::go-sha256-pclntab"
INJECTION = "objectives/execution/exploit/command-injection::gha-comment-body-run"


def scan(path):
    result = subprocess.run(
        [CLEAVE, "--traits-dir", str(ROOT), "--json", str(path)],
        check=True, capture_output=True, text=True,
    )
    report = json.loads(result.stdout)
    return {t["id"]: t for t in report["files"][0].get("traits", [])}


with tempfile.TemporaryDirectory(prefix="grype-rule-controls-") as tmp:
    tmp = Path(tmp)
    for filename in ("installer.yml", "untrusted-run.yml", "download-only.yml"):
        # Path-based fixture suppression must not hide the untrusted-input leg.
        path = tmp / filename
        shutil.copyfile(HERE / filename, path)
        traits = scan(path)
        assert OLD_PIPE not in traits, filename
        if filename == "download-only.yml":
            assert PIPE not in traits
        else:
            assert traits[PIPE]["crit"] == 3, filename
        if filename == "untrusted-run.yml":
            assert traits[INJECTION]["crit"] == 4
        else:
            assert not any(t["crit"] >= 4 for t in traits.values()), filename

    env = dict(os.environ, GOOS="linux", GOARCH="amd64", CGO_ENABLED="0")
    for filename, expected in (("digest.go", True), ("digest-name-only.go", False)):
        path = tmp / (filename + ".elf")
        subprocess.run(["go", "build", "-o", str(path), str(HERE / filename)],
                       check=True, env=env)
        traits = scan(path)
        assert (DIGEST in traits) == expected, filename

    for filename in ("gha-pipe-stage-controls.tar", "gha-test-canary-controls.tar"):
        traits = scan(ROOT / "testdata" / "benign" / filename)
        assert not any(t["crit"] >= 4 for t in traits.values()), filename

for filename in (
    "gha-marrowworks-workflow-inject-linux.tgz",
    "gha-basaltbyte-token-exfil-linux.tgz",
):
    traits = scan(ROOT / "testdata" / "hostile" / "supply-chain-corpus" / "gha" / filename)
    assert any(t["crit"] == 5 for t in traits.values()), filename

server = "metadata/file/catalog/service::java-app-server-name-reference"
trace = subprocess.run(
    [CLEAVE, "--traits-dir", str(ROOT), "test-rules",
     str(HERE / "service-names.c"), "--rules", server],
    check=True, capture_output=True, text=True,
)
assert "MATCHED " + server in trace.stdout
assert not any(t["crit"] >= 4 for t in scan(HERE / "service-names.c").values())
assert scan(HERE / "service-stop.c")[
    "objectives/impact/degrade/services::native-service-stop-status"
]["crit"] == 4

print("CI pipeline, attack-input, SHA-256, and retained attack controls passed")
