#!/usr/bin/env python3
"""Check neutral HTTP vocabulary without depending on a compiler or specimen."""
import json
import os
from pathlib import Path
import struct
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[3]
TRAIT = "micro-behaviors/communications/http/message::request-line-and-url-vocabulary"
RETIRED = "objectives/command-and-control/channel/http/message::hardcoded-request"


def elf(strings):
    """Non-executable ELF64 fixture with a read-only string section."""
    # The existing URL-prefix dependency requires a parsed literal. Model an
    # embedded helper's URL independently of the native request line, as in
    # applications that ship source resources alongside compiled HTTP code.
    strings = [
        (b'#!/usr/bin/env python3\nimport sys\n\ndef show_endpoint():\n'
         b'    endpoint = "' + value + b'"\n'
         b'    sys.stdout.write(endpoint + "\\n")\n'
         b'    return endpoint\n\n'
         b'if __name__ == "__main__":\n    show_endpoint()\n')
        if value.startswith((b"http://", b"https://")) else value
        for value in strings
    ]
    payload = b"\0".join(strings) + b"\0"
    names = b"\0.rodata\0.shstrtab\0"
    data_offset = 64
    names_offset = data_offset + len(payload)
    sections_offset = (names_offset + len(names) + 7) & ~7
    header = struct.pack(
        "<16sHHIQQQIHHHHHH", b"\x7fELF\x02\x01\x01" + b"\0" * 9,
        2, 62, 1, 0, 0, sections_offset, 0, 64, 0, 0, 64, 3, 2,
    )
    sections = bytes(64)
    sections += struct.pack("<IIQQQQIIQQ", 1, 1, 2, data_offset,
                            data_offset, len(payload), 0, 0, 1, 0)
    sections += struct.pack("<IIQQQQIIQQ", 9, 3, 0, 0,
                            names_offset, len(names), 0, 0, 1, 0)
    return (header + payload + names).ljust(sections_offset, b"\0") + sections


def main():
    cases = {
        "loopback-get": ([b"http://127.0.0.1:1455", b"GET /stop HTTP/1.1\r\n"], True),
        "remote-get": ([b"https://example.org/", b"GET /status HTTP/1.0\r\n"], True),
        "remote-post": ([b"https://example.org/", b"POST /events HTTP/1.1\r\n"], True),
        "documentation": ([b"https://example.org/", b"GET /index.html HTTP/1.1"], True),
        "url-only": ([b"https://example.org/"], False),
        "request-only": ([b"GET /status HTTP/1.1\r\n"], False),
    }
    with tempfile.TemporaryDirectory(prefix="http-vocabulary-", dir=ROOT / "testdata") as temp:
        paths = []
        for name, (strings, _) in cases.items():
            path = Path(temp) / (name + ".elf")
            path.write_bytes(elf(strings))
            paths.append(str(path))
        result = subprocess.run(
            [os.environ.get("CLEAVE", "cleave"), "--traits-dir", str(ROOT),
             "--format", "json", *paths],
            check=True, capture_output=True, text=True,
        )
        # Multiple targets may emit adjacent JSON report objects.
        decoder = json.JSONDecoder()
        remaining = result.stdout.lstrip()
        files = []
        while remaining:
            report, end = decoder.raw_decode(remaining)
            files.extend(report["files"])
            remaining = remaining[end:].lstrip()
        seen = set()
        for file in files:
            name = Path(file["path"]).stem
            seen.add(name)
            traits = {t["id"]: t for t in file.get("traits", [])}
            assert (TRAIT in traits) == cases[name][1], (name, traits)
            assert RETIRED not in traits, name
            if TRAIT in traits:
                assert traits[TRAIT]["crit"] == 3, (name, traits[TRAIT])
        assert seen == set(cases), seen
    print("PASS: six HTTP vocabulary positive/near-miss controls")


if __name__ == "__main__":
    main()
