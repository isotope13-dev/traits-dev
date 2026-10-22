"""Check prompt content coverage outside fixture-path exclusions; never run it."""
import concurrent.futures
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
PREFIX = "objectives/evasion/security-bypass/llm/override::"
PAIR = PREFIX + "llm-jailbreak-system-extraction"
EXTRACTION = PREFIX + "llm-system-prompt-extraction"
PERSONA = PREFIX + "llm-jailbreak-payload"


def check(path, matched, absent, name=None):
    with tempfile.TemporaryDirectory(prefix="prompt-observation-") as folder:
        target = Path(folder) / (name or path.name)
        target.write_bytes(path.read_bytes())
        result = subprocess.run(
            [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT),
             "test-rules", str(target), "--rules", ",".join(matched + absent)],
            capture_output=True, text=True, check=True, timeout=180)
        actual = {line.split()[1] for line in result.stdout.splitlines()
                  if line.startswith("MATCHED ")}
        assert set(matched) <= actual, (path, result.stdout)
        assert not set(absent) & actual, (path, result.stdout)
        if PAIR in matched:
            assert "stays Suspicious" in result.stdout, result.stdout
        print("PASS", path.relative_to(ROOT))


if __name__ == "__main__":
    cases = [
        (HERE / "exported-prompts.js", [PAIR, EXTRACTION, PERSONA], []),
        (HERE / "submitted-prompts.js", [PAIR, EXTRACTION, PERSONA], []),
        (HERE / "persona-only.js", [PERSONA], [PAIR, EXTRACTION]),
    ]
    # Existing positive and exclusion controls, including files outside this
    # review batch. Copying isolates content from testdata path suppression.
    existing = ROOT / "testdata/taxonomy/llm-extraction-exception-selector/cases.json"
    for case in json.loads(existing.read_text())["fixtures"]:
        if case["path"].endswith("/security-review-query.md"):
            # Its legacy expectations predate the stricter documentary
            # exception: a permission claim alone does not establish inert
            # examples. Keep current query coverage, without changing rules.
            case["matched"] = [EXTRACTION,
                "objectives/evasion/security-bypass/llm/prompt/override::llm-system-prompt-query"]
            case["not_matched"] = [
                "metadata/package/documentation/agent-safety::security-example-documentation"]
        cases.append((ROOT / case["path"], case["matched"],
                      case["not_matched"], case.get("fixture_name")))
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        futures = [pool.submit(check, *case) for case in cases]
        for future in futures:
            future.result()
