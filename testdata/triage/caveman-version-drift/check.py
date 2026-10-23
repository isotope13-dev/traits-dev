"""Run focused controls from neutral paths, outside test-directory suppressors."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
HERE = ROOT / "testdata" / "benign" / "triage" / "caveman-version-drift"
STREAM = "micro-behaviors/process/deploy/file-exec::node-stream-file-finish-launch"
TEMP = "micro-behaviors/process/deploy/file-exec::node-streamed-temp-file-launch"
DNS = "micro-behaviors/process/deploy/file-exec::node-dns-streamed-temp-file-launch"
HOOK = "micro-behaviors/communications/ipc/agent-hook::sessionstart-fetch-command-config"
CLONE = "objectives/supply-chain/impersonation/clone-and-rename::rebranded-litellm-redistribution"
FIELD = "metadata/lang/source/naming/setting::litellm-call-id-key"


def reports(text):
    decoder = json.JSONDecoder()
    while text.strip():
        value, end = decoder.raw_decode(text.lstrip())
        yield value
        text = text.lstrip()[end:]


def scan(path):
    result = subprocess.run(
        [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT),
         "--format", "json", str(path)],
        capture_output=True, text=True, check=True,
    )
    return {
        Path(file["path"]).name: {t["id"] for t in file.get("traits", [])}
        for report in reports(result.stdout)
        for file in report.get("files", [])
    }


def main():
    cases = {
        "stream-launch.js": ({STREAM, TEMP}, {DNS}),
        "stream-dns-launch.js": ({STREAM, TEMP, DNS}, {"objectives/command-and-control/dropper/file-exec/command/script-host-embedded::compact-js-fetch-chmod-exec"}),
        "stream-other-launch.js": (set(), {STREAM, TEMP, DNS}),
        "stream-other-writer.js": (set(), {STREAM, TEMP, DNS}),
        "stream-shadowed-target.js": (set(), {STREAM, TEMP, DNS}),
        "session-command.sh": ({HOOK}, set()),
        "session-local-install.sh": (set(), {HOOK}),
        "adapter.py": ({FIELD}, {CLONE, "well-known/lib/ai/litellm::litellm-codebase"}),
    }
    with tempfile.TemporaryDirectory(prefix="caveman-controls-") as dest:
        for name in cases:
            shutil.copyfile(HERE / name, Path(dest) / name)
        found = scan(dest)
        for name, (required, forbidden) in cases.items():
            observed = found[name]
            assert required <= observed, (name, "missing", required - observed)
            assert not forbidden & observed, (name, "unexpected", forbidden & observed)
            print("PASS", name)


if __name__ == "__main__":
    main()
