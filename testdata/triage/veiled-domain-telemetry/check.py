"""Check the veiled-domain telemetry rotation and the aggregation channel.

The triaged wallet kit replaced its seed-arithmetic IP builder with a
literal domain whose scheme separators arrive as character codes, and its
per-value reporting callback with a password-input scrape joined into one
bulk report. Either rotation alone dropped the old composites:

- positive-veiled-telemetry.js: literal-domain builder plus input-spread
  JSON POST fires js-veiled-domain-endpoint-json-post while
  js-numeric-endpoint-json-post stays absent.
- positive-numeric-telemetry.js: octet-arithmetic builder plus input-spread
  JSON POST fires js-numeric-endpoint-json-post while the veiled finding
  stays absent (the unless: separation).
- negative-plain-telemetry.js: literal-URL POST of caller input fires
  neither concealment finding.
- positive-aggregate-harvest.js: password-selected inputs read, pushed,
  and joined fires password-field-values-collected-joined. The finding
  feeds wallet-input-telemetry-http-exfiltration through the
  dom-value-report-channel group, which also accepts value reporting with
  DOM edit/submit listeners. The staged archive assert below exercises the
  password-aggregation alternative without requiring an event listener.
- negative-form-echo.js: password selector loop that never reads value
  fires neither.
- staged-full-veiled.zip: no-data-claim manifest plus seed-entry page plus
  both positives fires wallet-input-telemetry-http-exfiltration.
- staged-full-plain.zip: same entry/report surface with a plain-URL sender
  fires no such hostile (no concealed sink).

Controls are synthetic variants, not sample bytes.
"""
import json
import pathlib
import shutil
import subprocess
import tempfile
import zipfile

root = pathlib.Path(__file__).resolve().parents[3]
fixtures = pathlib.Path(__file__).resolve().parent

MANIFEST = """\
{
  "manifest_version": 2,
  "name": "Control Panel",
  "version": "1.0",
  "permissions": ["clipboardRead"],
  "browser_specific_settings": {
    "gecko": {
      "data_collection_permissions": {"required": ["none"], "optional": []},
      "id": "{00000000-0000-4000-8000-000000000000}"
    }
  }
}
"""

ENTRY = """\
<html><body>
<h1>Enter your secret recovery phrase</h1>
<p>Type each wallet seed word below to restore your mnemonic vault.</p>
<input type="password" id="w1"><input type="password" id="w2">
<label>Private key import</label><input type="password" id="pk">
</body></html>
"""

VEILED = "objectives/anti-static/obfuscation/string/charcode-url::js-veiled-domain-endpoint-json-post"
NUMERIC = "objectives/anti-static/obfuscation/string/charcode-url::js-numeric-endpoint-json-post"
AGGREGATE = "micro-behaviors/data/property/access::password-field-values-collected-joined"
WALLET = "objectives/exfiltration/stealer/wallet::wallet-input-telemetry-http-exfiltration"

# Staged into a fresh temp dir before scanning: paths under this repo's own
# testdata/ tree can match harness test-presence markers, which suppress
# some legs. The committed bytes are the test; the temp location is just
# scaffolding.
with tempfile.TemporaryDirectory(prefix="veiled-") as stage:
    staged = pathlib.Path(stage)
    for control in ("positive-veiled-telemetry.js",
                    "positive-numeric-telemetry.js",
                    "negative-plain-telemetry.js",
                    "positive-aggregate-harvest.js",
                    "negative-form-echo.js"):
        shutil.copy(fixtures / control, staged / control)
    for name, sender in (("staged-full-veiled.zip",
                          "positive-veiled-telemetry.js"),
                         ("staged-full-plain.zip",
                          "negative-plain-telemetry.js")):
        with zipfile.ZipFile(staged / name, "w") as archive:
            archive.writestr("manifest.json", MANIFEST)
            archive.writestr("entry.html", ENTRY)
            archive.writestr("sender.js",
                             (fixtures / sender).read_text())
            archive.writestr("harvest.js",
                             (fixtures / "positive-aggregate-harvest.js").read_text())
    result = subprocess.run(
        ["cleave", "--traits-dir", str(root), "--format", "json", stage],
        check=True, capture_output=True, text=True,
    )
remaining = result.stdout.lstrip()
decoder = json.JSONDecoder()
reports = {}
while remaining:
    report, end = decoder.raw_decode(remaining)
    remaining = remaining[end:].lstrip()
    for item in report["files"]:
        reports[pathlib.Path(item["path"]).name] = item["traits"]


def has(name, rule_id):
    return rule_id in {t["id"] for t in reports[name]}


assert has("positive-veiled-telemetry.js", VEILED), "veiled positive"
assert not has("positive-veiled-telemetry.js", NUMERIC), "veiled separation"
assert has("positive-numeric-telemetry.js", NUMERIC), "numeric positive"
assert not has("positive-numeric-telemetry.js", VEILED), "numeric separation"
assert not has("negative-plain-telemetry.js", VEILED), "plain veiled"
assert not has("negative-plain-telemetry.js", NUMERIC), "plain numeric"
assert has("positive-aggregate-harvest.js", AGGREGATE), "aggregate positive"
assert not has("negative-form-echo.js", AGGREGATE), "echo aggregate"
assert has("staged-full-veiled.zip", WALLET), "archive hostile"
assert not has("staged-full-plain.zip", WALLET), "archive boundary"

print("veiled-domain-telemetry: all checks pass")
