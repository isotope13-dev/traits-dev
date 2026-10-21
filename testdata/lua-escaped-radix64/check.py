#!/usr/bin/env python3
"""Static controls for escaped Lua decoder concealment; run no sample code."""
import argparse
from pathlib import Path
import re
import subprocess
import tempfile


RULE = ("objectives/anti-static/obfuscation/encoding/base64::"
        "lua-escaped-table-radix64-concealment")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cleave", default="cleave")
    parser.add_argument("--fixture-parent", type=Path)
    args = parser.parse_args()
    # The large escaped population is required evidence, not filler to make
    # an exact sample-size signature. All controls use the same population.
    escaped = 'local strings={' + ','.join(
        [r'"\081\085\074\068"'] * 3200) + '}\n'
    decoder = ("local function decode(input) local total,index=0,0 "
               "for i=1,#input do local digit=alphabet[input:sub(i,i)] "
               "total=total+digit*64^(3-index) index=index+1 "
               "if index==4 then local high=floor(total/65536) "
               "local mid=floor((total%65536)/256) "
               "local low=total%256 output=string.char(high,mid,low) "
               "index=0 total=0 end end end\n")
    proxy = "local environment,proxy,meta=getfenv(),newproxy,setmetatable\n"
    positive = escaped + decoder + proxy
    renamed = re.sub(r"\b(total|index|digit|high|mid|low)\b",
                     lambda m: "renamed_" + m[0], positive)
    cases = [
        ("concealed.log", positive, True),
        ("renamed.txt", renamed, True),
        ("ordinary-decoder.lua", decoder, False),
        ("escaped-resources.log", escaped + proxy, False),
        ("no-indirection.log", escaped + decoder, False),
        ("different-radix.log", positive.replace("*64^", "*32^"), False),
        ("missing-byte-split.log", positive.replace("/65536)", "/1024)"), False),
    ]
    with tempfile.TemporaryDirectory(dir=args.fixture_parent) as directory:
        for name, source, expected in cases:
            path = Path(directory) / name
            path.write_text(source)
            result = subprocess.run(
                [args.cleave, "test-rules", str(path), "--rules", RULE],
                text=True, capture_output=True, check=True)
            output = result.stdout + result.stderr
            matched = bool(re.search(r"^MATCHED " + re.escape(RULE),
                                     output, re.MULTILINE))
            assert "ERROR" not in output and "not found" not in output, output
            assert matched == expected, (name, expected, output)
            print("PASS", name)


if __name__ == "__main__":
    main()
