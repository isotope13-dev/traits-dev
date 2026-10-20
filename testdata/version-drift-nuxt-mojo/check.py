"""Check neutral inventory placement, execution evidence and retained consumers."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import tempfile


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cleave", default="cleave")
    parser.add_argument("--work-dir")
    args = parser.parse_args()
    fixtures = Path(__file__).resolve().parent
    root = fixtures.parent.parent
    s3 = "micro-behaviors/communications/http/services/aws-s3::"
    old = "objectives/discovery/cloud/permissions::aws-s3-"
    setup = "metadata/build/pip::root-setup-py-path"
    cases = {
        "inventory.py": ([s3 + "s3-permission-surface-enumeration"], [], 3),
        "read-only.py": ([s3 + "s3-permission-read-operation"],
                         [s3 + "s3-permission-surface-enumeration"], 3),
        "list-only.py": ([s3 + "s3-list-buckets-operation"],
                         [s3 + "s3-permission-surface-enumeration"], 3),
        "references.py": ([], [s3 + name for name in (
            "s3-list-buckets-operation", "s3-permission-read-operation",
            "s3-set-public-access-block")], 3),
        "public-access-update.py": ([s3 + "s3-set-public-access-block"], [], 3),
        "aws_setup.py": ([], [setup], 3),
        "setup.py": ([setup], [], 3),
        "prefix.js": ([s3 + "s3-prefix-scoped-bucket-lookup"], [], 3),
        "unscoped.js": ([s3 + "s3-list-buckets-unscoped-call"],
                        [s3 + "s3-prefix-scoped-bucket-lookup"], 3),
        "role-inventory.py": ([s3 + "s3-permission-surface-enumeration",
            "objectives/discovery/cloud/permissions::aws-cross-account-s3-permission-enumeration"], [], 4),
    }
    # Analyze copies outside testdata: the existing file-local test-directory
    # exclusion is deliberately preserved by this migration.
    with tempfile.TemporaryDirectory(prefix="inventory-controls-", dir=args.work_dir) as work:
        paths = []
        for name in cases:
            target = Path(work) / name
            shutil.copyfile(fixtures / name, target)
            paths.append(str(target))
        result = subprocess.run(
            [args.cleave, "--traits-dir", str(root), "--json", *paths],
            capture_output=True, text=True, check=True)
        assert "failed" not in result.stderr.lower(), result.stderr
        reports = [json.loads(line) for line in result.stdout.splitlines() if line.strip()]
        assert len(reports) == len(cases), len(reports)
        for report in reports:
            name = Path(report["files"][0]["path"]).name
            required, forbidden, max_crit = cases[name]
            traits = {t["id"]: t["crit"] for f in report["files"] for t in f.get("traits", [])}
            assert set(required) <= traits.keys(), (name, "missing", set(required) - traits.keys())
            assert not set(forbidden) & traits.keys(), (name, "unexpected", set(forbidden) & traits.keys())
            assert not any(t.startswith(old) for t in traits), (name, "retired ID")
            assert max(traits.values(), default=0) <= max_crit, (name, traits)
    print(f"{len(cases)} inventory, call/reference and filename controls passed")


if __name__ == "__main__":
    main()
