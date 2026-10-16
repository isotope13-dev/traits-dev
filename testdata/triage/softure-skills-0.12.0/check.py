"""Check auth-name boundaries and neutral no-reply address placement.

Generated controls are scanned as data outside test-named paths, never executed.
Usage: python3 check.py --out /tmp/softure-controls --cleave /path/to/cleave
"""
import argparse
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[3]
AUTH = "micro-behaviors/data/property/assign::auth-token-variable-assignment-source"
SHELL_AUTH = "micro-behaviors/data/property/assign::auth-token-shell-assignment"
ADDRESS = "micro-behaviors/communications/email/address::no-reply-address-text"
OLD = "objectives/credential-access/phishing/mfa-relay::noreply-sender-address"
CONSUMER = "objectives/credential-access/phishing/mfa-relay::mailbox-notification-filter"
SELECTED = {AUTH, SHELL_AUTH, ADDRESS, OLD, CONSUMER}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--cleave", default=os.environ.get("CLEAVE", "cleave"))
    args = parser.parse_args()
    directory = args.out / "inputs"
    directory.mkdir(parents=True, exist_ok=True)
    cases = []
    positive = ["AUTH", "AUTHORIZATION", "API_AUTH", "API_AUTH_HEADER",
                "API_TOKEN", "TOKENS", "ACCESS_TOKEN_VALUE"]
    negative = ["AUTHOR", "COAUTHOR", "AUTHOR_INFO", "COAUTHOR_NAME",
                "AUTHENTICATOR", "AUTHORITY"]
    for extension in ["py", "js", "sh"]:
        trait = SHELL_AUTH if extension == "sh" else AUTH
        for name in positive + negative:
            prefix = "const " if extension == "js" else ""
            source = f'{prefix}{name}="provided-value"\n'
            cases.append((f"{name.lower()}.{extension}", source,
                          {trait} if name in positive else set()))
    coauthor = 'COAUTHOR = "Co-Authored-By: Assistant <noreply@example.org>"\n'
    cases.extend([
        ("coauthor-address.py", coauthor, {ADDRESS}),
        ("coauthor-with-real-token.py", coauthor + 'API_TOKEN = input()\n', {AUTH, ADDRESS}),
        ("no-reply-variant.py", 'sender = "NO-REPLY@example.org"\n', {ADDRESS}),
        ("ordinary-address.py", 'sender = "reply@example.org"\n', set()),
        # Scope preservation: the moved atom was Python-only.
        ("address-outside-scope.js", 'const sender = "noreply@example.org";\n', set()),
        # Existing objective consumer keeps its evidence after the move.
        ("existing-consumer.py", 'sender = {"from": "noreply@example.org"}\n', {ADDRESS, CONSUMER}),
        ("placeholder.py", 'API_TOKEN=<key>\n', set()),
        ("tls-policy.py", 'NODE_TLS_REJECT_UNAUTHORIZED = "0"\n', set()),
        ("lexical-token.js", 'const CSS_TOKEN_PATTERN = /name/;\n', set()),
    ])
    for name, source, _ in cases:
        (directory / name).write_text(source)
    result = subprocess.run(
        [args.cleave, "--traits-dir", str(ROOT), "--no-update-check", "--format", "jsonl", str(directory)],
        capture_output=True, text=True, timeout=600, check=True,
        env={**os.environ, "CLEAVE_SKIP_CACHE": "1", "RAYON_NUM_THREADS": "2"},
    )
    (args.out / "scan.jsonl").write_text(result.stdout)
    reports = {}
    for line in result.stdout.splitlines():
        doc = json.loads(line)
        for report in doc.get("files", [doc] if "path" in doc else []):
            if "!!" not in report["path"]:
                reports[Path(report["path"]).name] = report
    results = []
    for name, _, expected in cases:
        observed = {t["id"] for t in reports[name]["traits"]} & SELECTED
        assert observed == expected, (name, sorted(observed), sorted(expected))
        results.append({"case": name, "passed": True, "matched": sorted(observed)})
    (args.out / "results.json").write_text(json.dumps(results, indent=2) + "\n")
    print(f"Passed {len(results)} auth-boundary, address-placement and consumer controls")


if __name__ == "__main__":
    main()
