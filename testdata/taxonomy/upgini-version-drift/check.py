"""Check identity telemetry coverage without executing fixture code."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import zipfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PARSER = "micro-behaviors/data/parse/regex::error-array-numeric-visitor-context"
CONTEXT = "micro-behaviors/data/parse/regex::secret-rpc-error-visitor-identity-context"
UPLOAD = "micro-behaviors/communications/http/telemetry::secret-error-identity-tracking-upload-context"
PREDICATE = "metadata/file/function::hosted-notebook-predicate-name"
PROFILE = "micro-behaviors/communications/http/telemetry::python-host-profile-post-context"
CODEC = "micro-behaviors/data/codec::gzip-compression-option"
BOX = "micro-behaviors/data/format/container::item-location-box"
BLOB = "micro-behaviors/data/buffer/alloc::dom-text-content-blob-context"
WORKER = "micro-behaviors/process/create/workers::inert-script-worker-source"
RETIRED = {
    "objectives/credential-access/credential-manager/store-api::notebook-secret-error-identity-exfil",
    "objectives/credential-access/credential-manager/store-api::notebook-secret-error-identity-theft",
    "objectives/exfiltration/http/collect::notebook-gated-machine-profile-upload",
    "micro-behaviors/data/source/function/names::hosted-notebook-predicate-name",
    "micro-behaviors/data/db/snowflake::gzip-unload-option",
    "micro-behaviors/process/create/workers::worker-source-text-read",
    "objectives/exfiltration/stealer/system-info/identity::python-machine-profile-ip-exfil",
}


def check(report, path, required=(), absent=()):
    traits = [t for f in report["files"] for t in f.get("traits", [])]
    ids = {t["id"] for t in traits}
    assert set(required) <= ids, (path, "missing", set(required) - ids)
    assert not (set(absent) | RETIRED) & ids, (path, "unexpected", ids & (set(absent) | RETIRED))
    assert not [t for t in traits if t["crit"] >= 4], (path, "unjustified elevated finding")
    print(path.name, "passed", flush=True)


cases = [
    (HERE / "identity.py", [PARSER, CONTEXT], [UPLOAD, PREDICATE]),
    (HERE / "tracking.py", [], [PARSER, CONTEXT, UPLOAD]),
    (HERE / "unrelated-error.py", [], [PARSER, CONTEXT, UPLOAD]),
    (HERE / "predicate.py", [PREDICATE], [PARSER, CONTEXT, UPLOAD]),
    (HERE / "profile.py", [PROFILE], [PARSER, CONTEXT, UPLOAD]),
    (HERE / "profile-near.py", [], [PROFILE, PARSER, CONTEXT, UPLOAD]),
    (HERE / "codec.py", [CODEC], []),
    (HERE / "media-boxes.py", [BOX], []),
    (HERE / "pandas-index.py", [], [BOX]),
    (HERE / "report.html", [BLOB], [WORKER]),
    (HERE / "worker.html", [BLOB, WORKER], []),
    (HERE / "blob.html", [], [BLOB, WORKER]),
]
with tempfile.TemporaryDirectory(prefix="identity-telemetry-") as scratch:
    archive = Path(scratch) / "renamed.zip"
    with zipfile.ZipFile(archive, "w") as out:
        out.write(HERE / "identity.py", "renamed/lookup.py")
        out.write(HERE / "tracking.py", "renamed/client.py")
    cases.append((archive, [PARSER, CONTEXT, UPLOAD], [PREDICATE]))
    result = subprocess.run(
        [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT), "--format", "jsonl",
         *[str(path) for path, _, _ in cases]],
        capture_output=True, text=True,
    )
    assert result.returncode == 0, (result.stderr, result.stdout[:2000])
    reports = [json.loads(line) for line in result.stdout.splitlines() if line.strip()]
    reports_by_path = {Path(report["files"][0]["path"]).resolve(): report for report in reports}
    for path, required, absent in cases:
        check(reports_by_path[path.resolve()], path, required, absent)
print(f"{len(cases)} version-drift controls passed")
