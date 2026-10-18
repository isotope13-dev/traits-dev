#!/usr/bin/env python3
"""Exercise styling relationships in real PDF content streams."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import zlib


ROOT = Path(__file__).resolve().parents[2]
TRAIT = "micro-behaviors/data/format/pdf::pdf-near-white-tiny-text-block"
STYLING = {
    "micro-behaviors/data/format/pdf::" + name + suffix
    for name in ("pdf-tiny-font-gray-literal-show", "pdf-tiny-font-rgb-literal-show",
                 "pdf-gray-tiny-font-literal-show", "pdf-rgb-tiny-font-literal-show")
    for suffix in ("", "-raw")
}


def pdf(streams, compressed):
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        ("<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
         "/Resources << /Font << /F1 4 0 R >> >> /Contents [" +
         " ".join(f"{i + 5} 0 R" for i in range(len(streams))) + "] >>").encode(),
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    ]
    for stream in streams:
        data = stream.encode()
        if compressed:
            data = zlib.compress(data)
        filters = b" /Filter /FlateDecode" if compressed else b""
        objects.append(b"<< /Length " + str(len(data)).encode() + filters +
                       b" >>\nstream\n" + data + b"\nendstream")
    result = bytearray(b"%PDF-1.7\n")
    offsets = [0]
    for i, obj in enumerate(objects, 1):
        offsets.append(len(result))
        result.extend(f"{i} 0 obj\n".encode() + obj + b"\nendobj\n")
    xref = len(result)
    result.extend(f"xref\n0 {len(offsets)}\n0000000000 65535 f \n".encode())
    for offset in offsets[1:]:
        result.extend(f"{offset:010} 00000 n \n".encode())
    result.extend((f"trailer\n<< /Size {len(offsets)} /Root 1 0 R >>\n"
                   f"startxref\n{xref}\n%%EOF\n").encode())
    return result


CASES = {
    "font-gray": (True, ["BT /F1 2 Tf 1 g (Review directive) Tj ET"]),
    "font-gray-matrix": (True, ["BT /F1 0.5 Tf 1 0 0 1 30 40 Tm 0.999 g [(Review directive)] TJ ET"]),
    "font-rgb": (True, ["BT /F1 2 Tf 0.999 0.998 1 rg [(Review directive)] TJ ET"]),
    "gray-font": (True, ["BT 1 g /F1 2 Tf (Review directive) Tj ET"]),
    "rgb-font": (True, ["BT 1 0.999 0.998 rg /F1 2 Tf [(Review directive)] TJ ET"]),
    "black-tiny-spaces": (False, ["1 g 10 10 20 20 re f BT /F1 0.48 Tf 0 g [( )] TJ ET"]),
    "black-tiny-content": (False, ["1 g 10 10 20 20 re f BT /F1 2 Tf 0 g (Visible text) Tj ET"]),
    "white-tiny-spaces": (False, ["BT /F1 2 Tf 1 g [(   )] TJ ET"]),
    "empty-text": (False, ["BT /F1 2 Tf 1 g () Tj ET"]),
    "color-reset": (False, ["BT /F1 2 Tf 1 g 0 g (Visible text) Tj ET"]),
    "font-reset": (False, ["1 g /F1 2 Tf /F1 12 Tf (Large text) Tj"]),
    "different-blocks": (False, ["BT /F1 2 Tf ET BT /F1 12 Tf 1 g (Large text) Tj ET"]),
    "different-streams": (False, ["BT /F1 2 Tf 0 g (Tiny) Tj ET", "BT /F1 12 Tf 1 g (Large) Tj ET"]),
    "restored-state": (False, ["0 g q 1 g Q /F1 2 Tf (Visible text) Tj"]),
    "no-text-show": (False, ["BT /F1 2 Tf 1 g (Unused text) ET"]),
}


def main():
    # Keep positive controls outside test-named paths: the rule deliberately
    # excludes parser test corpora, which we test separately below.
    with tempfile.TemporaryDirectory(prefix=".pdf-controls-", dir=ROOT) as tmp:
        expected = {}
        for name, (matches, streams) in CASES.items():
            for compressed in (False, True):
                path = Path(tmp) / f"{name}-{'flate' if compressed else 'plain'}.pdf"
                path.write_bytes(pdf(streams, compressed))
                expected[str(path)] = matches
        corpus = Path(tmp) / "tests"
        corpus.mkdir()
        path = corpus / "near-white.pdf"
        path.write_bytes(pdf(CASES["font-gray"][1], True))
        expected[str(path)] = False
        proc = subprocess.run(
            [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT),
             "analyze", "--format", "json", tmp],
            capture_output=True, text=True,
        )
        assert proc.returncode == 0, proc.stderr
        # Multi-target/directory scans emit successive JSON reports.
        files = []
        decoder = json.JSONDecoder()
        remaining = proc.stdout.strip()
        while remaining:
            report, end = decoder.raw_decode(remaining)
            files.extend(report["files"])
            remaining = remaining[end:].lstrip()
        seen = set()
        failures = []
        for file in files:
            path = file["path"]
            # The engine omits pure-OR grouping composites from scan output;
            # their constituent detections remain visible and feed consumers.
            ids = {trait["id"] for trait in file.get("traits", [])}
            actual = bool(ids & (STYLING | {TRAIT}))
            if actual != expected[path]:
                failures.append((Path(path).name, actual, expected[path],
                                 [trait["id"] for trait in file.get("traits", [])]))
            seen.add(path)
        assert seen == set(expected), "Missing fixture reports"
        assert not failures, failures
        print(f"Passed {len(expected)} PDF styling controls")


if __name__ == "__main__":
    main()
