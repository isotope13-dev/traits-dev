#!/usr/bin/env python3
"""Static scanner regressions for the October 2026 Go good-pool review."""

import argparse
import json
import shutil
import subprocess
import tempfile
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cleave", default="../cleave/target/release/cleave")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    cleave = str(Path(args.cleave).resolve())
    with tempfile.TemporaryDirectory(prefix="go-source-review-") as work:
        staged = Path(work) / "source"
        staged.mkdir()
        for level in ("baseline", "notable", "suspicious", "hostile"):
            for source in (root / "testdata" / level / "go-good-review").glob("*.go"):
                shutil.copyfile(source, staged / source.name)
        sliver_source = (staged / "sliver-wireguard.go").read_text()
        (staged / "sliver-wireguard.go").rename(staged / "operator-client.go")
        (staged / "ordinary-wireguard.go").write_text(
            sliver_source.replace("github.com/bishopfox/sliver/client/assets", "example.org/operator/assets")
            .replace("github.com/bishopfox/sliver/protobuf/rpcpb", "example.org/operator/rpcpb")
        )
        (staged / "documented-wireguard.go").write_text(
            "package notes\n" + "\n".join("// " + line for line in sliver_source.splitlines()) + "\n"
        )
        # Neutral paths prevent a tests/ directory exclusion from concealing a
        # regression. This input is parsed only; no Go code is compiled or run.
        (staged / "environment-upload.go").write_text('''package upload
import ("net/http"; "net/url"; "os"; "strings")
func send(endpoint string) {
    body := strings.Join(os.Environ(), "\\n")
    http.PostForm(endpoint, url.Values{"env": {body}})
}
''')
        proc = subprocess.run(
            [cleave, "--traits-dir", str(root), "--format", "jsonl", str(staged)],
            text=True, capture_output=True, check=True,
        )
        reports = [json.loads(line) for line in proc.stdout.split("\n") if line]
        files = {
            Path(f["path"]).name: f
            for report in reports for f in report["files"]
        }
        assert len(files) == 12, sorted(files)

        def ids(name):
            return {t["id"] for t in files[name].get("traits", [])}

        def require(name, *wanted):
            missing = set(wanted) - ids(name)
            assert not missing, (name, "missing", sorted(missing))

        def reject(name, *unwanted):
            found = set(unwanted) & ids(name)
            assert not found, (name, "unexpected", sorted(found))

        launch = "micro-behaviors/process/thread/create::go-goroutine-launch-call"
        debugger = "micro-behaviors/process/debug/detect::go-debugger-present-helper-call"
        hypervisor = "micro-behaviors/os/virtualization/hypervisor::go-cpuid-hypervisor-report-call"
        timing = "micro-behaviors/time/query::go-rdtsc-delta-helper-call"
        decrypt = "micro-behaviors/crypto/decrypt::go-lsa-decrypt-helper-call"
        read = "micro-behaviors/mem/read/arbitrary::go-readva-helper-call"
        allocated = "micro-behaviors/process/inject/remote-thread::go-allocated-memory-remote-thread-start"
        source_write = "micro-behaviors/mem/write/arbitrary::write-process-memory-source"
        require("calls.go", launch, debugger, hypervisor, timing)
        reject("documented-operations.go", launch, debugger, hypervisor, timing,
               decrypt, read, allocated, source_write,
               "micro-behaviors/data/buffer/transfer::go-byte-string-io-method-call",
               "micro-behaviors/data/buffer/transfer::go-stream-transfer-method-call")
        require("remote-thread.go", allocated, source_write)
        reject("unrelated-thread.go", allocated)
        require("tspkg.go", decrypt, read,
                "objectives/credential-access/memory::go-tspkg-credential-decryption")
        exfil = "objectives/exfiltration/stealer/configuration/environment::go-env-http-exfiltration"
        require("environment-upload.go", exfil)
        reject("unrelated-environment.go", exfil,
               "micro-behaviors/communications/http/request/body/environment::environment-http-body-flow")
        check_terms = ["metadata/package/documentation/security-testing::" + name for name in (
            "security-check-status-wording", "security-check-id-field")]
        check_terms.append("metadata/package/documentation/security-advisory::cwe-weakness-reference")
        require("security-report.go", *check_terms)
        reject("ordinary-log.go", *check_terms,
               "metadata/package/documentation/security-testing::security-check-report-vocabulary")
        sliver_identity = "well-known/tool/offensive/command-and-control/sliver::sliver-operator-wireguard-source"
        sliver_channel = "objectives/command-and-control/channel/transport::sliver-operator-wireguard-rpc-channel"
        require("operator-client.go", sliver_identity, sliver_channel)
        reject("ordinary-wireguard.go", sliver_identity, sliver_channel)
        reject("documented-wireguard.go", sliver_identity, sliver_channel)
        expected_high = {"remote-thread.go", "unrelated-thread.go", "tspkg.go", "environment-upload.go"}
        expected_high.add("operator-client.go")
        for name, report in files.items():
            high = [t for t in report.get("traits", []) if t["crit"] >= 4]
            if name not in expected_high:
                assert not high, (name, high)
            elif name == "operator-client.go":
                assert {t["id"] for t in high} == {sliver_identity, sliver_channel}, (name, high)
                assert all(t["crit"] == 5 for t in high), (name, high)
            elif name != "environment-upload.go":
                assert len(high) == 1 and high[0]["crit"] == 4, (name, high)
    print("Go triage regressions passed: 12 source controls; no sample code executed")


if __name__ == "__main__":
    main()
