#!/usr/bin/env python3
"""Check keyed-archive format evidence and retain independent attack findings."""

import argparse
import json
from pathlib import Path
import plistlib
import subprocess
import tempfile


PREFIX = "metadata/file/format/serialization::"
ARCHIVER = PREFIX + "ns-keyed-archiver"
IB = PREFIX + "interface-builder-object-data-class"
MASQUERADE = "objectives/evasion/masquerade/identity/bundle::generic-utils-bundle-id"
CMS = PREFIX + "cms-wrapped-plist"
ALL_DEVICES = "metadata/package/publishing::profile-all-device-distribution"
SYSTEM_EXTENSION = "metadata/signature/entitlements::profile-system-extension-install"
ASSOCIATED_DOMAINS = "metadata/signature/entitlements::profile-associated-domains-wildcard"
KEYCHAIN = "metadata/signature/entitlements::profile-keychain-access-group"
REVIEWED = {ARCHIVER, IB, MASQUERADE, CMS, ALL_DEVICES, SYSTEM_EXTENSION, ASSOCIATED_DOMAINS, KEYCHAIN}


def cms_wrap(content):
    """Minimal CMS SignedData framing with no signer (no trust is implied)."""
    def tlv(tag, body):
        length = len(body)
        if length < 128:
            size = bytes([length])
        else:
            encoded = length.to_bytes((length.bit_length() + 7) // 8, "big")
            size = bytes([0x80 | len(encoded)]) + encoded
        return bytes([tag]) + size + body

    data_oid = bytes.fromhex("06092a864886f70d010701")
    signed_oid = bytes.fromhex("06092a864886f70d010702")
    encapsulated = tlv(0x30, data_oid + tlv(0xa0, tlv(4, content)))
    signed_data = tlv(0x30, bytes.fromhex("0201013100") + encapsulated + bytes.fromhex("3100"))
    return tlv(0x30, signed_oid + tlv(0xa0, signed_data))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cleave", default="../cleave/target/release/cleave")
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[2]
    cleave = str((repo / args.cleave).resolve())
    archive = {
        "$archiver": "NSKeyedArchiver", "$version": 100000,
        "$top": {"root": plistlib.UID(1)},
        "$objects": ["$null", {"$classname": "NSIBObjectData"}],
    }
    cases = {
        "renamed.bin": (archive, {ARCHIVER, IB}),
        "ordinary.plist": ({"$archiver": "OtherArchiver", "$objects": []}, set()),
        "non-ui.plist": ({**archive, "$objects": ["$null"]}, {ARCHIVER}),
        "quoted.plist": ({"description": "NSKeyedArchiver NSIBObjectData"}, set()),
        "wrong-field.plist": ({"$archiver": "NSKeyedArchiverSuffix",
                               "$objects": [{"description": "NSIBObjectData"}]}, set()),
        # Format evidence must never serve as a blanket benign exclusion.
        "mixed.plist": ({**archive, "CFBundleIdentifier": "com.utils.wormgpt"},
                        {ARCHIVER, IB, MASQUERADE}),
        "provisioning.plist": ({
            "ProvisionsAllDevices": True,
            "Entitlements": {
                "com.apple.developer.system-extension.install": True,
                "com.apple.developer.associated-domains": "*",
                "keychain-access-groups": ["EXAMPLETEAM.org.example.app"],
            },
        }, {ALL_DEVICES, SYSTEM_EXTENSION, ASSOCIATED_DOMAINS, KEYCHAIN}),
        "restricted-profile.plist": ({
            "ProvisionsAllDevices": False,
            "Entitlements": {
                "com.apple.developer.system-extension.install": False,
                "com.apple.developer.associated-domains": "applinks:example.test",
                "keychain-access-groups": [],
            },
        }, set()),
        "profile-prose.plist": ({"description":
            'ProvisionsAllDevices true Entitlements com.apple.developer.system-extension.install '
            'com.apple.developer.associated-domains * keychain-access-groups'}, set()),
        "forged-envelope.plist": ({"plist": {"cms_wrapped": True}}, set()),
    }
    with tempfile.TemporaryDirectory(prefix="plist-triage-") as tmp:
        paths = []
        expected = {}
        for name, (value, required) in cases.items():
            path = Path(tmp) / name
            path.write_bytes(plistlib.dumps(value, fmt=plistlib.FMT_BINARY))
            paths.append(str(path))
            expected[name] = required
        # XML archives have the same parsed schema (UIDs use dictionary form).
        xml = Path(tmp) / "archive.xml"
        xml.write_bytes(plistlib.dumps({**archive, "$top": {"root": {"CF$UID": 1}}}))
        paths.append(str(xml))
        expected[xml.name] = {ARCHIVER, IB}
        # Content identity survives CMS wrapping and renaming. An unrelated
        # suspicious field must remain visible even inside such an envelope.
        for name, content, required in [
            ("wrapped-profile.bin", cases["provisioning.plist"][0], cases["provisioning.plist"][1]),
            ("wrapped-mixed.bin", cases["mixed.plist"][0], cases["mixed.plist"][1]),
        ]:
            path = Path(tmp) / name
            encoding = plistlib.FMT_BINARY if name == "wrapped-mixed.bin" else plistlib.FMT_XML
            path.write_bytes(cms_wrap(plistlib.dumps(content, fmt=encoding)))
            paths.append(str(path))
            expected[name] = required | {CMS}
        result = subprocess.run(
            [cleave, "--traits-dir", str(repo), "--format", "json", *paths],
            check=True, capture_output=True, text=True,
        )
        reports = [json.loads(line) for line in result.stdout.splitlines() if line.strip()]
        seen = set()
        for file in (file for report in reports for file in report["files"]):
            name = Path(file["path"]).name
            findings = file.get("traits", [])
            ids = {finding["id"] for finding in findings}
            actual = ids & REVIEWED
            assert actual == expected[name], (name, expected[name], actual)
            severe = {finding["id"] for finding in findings if finding["crit"] >= 4}
            assert severe == ({MASQUERADE} if name in {"mixed.plist", "wrapped-mixed.bin"} else set()), (name, severe)
            seen.add(name)
        assert seen == set(expected), (seen, set(expected))
    print(f"Passed {len(expected)} plist format and near-miss controls")


if __name__ == "__main__":
    main()
