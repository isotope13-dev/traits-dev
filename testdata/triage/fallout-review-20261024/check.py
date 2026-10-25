"""Static regression controls. Never execute sample JavaScript."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
CHILD = "micro-behaviors/process/create/eval::awaited-source-node-inline-child"
PAYLOAD = "objectives/execution/payload/script-eval::ethereum-blockchain-derived-node-stage"
C2 = "objectives/command-and-control/channel/deaddrop/blockchain::ethereum-recipient-payload-header-rendezvous"
HIDDEN = "objectives/evasion/process/hidden/window::ethereum-stage-hidden-detached-child"
SHARED = "objectives/execution/payload/script-eval::node-http-xor-eval-detached-stage"
ALL = {CHILD, PAYLOAD, C2, HIDDEN}

def main():
    source_dir = ROOT / "testdata/stranded-members/agentgui-metasploit-review"
    source = (source_dir / "different-eval-source.js").read_text()
    cases = {
        "child-only.js": (source, ALL, {SHARED}),
        "comma-sequence-child.js": (source.replace("e||eval(r+unrelated);spawn", "e||eval(r+unrelated),spawn"), ALL, {SHARED}),
        "original.js": ((source_dir / "database.js").read_text(), ALL | {SHARED}, set()),
        "different-child.js": ((source_dir / "different-child-source.js").read_text(), {C2}, {CHILD, PAYLOAD, HIDDEN, SHARED}),
        "clean-database.js": (source[:source.index("global.i=")], set(), ALL),
        "other-wallet.js": (source.replace(r"\u0061\u0033\u0032\u0032", r"\u0062\u0034\u0033\u0033"), ALL, {SHARED}),
        "other-paths.js": (source.replace("/0x/cls", "/stage/one").replace("/0x/ls", "/stage/two"), ALL, {SHARED}),
        "visible-child.js": (source.replace("windowsHide:!0", "windowsHide:!1"), {CHILD, PAYLOAD, C2}, {HIDDEN}),
        "no-xor.js": (source.replace("]^=", "]+="), {CHILD}, {PAYLOAD, C2, HIDDEN}),
        "wrong-runtime.js": (source.replace('spawn("node",', 'spawn("echo",'), {C2}, {CHILD, PAYLOAD, HIDDEN}),
        "wrong-first-argument.js": (source.replace('spawn("node",', 'spawn("echo","node",'), {C2}, {CHILD, PAYLOAD, HIDDEN}),
        "wrong-code-position.js": (source.replace('["-e",r+o]', '["ignored","-e",r+o]'), {C2}, {CHILD, PAYLOAD, HIDDEN}),
        "benign-async-wrapper.js": ('async function wrap() { const body = await makeLocalScript(); spawn("node", ["-e", prefix+body], {detached:true, windowsHide:true, stdio:"ignore"}).unref(); }', {CHILD}, {PAYLOAD, C2, HIDDEN}),
    }
    moved = "micro-behaviors/process/create/eval::"
    direct, first, computed = [moved + name for name in ["spawn-node-eval", "spawn-node-eval-first-option", "spawn-node-eval-computed-access"]]
    cases.update({
        "inline-first.js": ('spawn("node", ["-e", code]);', {direct, first}, {computed}),
        "inline-later.js": ('spawn("node", ["--no-warnings", "-e", code]);', {direct}, {first, computed}),
        "inline-computed.js": ('cp["spawn"]("node", ["-e", code]);', {computed}, {direct, first}),
        "other-interpreter.js": ('spawn("python", ["-e", code]);', set(), {direct, first, computed}),
    })
    tag = "metadata/lang/source/syntax/assignment::global-i-a-digit-tag"
    retired_tag = "well-known/malware/supply-chain/contagious-interview::etherhiding-global-i-marker"
    cases.update({
        "global-tag-only.js": ('global.i="A7-local";', {tag}, ALL | {retired_tag}),
        "other-global-tag.js": ('global.i="B7-local";', set(), ALL | {tag, retired_tag}),
    })
    env = os.environ.copy()
    env.pop("CLEAVE_VALIDATE", None)
    with tempfile.TemporaryDirectory(prefix=".fallout-review-", dir=ROOT) as tmp:
        paths = []
        for name, (content, _, _) in cases.items():
            path = Path(tmp) / name
            path.write_text(content)
            paths.append(str(path))
        proc = subprocess.run([env.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT), "--format", "jsonl", *paths], capture_output=True, text=True, env=env, check=True)
        files = {Path(f["path"]).name: f for line in proc.stdout.splitlines() for f in json.loads(line).get("files", [])}
        for name, (_, required, forbidden) in cases.items():
            traits = {t["id"] for t in files[name].get("traits", [])}
            assert required <= traits, (name, "missing", required-traits)
            assert not forbidden & traits, (name, "unexpected", forbidden & traits)
            if name in {"clean-database.js", "benign-async-wrapper.js"}:
                assert not any(t["crit"] >= 4 for t in files[name].get("traits", [])), name
            print("PASS", name)

if __name__ == "__main__":
    main()
