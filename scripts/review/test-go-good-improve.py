#!/usr/bin/env python3
"""Check Go triage coverage against aliases, inert examples, and missing roles."""

import argparse
import json
import re
import subprocess
import tempfile
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cleave", default="../cleave/target/release/cleave")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    cleave = str(Path(args.cleave).resolve())

    def fixture(level, name):
        return (root / "testdata" / level / "go-good-improve" / name).read_text()

    def documented(source):
        return "package notes\n" + "\n".join("// " + line for line in source.splitlines()) + "\n"

    sliver = (root / "testdata/hostile/go-good-review/sliver-wireguard.go").read_text()
    renamed = sliver
    for original, alias in (
        ("google.golang.org/grpc", "rpc"),
        ("golang.zx2c4.com/wireguard/device", "wg"),
        ("github.com/bishopfox/sliver/protobuf/rpcpb", "pb"),
        ("github.com/bishopfox/sliver/client/assets", "cfg"),
    ):
        old = original.rsplit("/", 1)[-1]
        renamed = renamed.replace(f'"{original}"', f'{alias} "{original}"')
        renamed = renamed.replace(old + ".", alias + ".")
    for original, replacement in (
        ("wireGuardMTLSConnect", "connect"),
        ("validateWireGuardConfig", "validate"),
        ("dialRPCClient", "openRPC"),
    ):
        renamed = renamed.replace(original, replacement)
    ordinary = sliver.replace("github.com/bishopfox/sliver/client/assets", "example.org/operator/assets")
    ordinary = ordinary.replace("github.com/bishopfox/sliver/protobuf/rpcpb", "example.org/operator/rpcpb")

    startup = fixture("suspicious", "startup-gates.go")
    startup_alias = startup.replace('"github.com/MrTuxx/OffensiveGolang/pkg/evasion"',
                                    'guard "github.com/MrTuxx/OffensiveGolang/pkg/evasion"')
    startup_alias = startup_alias.replace("evasion.", "guard.")
    shadow = startup_alias.replace("func main() {", "func main() {\n guard := localChecker{}")
    shadow += """
var keepImportedHelper = guard.CheckNameEXE
type localChecker struct{}
func (localChecker) CheckNameEXE(string) {}
func (localChecker) CheckMouse(int) {}
func (localChecker) CheckScreen() {}
"""

    bot = fixture("suspicious", "keyed-hub.go")
    moved_bot = bot.replace("cs8425.noip.me:8787", "different.example.invalid:9443")
    moved_bot = moved_bot.replace('"local/base"', 'core "local/base"')
    moved_bot = moved_bot.replace("base.", "core.").replace("NewClientM()", "NewClient()")
    moved_bot = re.sub(r"\bc\b", "node", moved_bot)
    header = fixture("notable", "elf-header.go")
    domain = fixture("suspicious", "tor-domain.go")
    precomputed = fixture("suspicious", "tor-precomputed.go")
    cases = {
        "sliver.go": sliver,
        "renamed.go": renamed,
        "ordinary-wireguard.go": ordinary,
        "documented-sliver.go": documented(sliver),
        "startup.go": startup,
        "startup-alias.go": startup_alias,
        "startup-shadow.go": shadow,
        "documented-startup.go": documented(startup),
        "keyed-hub.go": bot,
        "other-hub.go": moved_bot,
        "hub-without-key.go": bot.replace("\tc.HubPubKey = hubPubKey\n", ""),
        "hub-without-browser.go": re.sub(r'userAgent = "[^"]+"', 'userAgent = "Custom/1.0"', bot),
        "unrelated-start.go": bot.replace("c.Start(hubAddr)", "other.Start(hubAddr)"),
        "documented-hub.go": documented(bot),
        "elf-header.go": header,
        "elf-comments.go": header.replace("out", "image").replace(
            "image[2]", "// preserve layout\n    image[2]"),
        "elf-split-buffers.go": header.replace("out[2]", "other[2]"),
        "documented-elf.go": documented(header),
        "elf-copy.go": fixture("notable", "elf-copy.go"),
        "tor-domain.go": domain,
        "documented-domain.go": documented(domain),
        "tor-secret.go": domain.replace('[]byte("Derive temporary signing key hash input")',
                                       'append([]byte("Derive temporary signing key hash input"), secret...)'),
        "tor-precomputed.go": precomputed,
        "tor-precomputed-alias.go": precomputed.replace('"encoding/hex"', 'h "encoding/hex"')
                                              .replace("hex.DecodeString", "h.DecodeString"),
        "tor-other-decoder.go": precomputed.replace('"encoding/hex"', 'hex "example.org/decoder"'),
        "documented-precomputed.go": documented(precomputed),
    }
    with tempfile.TemporaryDirectory(prefix="go-trait-improve-") as work:
        stage = Path(work) / "source"
        stage.mkdir()
        for name, source in cases.items():
            (stage / name).write_text(source)
        result = subprocess.run(
            [cleave, "--traits-dir", str(root), "--format", "jsonl", str(stage)],
            text=True, capture_output=True, check=True,
        )
        assert "skipped" not in result.stderr.lower(), result.stderr
        reports = [json.loads(line) for line in result.stdout.split("\n") if line]
        files = {Path(f["path"]).name: f for r in reports for f in r["files"]}
        assert files.keys() == cases.keys(), (files.keys(), cases.keys())

        def ids(name):
            return {t["id"] for t in files[name].get("traits", [])}

        def require(name, *wanted):
            assert not (set(wanted) - ids(name)), (name, "missing", set(wanted) - ids(name))

        def reject(name, *unwanted):
            assert not (set(unwanted) & ids(name)), (name, "unexpected", set(unwanted) & ids(name))

        identity = "well-known/tool/offensive/command-and-control/sliver::sliver-operator-wireguard-source"
        channel = "objectives/command-and-control/channel/transport::sliver-operator-wireguard-rpc-channel"
        signature = "well-known/tool/offensive/command-and-control/sliver::operator-rpc-client-return-type"
        for name in ("sliver.go", "renamed.go"):
            require(name, identity, channel, signature)
            high = [t for t in files[name].get("traits", []) if t["crit"] >= 4]
            assert {t["id"] for t in high} == {identity, channel} and all(t["crit"] == 5 for t in high), (name, high)
        for name in ("ordinary-wireguard.go", "documented-sliver.go"):
            reject(name, identity, channel, signature)
        gates = (
            "objectives/anti-analysis/environment-detect/check::go-offensivegolang-executable-name-gate",
            "objectives/anti-analysis/environment-detect/check::go-offensivegolang-display-startup-gate",
            "objectives/anti-analysis/sandbox-detect/input::go-offensivegolang-mouse-startup-gate",
        )
        for name in ("startup.go", "startup-alias.go"):
            require(name, *gates)
        for name in ("startup-shadow.go", "documented-startup.go"):
            reject(name, *gates)
        hub = "objectives/command-and-control/channel/covert::go-keyed-hub-browser-transport"
        endpoint = "micro-behaviors/communications/socket/endpoint::go-client-start-fixed-endpoint"
        for name in ("keyed-hub.go", "other-hub.go"):
            require(name, hub, endpoint)
        for name in ("hub-without-key.go", "hub-without-browser.go", "unrelated-start.go", "documented-hub.go"):
            reject(name, hub)
        reject("unrelated-start.go", endpoint)
        marker = "micro-behaviors/data/serialize/binary::go-elf-header-marker-writes"
        require("elf-header.go", marker)
        require("elf-comments.go", marker)
        reject("elf-split-buffers.go", marker)
        reject("documented-elf.go", marker)
        require("elf-copy.go", "micro-behaviors/data/serialize/binary::go-copy-elf-signature")
        public = "micro-behaviors/crypto/kdf/public-prefix::tor-empty-prefix-go"
        decoded = "micro-behaviors/crypto/kdf/public-prefix::tor-precomputed-public-prefix-go"
        require("tor-domain.go", public)
        reject("documented-domain.go", public)
        reject("tor-secret.go", public)
        for name in ("tor-precomputed.go", "tor-precomputed-alias.go"):
            require(name, decoded)
        for name in ("tor-other-decoder.go", "documented-precomputed.go"):
            reject(name, decoded)
        allowed_high = {
            "sliver.go", "renamed.go", "startup.go", "startup-alias.go",
            "keyed-hub.go", "other-hub.go", "tor-domain.go",
            "tor-precomputed.go", "tor-precomputed-alias.go",
        }
        for name, report in files.items():
            high = [t for t in report.get("traits", []) if t["crit"] >= 4]
            if name not in allowed_high:
                assert not high, (name, high)
    print(f"Go improvement regressions passed: {len(cases)} controls; no sample code executed")


if __name__ == "__main__":
    main()
