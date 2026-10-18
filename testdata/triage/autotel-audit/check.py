#!/usr/bin/env python3
"""Check hashing call syntax without executing the JavaScript or the sample."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
SHA256 = "micro-behaviors/crypto/hash/digest::node-createhash-sha256-call"
HASH = "micro-behaviors/crypto/hash/digest::node-createhash-call"


def scan(engine, target):
    result = subprocess.run(
        [engine, "--traits-dir", str(ROOT), "--format", "json", str(target)],
        check=True, capture_output=True, text=True,
    )
    decoder = json.JSONDecoder()
    remaining = result.stdout.lstrip()
    files = []
    while remaining:
        report, end = decoder.raw_decode(remaining)
        files.extend(report["files"])
        remaining = remaining[end:].lstrip()
    return files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cleave", default="cleave")
    parser.add_argument("--sample", type=Path)
    args = parser.parse_args()
    cases = {
        "direct.js": ('createHash("sha256").update(value).digest("hex");', True),
        "member.js": ('crypto.createHash("sha-256");', True),
        "computed-member.js": ('crypto["createHash"]("sha256");', True),
        "escaped.js": ('crypto.createHash("sha\\x32\\x35\\x36");', True),
        "unbound.cjs": ('(0, arbitrary.createHash)("sha256").update(value).digest("hex");', True),
        "unbound.ts": ("(0, provider.createHash)('sha-256');", True),
        "different-algorithm.js": ('(0, crypto.createHash)("sha1");', True),
        "dynamic-argument.js": ('(0, crypto.createHash)(name, "sha256");', True),
        "separate-call.js": ('(0, crypto.createHash)(name); log("sha256");', True),
        "reference.js": ('const fn = (0, crypto.createHash); const algorithm = "sha256";', False),
        "wrong-method.js": ('(0, crypto.createHmac)("sha256", key);', False),
        "wrong-sequence-result.js": ('(0, crypto.createHash, other)("sha256");', False),
        "prose.js": ('// (0, crypto.createHash)("sha256");\nconst text = "(0, crypto.createHash)(\\\"sha256\\\")";', False),
    }
    with tempfile.TemporaryDirectory(prefix="autotel-audit-controls-") as directory:
        scratch = Path(directory)
        for name, (source, _) in cases.items():
            (scratch / name).write_text(source + "\n")
        files = {Path(f["path"]).name: f for f in scan(args.cleave, scratch)}
        for name, (_, expected) in cases.items():
            traits = {t["id"] for t in files[name].get("traits", [])}
            assert (HASH in traits) == expected, (name, expected, traits)
            if name in {"direct.js", "member.js", "computed-member.js", "escaped.js"}:
                assert SHA256 in traits, name
    if args.sample:
        files = scan(args.cleave, args.sample)
        for file in files:
            assert not [t for t in file.get("traits", []) if t["crit"] >= 4], file["path"]
        for suffix in ("package/dist/index.js", "package/dist/index.cjs"):
            file = next(f for f in files if f["path"].endswith(suffix))
            assert HASH in {t["id"] for t in file.get("traits", [])}, suffix
    print(f"PASS: {len(cases)} hashing controls" + (" and supplied archive" if args.sample else ""))


if __name__ == "__main__":
    main()
