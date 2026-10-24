"""Scan controls only; never execute the JavaScript or batch fixtures."""
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
PAYLOAD = "objectives/execution/payload/script-eval::obfuscated-etherhiding-hex-stage-dropper"
RENDEZVOUS = "objectives/command-and-control/channel/deaddrop/blockchain::obfuscated-ethereum-recipient-stage-rendezvous"
PATCH = "objectives/supply-chain/trojanized/app/patch::http-handler-whitespace-hidden-blockchain-stage"
EVAL = "micro-behaviors/process/interpreter/eval/indirect::js-computed-helper-receives-eval"
SPAWN = "micro-behaviors/process/create/eval::js-helper-receives-spawn-inline-source"


def main():
    source = (HERE / "analytics-stage.js").read_text()
    cases = {
        "original.js": (source, {PAYLOAD, RENDEZVOUS, PATCH}, set()),
        "clean-handler.js": (source[:source.index("global.i=")], set(), {PAYLOAD, RENDEZVOUS, PATCH}),
        "no-eval.js": (source.replace("](eval,", "](ignoreSource,"), set(), {PAYLOAD, RENDEZVOUS, PATCH}),
        "no-spawn.js": (source.replace("](spawn,", "](ignoreChild,"), set(), {PAYLOAD, RENDEZVOUS, PATCH}),
        "no-xor.js": (source.replace("]^=", "]+="), set(), {PAYLOAD, RENDEZVOUS, PATCH}),
        "no-recipient.js": (source.replace("['tx']['to']", "['tx']['value']"), {PAYLOAD}, {RENDEZVOUS, PATCH}),
        "visible-stage.js": (re.sub(r"[ \t]{100,}", " ", source), {PAYLOAD, RENDEZVOUS}, {PATCH}),
        "helper-positive.js": ('x[f](eval, source()); x[g](spawn, target, ["-e", code], {});', {EVAL, SPAWN}, {PAYLOAD}),
        "helper-negative.js": ('x[f](log, source()); x[g](observe, target, ["-e", code], {});', set(), {EVAL, SPAWN, PAYLOAD}),
        "git-query-only.bat": ('@echo off\ngit log -1 --date=format-local:%%Y\ngit log -1 --format=%%an\ngit rev-parse --abbrev-ref HEAD\n',
                               {"micro-behaviors/revision-control/git::git-log-last-commit-local-date-query",
                                "micro-behaviors/revision-control/git::git-log-last-commit-field-query"},
                               {"objectives/evasion/indicator-removal/history::timestamped-amend-rewrite"}),
    }
    with tempfile.TemporaryDirectory(prefix=".registry-review-", dir=REPO) as tmp:
        paths = []
        for name, (content, _, _) in cases.items():
            path = Path(tmp) / name
            path.write_text(content)
            paths.append(str(path))
        env = os.environ.copy()
        env.pop("CLEAVE_VALIDATE", None)
        result = subprocess.run(
            [env.get("CLEAVE", "cleave"), "--traits-dir", str(REPO), "--format", "jsonl", *paths],
            capture_output=True, text=True, env=env, check=True,
        )
        reports = [json.loads(line) for line in result.stdout.splitlines() if line.strip()]
        files = {Path(f["path"]).name: f for report in reports for f in report["files"]}
        for name, (_, required, forbidden) in cases.items():
            traits = {t["id"] for t in files[name].get("traits", [])}
            assert required <= traits, (name, "missing", required - traits)
            assert not forbidden & traits, (name, "unexpected", forbidden & traits)
        for name in ["clean-handler.js", "helper-positive.js", "helper-negative.js", "git-query-only.bat"]:
            assert not any(t["crit"] >= 4 for t in files[name].get("traits", [])), name
    print(f"PASS {len(cases)} original-source and missing-role controls")


if __name__ == "__main__":
    main()
