"""Scan controls without importing or executing their code."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
INITIALIZE = "micro-behaviors/communications/http/client/initialize::"
GET = "micro-behaviors/communications/http/get::"
TLS = "micro-behaviors/communications/tls/"
CONNECT = "micro-behaviors/communications/socket/connect::"
CHECKSUM = "micro-behaviors/data/checksum::go-xxhash-sum64-string"
COOKIE = "micro-behaviors/communications/http/cookies::cookie-helper-set-call"
SUBMIT = "micro-behaviors/process/work/pool::parallel-submit-call"
REPLAY = "objectives/credential-access/browser/session-hijack::python-bearer-session-replay"


def main():
    scratch = Path(sys.argv[1])
    scratch.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=scratch, prefix="consumer-") as temporary:
        # Several existing consumer rules exclude test directories. Exercise
        # those same fixture bytes under a normal source path as well.
        replay = Path(temporary) / "replay.py"
        replay.write_bytes((HERE / "replay.py").read_bytes())
        async_replay = Path(temporary) / "async-replay.py"
        async_replay.write_text(replay.read_text().replace("httpx.Client()", "httpx.AsyncClient()"))
        paths = [HERE / name for name in
                 ["positive.py", "near-miss.py", "capabilities_test.go", "near-miss.go"]]
        paths += [replay, async_replay]
        result = subprocess.run(
            [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT),
             "--format", "jsonl", *map(str, paths)],
            env=dict(os.environ, CLEAVE_VALIDATE="0"),
            capture_output=True, text=True, check=True,
        )
        assert not result.stderr.strip(), result.stderr
        files = [file for line in result.stdout.splitlines()
                 for file in json.loads(line)["files"]]
        findings = {Path(file["path"]).name: {t["id"]: t["crit"]
                    for t in file.get("traits", [])} for file in files}
        positive = {
            INITIALIZE + "python-primp-client", INITIALIZE + "httpx-client",
            INITIALIZE + "httpx-async-client", GET + "python-primp-client-get",
            GET + "python-request-get-keyword", COOKIE, SUBMIT,
            TLS + "initialize::python-ssl-context-set-ciphers",
            TLS + "verify/disable::python-client-conditional-verify-false",
        }
        assert positive <= findings["positive.py"].keys(), positive - findings["positive.py"].keys()
        forbidden = positive - {INITIALIZE + "httpx-client"}
        assert not forbidden & findings["near-miss.py"].keys()
        go = {CONNECT + "dial", CONNECT + "dial-timeout-tcp", CHECKSUM}
        assert go <= findings["capabilities_test.go"].keys()
        assert not go & findings["near-miss.go"].keys()
        for name in ["replay.py", "async-replay.py"]:
            assert findings[name].get(REPLAY) == 5, (name, findings[name])
        print("Six controls passed, including both hostile httpx consumers.")


if __name__ == "__main__":
    main()
