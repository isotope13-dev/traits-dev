#!/usr/bin/env python3
"""Run the Roblox behavior-boundary matrix against a pinned Cleave engine."""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def run(cleave, traits_dir, args):
    env = {**os.environ, "CLEAVE_SKIP_CACHE": "1"}
    return subprocess.run(
        [cleave, "--no-update-check", "--traits-dir", str(traits_dir),
         "--disable", "yara,radare2,upx", *args],
        text=True, capture_output=True, check=True, env=env,
    )


def match_states(output, expected_ids):
    states = {}
    for rule_id in expected_ids:
        matches = re.findall(r"^(MATCHED|NOT MATCHED) " + re.escape(rule_id) + r" \(", output, re.M)
        assert len(matches) == 1, (rule_id, matches, output)
        states[rule_id] = matches[0]
    return states


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cleave", required=True)
    parser.add_argument("--traits-dir", type=Path, required=True,
                        help="Isolated root containing metadata/, micro-behaviors/, objectives/, and well-known/ only")
    parser.add_argument("--cases", type=Path, default=Path(__file__).with_name("cases.json"))
    parser.add_argument("--record", type=Path)
    args = parser.parse_args()
    cases = json.loads(args.cases.read_text())
    cleave = shutil.which(args.cleave)
    assert cleave, f"Missing Cleave executable: {args.cleave}"
    traits_dir = args.traits_dir.resolve()
    assert {p.name for p in traits_dir.iterdir() if p.is_dir()} == {
        "metadata", "micro-behaviors", "objectives", "well-known"
    }

    results = []
    with tempfile.TemporaryDirectory(prefix="h4-roblox-") as tmp:
        tmp = Path(tmp)
        assert not any(marker in tmp.name.lower() for marker in ("test", "case"))
        for case in cases["fixtures"]:
            archive = ROOT / case["path"]
            assert archive.is_file(), archive
            result = run(cleave, traits_dir, ["--format", "json", str(archive)])
            report = json.loads(result.stdout)
            root_file = next(f for f in report["files"] if f["path"] == str(archive))
            emitted = {t["id"] for t in root_file.get("traits", [])}
            for rule_id in case["archive_required_emitted"]:
                assert rule_id in emitted, (case["id"], "required archive finding missing", rule_id)
            for rule_id in case["archive_forbidden_emitted"]:
                assert rule_id not in emitted, (case["id"], "forbidden archive finding present", rule_id)

            trace_ids = list(case.get("archive_rule_traces", {}))
            archive_trace = ""
            archive_states = {}
            if trace_ids:
                traced = run(cleave, traits_dir,
                             ["test-rules", str(archive), "--rules", ",".join(trace_ids)])
                archive_trace = traced.stdout + traced.stderr
                archive_states = match_states(archive_trace, trace_ids)
                assert archive_states == case["archive_rule_traces"], (case["id"], archive_states)

            member_results = []
            for member_case in case.get("member_checks", []):
                member = member_case["member"]
                with zipfile.ZipFile(archive) as zf:
                    assert member in zf.namelist(), (case["id"], member)
                    member_path = tmp / case["id"] / member
                    member_path.parent.mkdir(parents=True, exist_ok=True)
                    member_path.write_bytes(zf.read(member))
                rule_ids = list(member_case["rules"])
                traced = run(cleave, traits_dir,
                             ["test-rules", str(member_path), "--rules", ",".join(rule_ids)])
                output = traced.stdout + traced.stderr
                states = match_states(output, rule_ids)
                assert states == member_case["rules"], (case["id"], member, states)
                member_results.append({"member": member, "rule_states": states})

            results.append({
                "id": case["id"],
                "fixture": case["path"],
                "fixture_sha256": sha256(archive),
                "archive_risk": root_file.get("risk"),
                "archive_emitted": sorted(emitted),
                "archive_rule_trace_states": archive_states,
                "archive_rule_trace": archive_trace,
                "member_rule_states": member_results,
            })
    evidence = {
        "status": "passed focused static matcher assertions; synthetic specimens only",
        "cleave": subprocess.run([cleave, "version"], capture_output=True, text=True, check=True).stdout.strip(),
        "cleave_sha256": sha256(cleave),
        "traits_dir": str(traits_dir),
        "trait_yaml_count": sum(1 for p in traits_dir.rglob("*.yaml")),
        "cases_sha256": sha256(args.cases),
        "results": results,
    }
    serialized = json.dumps(evidence, indent=2, sort_keys=True) + "\n"
    if args.record:
        args.record.write_text(serialized)
    print(serialized, end="")


if __name__ == "__main__":
    main()
