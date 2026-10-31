#!/usr/bin/env python3
"""Check renamed JVM positives and controls without executing fixture code."""
import argparse
import importlib.util
import json
import os
import subprocess
import tempfile
from pathlib import Path


def reports(stream):
    decoder = json.JSONDecoder()
    while stream.strip():
        stream = stream.lstrip()
        report, length = decoder.raw_decode(stream)
        if report.get("files"):
            yield report["files"][0]
        stream = stream[length:]


def main():
    root = Path(__file__).resolve().parents[2]
    parser = argparse.ArgumentParser()
    parser.add_argument("--cleave", default=os.environ.get("CLEAVE", str(root.parent / "cleave/target/release/cleave")))
    args = parser.parse_args()
    spec = importlib.util.spec_from_file_location("jvm_builder", root / "scripts/fixture-builders/java-class-triage.py")
    builder = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(builder)
    expected = {}
    with tempfile.TemporaryDirectory(prefix="jvm-controls-") as work:
        for severity, name, data in builder.fixtures() + builder.webhook_fixtures():
            path = Path(work) / (name + ".class")
            path.write_bytes(data)
            expected[path.name] = severity
        for severity, name, data in (builder.jphp_fixtures() + builder.archive_fixtures()
                                     + builder.endpoint_fixtures() + builder.keylogger_fixtures()
                                     + builder.secret_model_fixtures()):
            path = Path(work) / (name + ".jar")
            path.write_bytes(data)
            expected[path.name] = severity
        result = subprocess.run([args.cleave, "--traits-dir", str(root), "--format=jsonl", work],
                                capture_output=True, text=True)
        if result.returncode:
            raise RuntimeError(result.stderr)
        found = {Path(f["path"]).name: f for f in reports(result.stdout)}
    assert found.keys() == expected.keys(), (found.keys(), expected.keys())
    for name, severity in expected.items():
        traits = found[name].get("traits", [])
        highest = max((t["crit"] for t in traits), default=0)
        bounds = {"hostile": (5, 5), "suspicious": (4, 4), "notable": (3, 3), "baseline": (0, 2)}
        low, high = bounds[severity]
        assert low <= highest <= high, (name, severity, highest, traits)
        assert all(t["id"] not in {
            "objectives/credential-access/theft/authentication/keywords::irc-class-reference",
            "objectives/credential-access/theft/authentication/keywords::sendmessage-method-name",
        } for t in traits), name
    for name in ["bot-catalog.class", "replacement-bot.class"]:
        assert sum(t["crit"] == 5 for t in found[name]["traits"]) >= 3, name
    literal_ids = {t["id"] for t in found["string-only-irc-reference.class"].get("traits", [])}
    assert "metadata/import/jvm::sendmessage-member-reference" not in literal_ids
    assert "metadata/import/jvm::irc-class-reference" not in literal_ids
    theft = "objectives/credential-access/browser/multi-target::jvm-declared-cookie-password-theft"
    for name in ["quoted-theft-methods.class", "imported-theft-methods.class"]:
        assert theft not in {t["id"] for t in found[name].get("traits", [])}, name
    bundle_ids = {t["id"] for t in found["padded-native-theft-bundle.jar"].get("traits", [])}
    assert theft in bundle_ids
    assert "objectives/credential-access/discord/token::jvm-credential-theft-discord-recovery-bundle" in bundle_ids
    assert "objectives/collection/messaging/telegram::jvm-credential-theft-telegram-collection-bundle" in bundle_ids
    assert all(t["id"] != "objectives/anti-static/obfuscation/pack::allatori-demo-marker"
               for f in found.values() for t in f.get("traits", []))
    for name, expected_id in {
        "global-keylogger-buffer.class": "jvm-global-hook-keylog-buffer",
        "nested-keylogger-reporting.jar": "jvm-global-keylog-discord-reporting",
        "native-keylog-socket-control.jar": "jvm-native-keylog-socket-reporting",
        "reflected-live-keylogger.class": "jvm-reflected-live-keylog-packets",
    }.items():
        assert any(t["id"] == "objectives/collection/keylog/hook::" + expected_id
                   and t["crit"] == 5 for t in found[name].get("traits", [])), name
    for name, expected_id in {
        "protected-secret-collection-model.jar": "well-known/malware/stealer/myth::jvm-myth-secret-collection-model",
        "reviewed-attachment-diversion.class": "objectives/exfiltration/http/discord::jvm-diverted-webhook-file-uploads",
    }.items():
        assert any(t["id"] == expected_id and t["crit"] == 5
                   for t in found[name].get("traits", [])), name
    print(f"PASS: {len(found)} JVM controls, including renamed positives and literal-only negatives")


if __name__ == "__main__":
    main()
