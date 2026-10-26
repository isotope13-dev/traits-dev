#!/usr/bin/env python3
"""Check collection evidence, portable spellings, and protocol near misses."""
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]
CLEAVE = os.environ.get("CLEAVE", "/usr/local/var/cyclotron/cleave/target/release/cleave")
CONTROLS = Path(os.environ.get(
    "AI_TRAIN_CONTROLS", str(ROOT / "testdata/triage/fallout-20261026")))
CATALOG = "objectives/credential-access/dev-tools/ai::multi-ai-agent-"
PROTOCOL = "well-known/malware/stealer/aokigahara::chunked-upload-protocol"
MARKER = "micro-behaviors/communications/http/token-auth::x-gate-token-header-reference"
AUTH = "micro-behaviors/fs/path/credential::"
CONFIG = "micro-behaviors/fs/path/config/app::"
GEMINI = "micro-behaviors/fs/path/password-store::gemini-workspace-auth-artifact-path"
CURSOR = "micro-behaviors/fs/path/app-data::cursor-global-storage-artifact-path"
COLLECTION = {
    CATALOG + "auth-artifact-catalog",
    CATALOG + "config-artifact-catalog",
    CATALOG + "credential-collection-catalog",
}


def analyze(path):
    result = subprocess.run(
        [CLEAVE, "--traits-dir", str(ROOT), "--format", "json", str(path)],
        check=True, capture_output=True, text=True)
    files = json.loads(result.stdout)["files"]
    assert len(files) == 1, path
    return {t["id"]: t for t in files[0]["traits"]}


for name in ("windows-catalog.cs", "posix-paths.js"):
    traits = analyze(ROOT / "testdata/ai-train" / name)
    assert COLLECTION <= traits.keys(), (name, COLLECTION - traits.keys())
    assert all(traits[key]["crit"] == 4 for key in COLLECTION), name
    assert not any(t["crit"] == 5 for t in traits.values()), name
    assert {GEMINI, CURSOR, AUTH + "claude-auth-artifact-path",
            AUTH + "codex-auth-artifact-path", CONFIG + "codeium-config-artifact-path",
            CONFIG + "claude-root-config-artifact-path"} <= traits.keys(), name
    assert (PROTOCOL in traits) == (name == "windows-catalog.cs"), name
    print("PASS", name)

for name in ("single-vendor.py", "ordinary-upload.js", "marker-only.py",
             "path-near-misses.js"):
    traits = analyze(CONTROLS / name)
    high = {key for key, value in traits.items() if value["crit"] >= 4}
    assert not high, (name, high)
    if name == "single-vendor.py":
        assert AUTH + "codex-auth-artifact-path" in traits
    if name == "marker-only.py":
        assert MARKER in traits
    if name == "ordinary-upload.js":
        assert all("micro-behaviors/communications/http/url/api-path::upload-" +
                   route + "-route" in traits
                   for route in ("handshake", "chunk", "complete"))
    if name == "path-near-misses.js":
        assert not any(key in traits for key in (
            AUTH + "claude-auth-artifact-path", AUTH + "codex-auth-artifact-path",
            AUTH + "copilot-hosts-auth-artifact-path", AUTH + "kiro-sso-auth-artifact-path",
            CONFIG + "codeium-config-artifact-path", GEMINI, CURSOR))
    print("PASS", name)
