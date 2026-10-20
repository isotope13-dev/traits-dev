"""Check observations outside testdata paths, which suppress some intent rules."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
EXPECTED = {
    "credential-zip.py": ["objectives/collection/archive/stage::data-staging"],
    "credential-tar.py": ["objectives/collection/archive/stage::data-staging"],
    "kubernetes-meta.py": [],
    "bot-panel.html": ["objectives/command-and-control/backdoor/teamserver::bot-specific-attack-control"],
    "bot-status.html": [],
    "user-panel.html": [],
    "installer.ps1": ["micro-behaviors/process/create/spawn::powershell-webclient-executable-url-start-context"],
    "vendor-installer.ps1": ["micro-behaviors/process/create/spawn::powershell-webclient-exe-staging-start-context"],
    "trigger.js": ["micro-behaviors/os/module/load::cjs-side-effect-local-require"],
    "dynamic.kt": ["micro-behaviors/process/interpreter/webview::source-variable-named-javascript-interface"],
    "epoch.py": ["micro-behaviors/time/query::python-time-epoch-comparison-context"],
    "duration.py": ["micro-behaviors/time/query::python-time-epoch-comparison-context"],
    "ranking.csv": ["metadata/file/format/wordlist::search-ranking-csv-header"],
    "s3.json": ["objectives/discovery/cloud/permissions::s3-public-access-block-disabled"],
    "letter.txt": ["objectives/lateral-movement/social-engineering/lures::advance-fee-fraud-letter"],
    "diagnostics.ts": ["micro-behaviors/os/telemetry/activity::shell-guard-recent-read",
                       "micro-behaviors/os/telemetry/activity::shell-guard-command-rpc-output"],
    "detached.py": ["objectives/evasion/process/hidden/execution::nohup-hidden-curl-staged-script-exec"],
    "telemetry-installer.js": ["micro-behaviors/os/telemetry/logging/llm::global-agent-content-telemetry-write"],
    "static.kt": [],
    "domains.json": [],
    "component-toggle.kt": [],
    "hidden.vbs": [],
}
ZERO_HIGH = {
    "kubernetes-meta.py",
    "bot-status.html", "user-panel.html",
    "trigger.js", "dynamic.kt", "static.kt", "epoch.py", "duration.py",
    "ranking.csv", "domains.json", "diagnostics.ts", "component-toggle.kt",
    "hidden.vbs",
}
RETIRED = {
    "objectives/command-and-control/dropper/file-exec/spawn::powershell-webclient-remote-exe-launch",
    "objectives/command-and-control/dropper/file-exec/spawn::powershell-download-exe-execute",
    "objectives/command-and-control/backdoor/rat/tasking::toll-bridge-dynamic-name",
    "objectives/supply-chain/hidden-payload/trojan::npm-trigger-module-import",
    "objectives/supply-chain/hidden-payload/trojan::npm-trigger-module-api-facade",
    "objectives/exfiltration/llm::global-identity-attributed-conversation-export",
    "objectives/command-and-control/dropper/file-exec/spawn::vbs-hidden-first-arg-wsh-proxy",
    "objectives/anti-analysis/timing/timer::py-time-epoch-compare",
}


def main():
    with tempfile.TemporaryDirectory(prefix="hopper-rule-controls-") as scratch:
        for name in EXPECTED:
            shutil.copyfile(HERE / name, Path(scratch) / name)
        result = subprocess.run(
            ["atomscan", "--no-update", "--mode", "slow", "--follow=none",
             "--format=json", "path", scratch],
            env=dict(os.environ, CLEAVE_TRAITS_DIR=str(ROOT)),
            capture_output=True, text=True,
        )
        # Atomscan uses exit 1 for a hostile positive control and 2 for suspicious.
        assert result.returncode in (0, 1, 2), result.stderr
        assert "could not parse" not in result.stderr, result.stderr
        reports = {}
        for line in result.stdout.splitlines():
            envelope = json.loads(line)
            for report in envelope["raw"]["files"]:
                reports[Path(report["path"]).name] = report
        assert reports.keys() == EXPECTED.keys(), reports.keys()
        for name, required in EXPECTED.items():
            traits = reports[name].get("traits", [])
            ids = {t["id"] for t in traits}
            assert set(required) <= ids, (name, set(required) - ids)
            assert not RETIRED & ids, (name, RETIRED & ids)
            if name != "detached.py":
                assert not any(t["crit"] >= 5 for t in traits), (name, traits)
            if name in ZERO_HIGH:
                assert not any(t["crit"] >= 4 for t in traits), (name, traits)
            if name == "static.kt":
                assert EXPECTED["dynamic.kt"][0] not in ids
            print("PASS", name)
        print(f"{len(EXPECTED)} cases passed")


if __name__ == "__main__":
    main()
