"""Static mutation controls; never executes the supplied PE payload."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--sample", type=Path, required=True)
parser.add_argument("--work-dir", type=Path, required=True)
args = parser.parse_args()
original = args.sample.read_bytes()
assert hashlib.sha256(original).hexdigest() == (
    "8a370f218e0e14b026c64d66222fbfae8d1e4d197eed19e1e7a54599334c82cc"
)
args.work_dir.mkdir(parents=True, exist_ok=True)
dns = "micro-behaviors/communications/dns/lookup::"
beacon = "well-known/malware/rat/cobalt-strike/beacon::"
rules = [dns + name for name in ("dns-query-a", "dns-query-w", "dns-free", "dnsapi-lookup")]
rules.append(beacon + "dns-beacon-token-launch-formats")


def replaced(before, after):
    assert len(before) == len(after) and before in original
    return original.replace(before, after)


cases = [
    ("ansi-query", original, [True, False, True, True, True]),
    ("unicode-query", replaced(b"DnsQuery_A", b"DnsQuery_W"),
     [False, True, True, True, True]),
    # The original name remains as plain text, while DNS result cleanup is
    # still imported. Neither observation establishes a DNS query API.
    ("query-text-and-cleanup-only",
     replaced(b"DnsQuery_A", b"NotQuery_A") + b"\0DnsQuery_A\0",
     [False, False, True, False, False]),
    ("no-result-cleanup", replaced(b"DnsFree", b"NotFree"),
     [True, False, False, True, True]),
]
for name, token in (
    ("no-hex-label-template", b"%s.1%08x%08x.%x%x.%s"),
    ("no-token-diagnostic", b"%s as %s\\%s: %d"),
):
    cases.append((name, replaced(token, b"X" * len(token)),
                  [True, False, True, True, False]))

results = []
for name, data, expected in cases:
    sample = args.work_dir / (name + ".dll")
    sample.write_bytes(data)
    result = subprocess.run(
        ["cleave", "--traits-dir", ".", "test-rules", str(sample),
         "--rules", ",".join(rules)],
        capture_output=True, text=True, check=True,
    )
    actual = [any(line.startswith("MATCHED " + rule + " ")
                  for line in result.stdout.splitlines()) for rule in rules]
    (args.work_dir / (name + ".txt")).write_text(result.stdout + result.stderr)
    assert actual == expected, (name, actual, expected, result.stdout)
    results.append({"case": name, "matched": actual})
print(json.dumps({"rules": rules, "results": results}, indent=2))
