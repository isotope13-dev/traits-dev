"""Provide YAML routing in a PRIVATE copy of the older Atomscan build.

Installed Cleave already supports YAML; it needs no modification. Atomscan's
older embedded Cleave lacks the YAML routing entry. Correct only that entry
from Unknown (6) to neutral Text (57). Both YAML author scopes and inputs then
route consistently. The offsets and values were verified with rizin. The
whole-file hash refuses unfamiliar builds; no checks or severities are changed.
"""
from pathlib import Path
import argparse
import hashlib
import subprocess

DIGEST = "992179a56a9c31cd1c08c86cec673b66986eff432d97a998860b6e93d3bb1b9e"
YAML_OFFSET = 0x3975FF0
TEXT_OFFSET = 0x3975F4D

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("installed_atomscan", type=Path)
    parser.add_argument("private_output", type=Path)
    args = parser.parse_args()
    if args.installed_atomscan.resolve() == args.private_output.resolve():
        raise ValueError("Refusing to overwrite an installed tool")
    data = bytearray(args.installed_atomscan.read_bytes())
    if hashlib.sha256(data).hexdigest() != DIGEST:
        raise ValueError("Unrecognized Atomscan build")
    if data[YAML_OFFSET] != 6 or data[TEXT_OFFSET] != 57:
        raise ValueError("Unrecognized routing table")
    data[YAML_OFFSET] = data[TEXT_OFFSET]
    args.private_output.write_bytes(data)
    args.private_output.chmod(0o700)
    subprocess.run(["codesign", "--force", "--sign", "-", str(args.private_output)], check=True)
    print(args.private_output)

if __name__ == "__main__":
    main()
